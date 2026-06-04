#!/usr/bin/env python3
"""Compute inter-rater reliability for LocalGovBench validation ratings."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.validation.irr import run_inter_rater_study

DEFAULT_RATINGS = ROOT / "validation" / "ratings"
DEFAULT_OUTPUT = ROOT / "validation" / "reports" / "irr_analysis.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inter-rater reliability analysis (κ, α).")
    parser.add_argument(
        "--ratings-dir",
        type=Path,
        default=DEFAULT_RATINGS,
        help="Directory with rater YAML files",
    )
    parser.add_argument(
        "--study-id",
        default="irr-pilot-synthetic",
        help="Study identifier",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path",
    )
    args = parser.parse_args()

    if not args.ratings_dir.exists():
        print(f"Ratings directory not found: {args.ratings_dir}", file=sys.stderr)
        return 1

    result = run_inter_rater_study(args.ratings_dir, study_id=args.study_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "study_id": result.study_id,
        "instrument_id": result.instrument_id,
        "overall": {
            "cohens_kappa": result.overall_kappa,
            "krippendorff_alpha": result.overall_alpha,
            "kappa_label": result.overall_kappa_label,
            "alpha_label": result.overall_alpha_label,
        },
        "cases": [
            {
                "case_id": c.case_id,
                "disagreement_count": c.disagreement_count,
                "n_criteria": c.n_criteria,
                "cohens_kappa": c.cohens_kappa,
                "krippendorff_alpha": c.krippendorff_alpha,
            }
            for c in result.cases
        ],
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print("Inter-rater reliability analysis")
    print("=" * 40)
    print(f"Study: {result.study_id}")
    print(f"Overall Cohen's Kappa: {result.overall_kappa} ({result.overall_kappa_label})")
    print(f"Overall Krippendorff's Alpha: {result.overall_alpha} ({result.overall_alpha_label})")
    for case in result.cases:
        print(
            f"  {case.case_id}: κ={case.cohens_kappa}, α={case.krippendorff_alpha}, "
            f"disagreements={case.disagreement_count}"
        )
    print(f"JSON: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
