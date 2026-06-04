#!/usr/bin/env python3
"""GRB inter-rater reliability analysis from assessor score YAML files."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.reliability import (
    CSV_FIELDNAMES,
    csv_rows_from_result,
    render_irr_report,
    run_grb_irr_study,
)

DEFAULT_RATINGS = ROOT / "examples" / "grb" / "inter_rater"
CSV_PATH = ROOT / "results" / "inter_rater_reliability.csv"
REPORT_PATH = ROOT / "reports" / "inter_rater_reliability.md"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    if not DEFAULT_RATINGS.exists():
        print(f"Ratings directory not found: {DEFAULT_RATINGS}", file=sys.stderr)
        return 1

    result = run_grb_irr_study(DEFAULT_RATINGS)
    rows = csv_rows_from_result(result)
    write_csv(CSV_PATH, rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_irr_report(result), encoding="utf-8")

    m = result.metrics
    print("GRB inter-rater reliability")
    print("=" * 40)
    print(f"Study: {m.study_id}")
    print(f"Units: {m.n_units} | Raters: {m.n_raters}")
    print(f"Percent agreement: {m.percent_agreement:.2%}")
    for pair, value in sorted(m.cohens_kappa_pairs.items()):
        print(f"Cohen's κ ({pair}): {value}")
    if m.fleiss_kappa is not None:
        print(f"Fleiss' κ: {m.fleiss_kappa} ({m.kappa_interpretation})")
    print(f"Disagreements: {len(result.disagreement_rows)}")
    print(f"CSV: {CSV_PATH}")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
