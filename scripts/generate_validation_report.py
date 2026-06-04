#!/usr/bin/env python3
"""Generate LocalGovBench scientific validation benchmark report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.irr import run_inter_rater_study
from localgovbench.validation.reports import render_validation_report

VALIDATION_ROOT = ROOT / "validation"
DEFAULT_REPORT = VALIDATION_ROOT / "reports" / "validation_benchmark_report.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate validation benchmark report.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_REPORT,
        help="Markdown report path",
    )
    parser.add_argument(
        "--ratings-dir",
        type=Path,
        default=VALIDATION_ROOT / "ratings",
    )
    args = parser.parse_args()

    irr_result = None
    if args.ratings_dir.exists() and list(args.ratings_dir.glob("*.yaml")):
        irr_result = run_inter_rater_study(args.ratings_dir)

    report = render_validation_report(
        validation_root=VALIDATION_ROOT,
        irr_result=irr_result,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    print("Validation benchmark report generated")
    print(f"Output: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
