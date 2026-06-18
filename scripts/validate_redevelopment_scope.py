#!/usr/bin/env python3
"""Validate manuscript-facing LocalGovBench redevelopment scope guards.

Scans only the new instrument-validation layer (see validation/redevelopment_scope.yaml).
Does not scan submitted-paper reproduction assets, archived material, tests, or demos.

Exit 0 if scope guards pass; exit 1 on forbidden primary-evidence claims or missing templates.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE_FILE = ROOT / "validation" / "redevelopment_scope.yaml"
SCOPE_DEFINITION_FILE = SCOPE_FILE  # excluded from pattern matching (contains regex definitions)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt", ".json", ".csv", ".tex"}


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit(
            "PyYAML required: pip install pyyaml (or pip install -e '.[dev]')"
        ) from exc
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"Invalid scope file (expected mapping): {path}")
    return data


def _collect_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    if base.is_file():
        return [base]
    files: list[Path] = []
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES:
            files.append(p)
    return sorted(files)


def _normalize_for_negation(text: str) -> str:
    return re.sub(r"\*+", "", text.lower())


def _is_prohibition_context(file_text: str, line: str) -> bool:
    """Bullet or table row listing forbidden outcomes (not claims)."""
    lower_file = _normalize_for_negation(file_text)
    stripped = line.strip()
    if stripped.startswith("- ") and any(
        m in lower_file
        for m in (
            "does not authorise",
            "does not authorize",
            "must not",
            "forbidden as primary",
            "forbidden_primary",
            "not_primary_evidence",
            "forbidden_evidence",
        )
    ):
        return True
    if "|" in stripped and "forbidden as primary evidence" in lower_file:
        parts = [p.strip() for p in stripped.split("|") if p.strip()]
        if len(parts) >= 1 and parts[0] not in ("Allowed primary evidence", "—", "-"):
            # Second column of forbidden table, or single forbidden cell
            if len(parts) >= 2 or "synthetic irr" in stripped.lower():
                return True
    return False


def _line_has_negation(line: str, negations: list[str]) -> bool:
    lower = _normalize_for_negation(line)
    return any(n.lower() in lower for n in negations)


def _is_pattern_definition_line(line: str) -> bool:
    stripped = line.strip()
    if re.match(r'^-\s+".*\.\*', stripped):
        return True
    if "forbidden_primary_evidence_patterns:" in stripped:
        return True
    if stripped.startswith("patterns:"):
        return True
    return False


def _scan_forbidden_patterns(
    files: list[Path],
    patterns_by_id: dict[str, list[str]],
    negations: list[str],
) -> list[str]:
    errors: list[str] = []
    compiled: list[tuple[str, str, re.Pattern[str]]] = []
    for rule_id, patterns in patterns_by_id.items():
        for pat in patterns:
            compiled.append((rule_id, pat, re.compile(pat, re.IGNORECASE)))

    for file_path in files:
        if file_path.resolve() == SCOPE_DEFINITION_FILE.resolve():
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"Cannot read {file_path.relative_to(ROOT)}: {exc}")
            continue
        rel = file_path.relative_to(ROOT)
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if _is_pattern_definition_line(line):
                continue
            if _is_prohibition_context(text, line):
                continue
            for rule_id, raw_pat, regex in compiled:
                if regex.search(line) and not _line_has_negation(line, negations):
                    errors.append(
                        f"{rel}:{line_no} [{rule_id}] forbidden primary-evidence claim "
                        f"(pattern: {raw_pat!r})\n  > {stripped[:160]}"
                    )
    return errors


def _check_export_synthetic_flags(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for file_path in files:
        if file_path.parent.name != "validation" and "exports/validation" not in str(
            file_path
        ):
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = file_path.relative_to(ROOT)
        if re.search(r"\bsynthetic:\s*true\b", text, re.IGNORECASE):
            if "training" not in text.lower() and "not field" not in text.lower():
                errors.append(
                    f"{rel}: synthetic: true in exports/validation "
                    "(forbidden for publishable validation exports)"
                )
        if re.search(r"study_id:\s*.*synthetic", text, re.IGNORECASE):
            errors.append(f"{rel}: synthetic study_id in exports/validation")
    return errors


def _check_required_templates(templates: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in templates:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"Missing required template: {rel}")
    return errors


def main() -> int:
    if not SCOPE_FILE.is_file():
        print(f"ERROR: scope file not found: {SCOPE_FILE}", file=sys.stderr)
        return 1

    scope = _load_yaml(SCOPE_FILE)
    manuscript_paths: list[str] = scope.get("manuscript_facing_paths", [])
    required_templates: list[str] = scope.get("required_templates", [])
    forbidden_patterns: dict[str, list[str]] = scope.get(
        "forbidden_primary_evidence_patterns", {}
    )
    negations: list[str] = scope.get("allowed_negation_phrases", [])

    patterns_by_id: dict[str, list[str]] = {}
    if isinstance(forbidden_patterns, dict):
        for rule_id, rule in forbidden_patterns.items():
            if isinstance(rule, dict):
                patterns_by_id[str(rule_id)] = list(rule.get("patterns", []))
    elif isinstance(forbidden_patterns, list):
        for rule in forbidden_patterns:
            if isinstance(rule, dict) and "id" in rule:
                patterns_by_id[str(rule["id"])] = list(rule.get("patterns", []))

    scan_files: list[Path] = []
    for rel in manuscript_paths:
        scan_files.extend(_collect_files(ROOT / rel))
    scan_files = sorted(set(scan_files))

    errors: list[str] = []
    errors.extend(_check_required_templates(required_templates))
    errors.extend(_scan_forbidden_patterns(scan_files, patterns_by_id, negations))
    errors.extend(_check_export_synthetic_flags(scan_files))

    print("LocalGovBench redevelopment scope validation")
    print(f"  Root: {ROOT}")
    print(f"  Scanned paths: {len(manuscript_paths)}")
    print(f"  Scanned files: {len(scan_files)}")
    print(f"  Required templates: {len(required_templates)}")

    if errors:
        print(f"\nFAILED — {len(errors)} issue(s):\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\nPASSED — no forbidden primary-evidence claims in manuscript-facing layer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
