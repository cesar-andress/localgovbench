#!/usr/bin/env python3
"""GRB sensitivity analysis — >=150 deterministic synthetic profiles."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.sensitivity import (
    CSV_FIELDNAMES,
    MIN_PROFILE_COUNT,
    generate_profile_specs,
    render_sensitivity_report,
    run_sensitivity_study,
)

CSV_PATH = ROOT / "results" / "grb_sensitivity_analysis.csv"
REPORT_PATH = ROOT / "reports" / "grb_sensitivity_analysis.md"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in CSV_FIELDNAMES})


def main() -> int:
    specs = generate_profile_specs()
    rows = run_sensitivity_study()
    write_csv(CSV_PATH, rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_sensitivity_report(rows), encoding="utf-8")

    print("GRB sensitivity analysis")
    print("=" * 40)
    print(f"Profiles generated: {len(specs)} (minimum {MIN_PROFILE_COUNT})")
    print(f"CSV: {CSV_PATH}")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
