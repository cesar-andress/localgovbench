#!/usr/bin/env python3
"""Validate expert Delphi response YAML files (structure, ratings, pseudonymity, scope)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESPONSES_DIR = ROOT / "validation" / "content_validity" / "delphi" / "responses"
INSTRUMENT = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_instrument.yaml"

EXPECTED_CRITERIA = 25
EXPERT_ID_PATTERN = re.compile(r"^exp_\d{3}$")
RESPONSE_FIELDS = (
    "relevance_1_5",
    "clarity_1_5",
    "essential_yes_no",
    "suggested_revision",
    "comment",
)

PII_FIELD_NAMES = frozenset(
    {
        "name",
        "full_name",
        "first_name",
        "last_name",
        "email",
        "personal_email",
        "phone",
        "telephone",
        "mobile",
        "address",
        "postal_address",
        "employer",
        "institution",
        "institution_name",
        "organization",
        "organisation",
        "affiliation",
        "municipality",
        "city_name",
        "linkedin",
        "orcid",
    }
)

FORBIDDEN_OBSERVABILITY_PATTERNS = [
    re.compile(r"public.document observability", re.I),
    re.compile(r"public ai register", re.I),
    re.compile(r"transparency portal", re.I),
    re.compile(r"open.web documentary", re.I),
    re.compile(r"assess.*public.*document", re.I),
    re.compile(r"observable from public", re.I),
]


def load_yaml(path: Path) -> dict:
    from localgovbench.utils.io import load_yaml as _load

    data = _load(path)
    if not isinstance(data, dict):
        raise ValueError("root must be a mapping")
    return data


def expected_criterion_ids() -> set[str]:
    instrument = load_yaml(INSTRUMENT)
    criteria = instrument.get("criteria") or []
    return {c["criterion_id"] for c in criteria if isinstance(c, dict) and c.get("criterion_id")}


def collect_pii_keys(obj: object, prefix: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            if key_lower in PII_FIELD_NAMES:
                found.append(f"{prefix}{key}" if prefix else key_lower)
            found.extend(collect_pii_keys(value, prefix=f"{prefix}{key}."))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(collect_pii_keys(item, prefix=f"{prefix}[{i}]."))
    return found


def check_text_for_observability(text: str, field_label: str) -> list[str]:
    errors: list[str] = []
    for pattern in FORBIDDEN_OBSERVABILITY_PATTERNS:
        if pattern.search(text):
            errors.append(
                f"{field_label} appears to claim public-document observability assessment: "
                f"matched {pattern.pattern!r}"
            )
    return errors


def validate_rating(field: str, value: object) -> str | None:
    if value is None:
        return None
    if field in ("relevance_1_5", "clarity_1_5"):
        if not isinstance(value, int) or value < 1 or value > 5:
            return f"{field} must be null or integer 1–5, got {value!r}"
        return None
    if field == "essential_yes_no":
        if not isinstance(value, bool):
            return f"{field} must be null or boolean, got {value!r}"
        return None
    if field in ("suggested_revision", "comment"):
        if value is not None and not isinstance(value, str):
            return f"{field} must be null or string, got {value!r}"
        return None
    return None


def validate_file(path: Path, expected_ids: set[str]) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [f"{path.name}: failed to load YAML: {exc}"]

    expert_id = data.get("expert_id")
    if not isinstance(expert_id, str) or not EXPERT_ID_PATTERN.match(expert_id):
        errors.append(f"{path.name}: expert_id must match exp_NNN, got {expert_id!r}")

    if data.get("synthetic") is True:
        errors.append(f"{path.name}: synthetic responses must not be used as validation evidence")

    if data.get("confidential") is not True:
        errors.append(f"{path.name}: confidential must be true")

    responses = data.get("responses")
    if not isinstance(responses, list):
        return errors + [f"{path.name}: missing 'responses' list"]
    if len(responses) != EXPECTED_CRITERIA:
        errors.append(f"{path.name}: expected {EXPECTED_CRITERIA} criteria, found {len(responses)}")

    seen_ids: set[str] = set()
    for idx, item in enumerate(responses):
        if not isinstance(item, dict):
            errors.append(f"{path.name}: responses[{idx}] must be a mapping")
            continue
        cid = item.get("criterion_id")
        if not cid:
            errors.append(f"{path.name}: responses[{idx}] missing criterion_id")
            continue
        seen_ids.add(cid)
        for field in RESPONSE_FIELDS:
            if field not in item:
                errors.append(f"{path.name}: {cid} missing field {field}")
                continue
            err = validate_rating(field, item[field])
            if err:
                errors.append(f"{path.name}: {cid}: {err}")
        for field in ("suggested_revision", "comment"):
            val = item.get(field)
            if isinstance(val, str) and val.strip():
                errors.extend(check_text_for_observability(val, f"{path.name}:{cid}:{field}"))

    missing = expected_ids - seen_ids
    extra = seen_ids - expected_ids
    if missing:
        errors.append(f"{path.name}: missing criterion_ids: {sorted(missing)}")
    if extra:
        errors.append(f"{path.name}: unknown criterion_ids: {sorted(extra)}")

    pii_keys = collect_pii_keys(data)
    if pii_keys:
        errors.append(f"{path.name}: forbidden PII fields present: {pii_keys}")

    framing = data.get("study_framing") or {}
    if framing.get("forbidden_basis") == "public-document observability":
        pass  # expected guard label
    elif framing.get("evidence_layer") not in (None, "confidential programme dossier"):
        errors.append(
            f"{path.name}: study_framing.evidence_layer must be 'confidential programme dossier'"
        )

    instruction = framing.get("instruction") or ""
    if isinstance(instruction, str) and instruction.strip():
        for pattern in FORBIDDEN_OBSERVABILITY_PATTERNS:
            if pattern.search(instruction) and "do not" not in instruction.lower():
                errors.append(
                    f"{path.name}: study_framing.instruction may assert forbidden observability basis"
                )
                break

    return errors


def main() -> int:
    if not RESPONSES_DIR.is_dir():
        print(f"No responses directory: {RESPONSES_DIR}", file=sys.stderr)
        return 1

    yaml_files = sorted(RESPONSES_DIR.glob("*.yaml"))
    if not yaml_files:
        print(f"No response YAML files in {RESPONSES_DIR}", file=sys.stderr)
        return 1

    if not INSTRUMENT.is_file():
        print(f"Instrument not found: {INSTRUMENT}", file=sys.stderr)
        return 1

    expected_ids = expected_criterion_ids()
    if len(expected_ids) != EXPECTED_CRITERIA:
        print(f"Instrument criterion count mismatch: {len(expected_ids)}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in yaml_files:
        all_errors.extend(validate_file(path, expected_ids))

    print("Delphi response validation")
    print(f"Files checked: {len(yaml_files)}")
    print(f"Expected criteria per file: {EXPECTED_CRITERIA}")

    if all_errors:
        print(f"FAIL: {len(all_errors)} issue(s)", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("PASS: all response files valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
