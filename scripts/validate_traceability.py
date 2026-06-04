#!/usr/bin/env python3
"""Validate and regenerate LocalGovBench construct traceability artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.traceability import sync_traceability_artifacts

CSV_PATH = ROOT / "data" / "traceability" / "indicator_mapping.csv"
REPORT_PATH = ROOT / "reports" / "traceability_report.md"


def main() -> int:
    result = sync_traceability_artifacts(csv_path=CSV_PATH, report_path=REPORT_PATH)

    print("Construct traceability validation")
    print("=" * 40)
    print(f"Indicators mapped: {result.mapped_indicators}/{result.expected_indicators}")
    print(f"Mapping rows: {result.row_count}")
    print(f"Status: {'PASS' if result.ok else 'FAIL'}")
    if result.missing_indicator_ids:
        print("Missing:", ", ".join(result.missing_indicator_ids))
    if result.orphan_indicator_ids:
        print("Orphans:", ", ".join(result.orphan_indicator_ids))
    if result.missing_dimension_ids:
        print("Missing dimensions:", ", ".join(result.missing_dimension_ids))
    print(f"CSV: {CSV_PATH}")
    print(f"Report: {REPORT_PATH}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
