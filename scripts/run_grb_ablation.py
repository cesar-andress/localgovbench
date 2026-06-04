#!/usr/bin/env python3
"""GRB dimension ablation study on synthetic sensitivity profiles."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.ablation import (
    CSV_FIELDS,
    build_csv_rows,
    render_ablation_report,
    run_ablation_study,
)

CSV_PATH = ROOT / "results" / "grb_ablation.csv"
REPORT_PATH = ROOT / "reports" / "grb_ablation.md"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDS), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run GRB dimension ablation study.")
    parser.add_argument("--output-csv", type=Path, default=CSV_PATH)
    parser.add_argument("--output-report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    scores, comparisons, summary = run_ablation_study()
    rows = build_csv_rows(scores, comparisons, summary)
    write_csv(args.output_csv, rows)
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text(
        render_ablation_report(scores, comparisons, summary),
        encoding="utf-8",
    )

    print("GRB ablation study")
    print("=" * 40)
    print(f"Profiles: {summary['profile_count']}")
    print(f"Full model — mean readiness: {summary['full_mean_readiness_final']}")
    print(f"Full model — safeguard rate: {summary['full_safeguard_fraction']:.1%}")
    for comp in comparisons:
        print(
            f"  {comp.alternate}: mean Δ={comp.mean_readiness_delta:+.2f}, "
            f"spearman={comp.spearman:.4f}, safeguard Δ={comp.safeguard_activation_delta:+d}"
        )
    print(f"CSV: {args.output_csv}")
    print(f"Report: {args.output_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
