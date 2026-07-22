#!/usr/bin/env python3
"""Validate exported Delphi Round 1 participant package."""

from __future__ import annotations

import csv
import json
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_delphi_round1_instrument import build_criteria, load_traceability  # noqa: E402
from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS  # noqa: E402

PACKAGE_DIR = ROOT / "exports" / "delphi_round1"
VALIDATION_JSON = ROOT / "exports" / "validation" / "delphi_package_validation.json"

REQUIRED_FILES = [
    "participant_questionnaire.md",
    "criterion_catalog.csv",
    "criterion_catalog.xlsx",
    "participant_instructions.md",
    "consent_information.md",
]

CATALOG_COLUMNS = [
    "criterion_id",
    "dimension_id",
    "dimension_name",
    "assessment_question",
    "criterion_description",
    "documentation_hint",
    "risk_if_missing",
    "traceability_references",
    "relevance_1_5",
    "clarity_1_5",
    "essential_yes_no",
    "suggested_revision",
    "comment",
]


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def count_xlsx_rows(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        sheet = archive.read("xl/worksheets/sheet1.xml")
    root = ElementTree.fromstring(sheet)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows = root.findall(".//m:sheetData/m:row", ns)
    return max(0, len(rows) - 1)


def validate_package() -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_FILES:
        if not (PACKAGE_DIR / name).is_file():
            errors.append(f"Missing required file: exports/delphi_round1/{name}")

    pdf_path = PACKAGE_DIR / "participant_questionnaire.pdf"
    pdf_present = pdf_path.is_file()
    if not pdf_present:
        warnings.append(
            "participant_questionnaire.pdf not present (optional if pandoc unavailable)"
        )

    traceability = load_traceability()
    expected_criteria, missing_trace = build_criteria(traceability)
    expected_ids = [item["criterion_id"] for item in expected_criteria]
    expected_dimension_ids = {dim.id for dim in GOVERNANCE_DIMENSIONS}

    if missing_trace:
        errors.append(
            f"Source traceability incomplete for {len(missing_trace)} criterion(s): "
            + ", ".join(missing_trace)
        )

    if len(expected_criteria) != 25:
        errors.append(f"Source specification has {len(expected_criteria)} criteria, expected 25")
    if len(expected_dimension_ids) != 5:
        errors.append(f"Source specification has {len(expected_dimension_ids)} dimensions, expected 5")

    csv_rows: list[dict[str, str]] = []
    csv_path = PACKAGE_DIR / "criterion_catalog.csv"
    if csv_path.is_file():
        csv_rows = load_csv_rows(csv_path)
        header = list(csv_rows[0].keys()) if csv_rows else []
        if header != CATALOG_COLUMNS:
            errors.append(
                f"criterion_catalog.csv columns mismatch: expected {CATALOG_COLUMNS}, got {header}"
            )

        if len(csv_rows) != 25:
            errors.append(f"criterion_catalog.csv has {len(csv_rows)} data rows, expected 25")

        ids = [row["criterion_id"] for row in csv_rows]
        dupes = [cid for cid, count in Counter(ids).items() if count > 1]
        if dupes:
            errors.append(f"Duplicate criterion_id in CSV: {', '.join(sorted(dupes))}")

        csv_dimension_ids = {row["dimension_id"] for row in csv_rows}
        if len(csv_dimension_ids) != 5:
            errors.append(
                f"criterion_catalog.csv has {len(csv_dimension_ids)} dimensions, expected 5"
            )

        missing_refs = [
            row["criterion_id"]
            for row in csv_rows
            if not row.get("traceability_references", "").strip()
        ]
        if missing_refs:
            errors.append(
                "Missing traceability references in CSV for: " + ", ".join(missing_refs)
            )

        for row in csv_rows:
            for field in ("relevance_1_5", "clarity_1_5", "essential_yes_no"):
                if row.get(field, "") != "":
                    warnings.append(
                        f"{row['criterion_id']}: response field {field} should be empty in export package"
                    )

        if set(ids) != set(expected_ids):
            missing = sorted(set(expected_ids) - set(ids))
            extra = sorted(set(ids) - set(expected_ids))
            if missing:
                errors.append(f"CSV missing criterion_id(s): {', '.join(missing)}")
            if extra:
                errors.append(f"CSV unexpected criterion_id(s): {', '.join(extra)}")

    xlsx_path = PACKAGE_DIR / "criterion_catalog.xlsx"
    if xlsx_path.is_file() and csv_rows:
        try:
            xlsx_count = count_xlsx_rows(xlsx_path)
            if xlsx_count != 25:
                errors.append(f"criterion_catalog.xlsx has {xlsx_count} data rows, expected 25")
        except (KeyError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
            errors.append(f"criterion_catalog.xlsx unreadable: {exc}")

    questionnaire = PACKAGE_DIR / "participant_questionnaire.md"
    if questionnaire.is_file():
        text = questionnaire.read_text(encoding="utf-8")
        for cid in expected_ids:
            if f"`{cid}`" not in text:
                errors.append(f"participant_questionnaire.md missing criterion block: {cid}")
        if text.count("### ") < 25:
            errors.append("participant_questionnaire.md appears to have fewer than 25 criterion sections")

    report = {
        "validation": "delphi_round1_participant_package",
        "validated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "package_dir": str(PACKAGE_DIR.relative_to(ROOT)),
        "status": "passed" if not errors else "failed",
        "criteria_count": len(csv_rows),
        "dimensions_count": len({row["dimension_id"] for row in csv_rows}) if csv_rows else 0,
        "expected_criteria_count": 25,
        "expected_dimensions_count": 5,
        "pdf_present": pdf_present,
        "errors": errors,
        "warnings": warnings,
        "files_checked": REQUIRED_FILES + (["participant_questionnaire.pdf"] if pdf_present else []),
    }
    return report


def main() -> int:
    if not PACKAGE_DIR.is_dir():
        print(f"Package directory not found: {PACKAGE_DIR}", file=sys.stderr)
        print("Run: python3.12 scripts/export_delphi_participant_package.py", file=sys.stderr)
        return 1

    report = validate_package()
    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("Delphi Round 1 package validation")
    print(f"  Package: {PACKAGE_DIR.relative_to(ROOT)}/")
    print(f"  Report:  {VALIDATION_JSON.relative_to(ROOT)}")
    print(f"  Criteria: {report['criteria_count']} (expected 25)")
    print(f"  Dimensions: {report['dimensions_count']} (expected 5)")
    print(f"  PDF: {'yes' if report['pdf_present'] else 'no'}")

    if report["warnings"]:
        print(f"\nWarnings ({len(report['warnings'])}):")
        for warning in report["warnings"]:
            print(f"  - {warning}")

    if report["errors"]:
        print(f"\nFAILED — {len(report['errors'])} issue(s):", file=sys.stderr)
        for err in report["errors"]:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\nPASSED — Delphi Round 1 participant package OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
