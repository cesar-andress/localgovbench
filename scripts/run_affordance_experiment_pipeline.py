#!/usr/bin/env python3
"""Run the Phase 3 schema-affordance experiment pipeline.

Does not calculate realization, affordance–realization gaps, or IRR.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from localgovbench_measurement_validation.affordance.experiments.import_coding import (
    CodingImportError,
)
from localgovbench_measurement_validation.affordance.experiments.pipeline import (
    run_affordance_experiment,
    run_single_coder_matrix,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 3 schema-affordance experiment pipeline"
    )
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--operator", default="local")
    parser.add_argument("--output-root", type=Path, default=None)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Do not require full 55-unit coverage (e.g. pilot subsets).",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--single-coder",
        type=Path,
        help="Path to a single completed coding CSV/JSON",
    )
    mode.add_argument(
        "--coder-a",
        type=Path,
        help="Coder A completed coding file (use with --coder-b)",
    )
    parser.add_argument("--coder-b", type=Path, default=None)
    parser.add_argument("--adjudication", type=Path, default=None)
    args = parser.parse_args(argv)

    require_complete = not args.allow_partial
    try:
        if args.single_coder:
            result = run_single_coder_matrix(
                experiment_id=args.experiment_id,
                coding_path=args.single_coder,
                operator=args.operator,
                require_complete=require_complete,
                output_root=args.output_root,
            )
        else:
            if args.coder_b is None:
                parser.error("--coder-b is required with --coder-a")
            result = run_affordance_experiment(
                experiment_id=args.experiment_id,
                coder_a=args.coder_a,
                coder_b=args.coder_b,
                adjudication=args.adjudication,
                operator=args.operator,
                require_complete=require_complete,
                output_root=args.output_root,
            )
    except CodingImportError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
