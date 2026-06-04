#!/usr/bin/env python3
"""GRB Monte Carlo sensitivity — 10k random synthetic indicator profiles."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.grb.monte_carlo import (
    DEFAULT_PROFILE_COUNT,
    DISTRIBUTION_PRESETS,
    PROFILE_CSV_FIELDS,
    build_csv_rows,
    render_monte_carlo_report,
    run_monte_carlo_study,
    write_monte_carlo_figures,
)

CSV_PATH = ROOT / "results" / "grb_monte_carlo.csv"
REPORT_PATH = ROOT / "reports" / "grb_monte_carlo.md"
FIGURES_DIR = ROOT / "figures" / "grb_monte_carlo"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PROFILE_CSV_FIELDS))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in PROFILE_CSV_FIELDS})


def main() -> int:
    parser = argparse.ArgumentParser(description="GRB Monte Carlo sensitivity study.")
    parser.add_argument(
        "--profiles",
        type=int,
        default=DEFAULT_PROFILE_COUNT,
        help=f"Number of synthetic profiles (default {DEFAULT_PROFILE_COUNT})",
    )
    parser.add_argument(
        "--distribution",
        choices=sorted(DISTRIBUTION_PRESETS.keys()),
        default="uniform",
        help="Indicator score sampling preset",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-csv", type=Path, default=CSV_PATH)
    parser.add_argument("--output-report", type=Path, default=REPORT_PATH)
    parser.add_argument("--figures-dir", type=Path, default=FIGURES_DIR)
    parser.add_argument(
        "--skip-figures",
        action="store_true",
        help="Skip PNG generation (no matplotlib required)",
    )
    args = parser.parse_args()

    results, summary = run_monte_carlo_study(
        profile_count=args.profiles,
        distribution_name=args.distribution,
        seed=args.seed,
    )
    rows = build_csv_rows(results, summary)
    write_csv(args.output_csv, rows)
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.write_text(render_monte_carlo_report(summary), encoding="utf-8")

    figure_paths: list[Path] = []
    if not args.skip_figures:
        figure_paths = write_monte_carlo_figures(results, summary, args.figures_dir)

    print("GRB Monte Carlo sensitivity study")
    print("=" * 40)
    print(f"Profiles: {summary['profile_count']:,}")
    print(f"Distribution: {summary['distribution']}")
    print(
        f"Readiness final — mean {summary['readiness_final_mean']}, "
        f"std {summary['readiness_final_std']}"
    )
    print(f"Safeguard G1 applied: {summary['safeguard_applied_fraction']:.1%}")
    print(f"CSV: {args.output_csv}")
    print(f"Report: {args.output_report}")
    if figure_paths:
        print("Figures:")
        for path in figure_paths:
            print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
