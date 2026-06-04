#!/usr/bin/env python3
"""
Fill GRB assessor template with SYNTHETIC demo scores — workflow walkthrough only.

WARNING: Do not use for real municipal assessments or empirical claims.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.workflows.demo_scores import SYNTHETIC_DEMO_BANNER, fill_demo_scores_file

DEFAULT_INPUT = ROOT / "outputs" / "demo_municipality" / "assessor_scoring_template.yaml"
DEFAULT_OUTPUT = ROOT / "outputs" / "demo_municipality" / "assessor_scoring_completed.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fill assessor template with SYNTHETIC demo scores (not for real use).",
        epilog=SYNTHETIC_DEMO_BANNER,
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Scoring template YAML")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Completed scores YAML")
    parser.add_argument(
        "--evidence-log",
        type=Path,
        default=None,
        help="Optional evidence_log.yaml (default: alongside input file)",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        print("Run assessment workflow prepare phase first.", file=sys.stderr)
        return 1

    completed = fill_demo_scores_file(
        input_path,
        args.output.resolve(),
        evidence_log_path=args.evidence_log.resolve() if args.evidence_log else None,
    )
    scores = completed["responses"]
    values = list(scores.values())
    print("SYNTHETIC DEMO SCORE FILL — NOT FOR REAL ASSESSMENTS")
    print("=" * 50)
    print(SYNTHETIC_DEMO_BANNER)
    print(f"Input:  {input_path}")
    print(f"Output: {args.output.resolve()}")
    print(f"Indicators filled: {len(scores)}")
    print(f"Score range: {min(values)}–{max(values)} (deterministic, centred on ~3)")
    if completed.get("evidence_refs"):
        n_refs = sum(len(v) for v in completed["evidence_refs"].values())
        print(f"Evidence refs attached: {n_refs} (for scores >= 3)")
    print("Next: run assessment workflow with --compute-score and --scores pointing to output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
