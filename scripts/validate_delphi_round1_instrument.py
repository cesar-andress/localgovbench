#!/usr/bin/env python3
"""Validate generated Delphi Round 1 instrument YAML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTRUMENT = ROOT / "validation" / "content_validity" / "delphi" / "delphi_round1_instrument.yaml"

REQUIRED_RESPONSE_FIELDS = (
    "relevance_1_5",
    "clarity_1_5",
    "essential_yes_no",
    "suggested_revision",
    "comment",
)

FORBIDDEN_EVIDENCE_BASIS_PATTERNS = [
    re.compile(r"evidence_layer:\s*public", re.I),
    re.compile(r"evidence_basis:\s*public", re.I),
    re.compile(r"primary.*public.document observability", re.I),
    re.compile(r"public.document observability.*primary", re.I),
    re.compile(r"use public (ai )?registers as (the )?evidence", re.I),
    re.compile(r"transparency portals as (the )?evidence", re.I),
]

ALLOWED_FORBIDDEN_BASIS_LINES = re.compile(
    r"forbidden_basis:\s*public-document observability", re.I
)


def load_instrument() -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "PyYAML required: pip install pyyaml (or pip install -e '.[dev]')"
        ) from exc
    if not INSTRUMENT.is_file():
        raise SystemExit(f"Instrument not found: {INSTRUMENT}")
    text = INSTRUMENT.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise SystemExit("Instrument root must be a mapping")
    return data


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    criteria = data.get("criteria")
    if not isinstance(criteria, list):
        return ["Missing or invalid 'criteria' list"]

    if len(criteria) != 25:
        errors.append(f"Expected exactly 25 criteria, found {len(criteria)}")

    dimension_ids = {c.get("dimension_id") for c in criteria if isinstance(c, dict)}
    if len(dimension_ids) != 5:
        errors.append(f"Expected exactly 5 dimensions, found {len(dimension_ids)}: {sorted(dimension_ids)}")

    if data.get("synthetic") is True:
        errors.append("Instrument root must not be marked synthetic: true")

    framing = data.get("study_framing") or {}
    if framing.get("evidence_layer") != "confidential programme dossier":
        errors.append(
            f"study_framing.evidence_layer must be 'confidential programme dossier', "
            f"got {framing.get('evidence_layer')!r}"
        )
    if framing.get("forbidden_basis") != "public-document observability":
        errors.append(
            f"study_framing.forbidden_basis must be 'public-document observability', "
            f"got {framing.get('forbidden_basis')!r}"
        )

    text = INSTRUMENT.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), start=1):
        if ALLOWED_FORBIDDEN_BASIS_LINES.search(line):
            continue
        for pat in FORBIDDEN_EVIDENCE_BASIS_PATTERNS:
            if pat.search(line):
                errors.append(
                    f"{INSTRUMENT.relative_to(ROOT)}:{line_no} forbidden evidence basis: {line.strip()[:120]}"
                )

    seen_ids: set[str] = set()
    for idx, item in enumerate(criteria):
        prefix = f"criteria[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: expected mapping")
            continue
        cid = item.get("criterion_id")
        if not cid:
            errors.append(f"{prefix}: missing criterion_id")
            continue
        if cid in seen_ids:
            errors.append(f"Duplicate criterion_id: {cid}")
        seen_ids.add(cid)

        if item.get("synthetic") is True:
            errors.append(f"{cid}: must not be marked synthetic: true")

        question = item.get("assessment_question")
        if not question or not str(question).strip():
            errors.append(f"{cid}: empty assessment_question")

        response = item.get("response")
        if not isinstance(response, dict):
            errors.append(f"{cid}: missing response mapping")
            continue
        for field in REQUIRED_RESPONSE_FIELDS:
            if field not in response:
                errors.append(f"{cid}: missing response.{field}")

    return errors


def main() -> int:
    data = load_instrument()
    errors = validate(data)
    criteria = data.get("criteria") or []
    dims = sorted({c.get("dimension_id") for c in criteria if isinstance(c, dict)})

    print("Delphi Round 1 instrument validation")
    print(f"  File: {INSTRUMENT.relative_to(ROOT)}")
    print(f"  Criteria: {len(criteria)}")
    print(f"  Dimensions: {len(dims)}")

    if errors:
        print(f"\nFAILED — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\nPASSED — instrument structure and scope guards OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
