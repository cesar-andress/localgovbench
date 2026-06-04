#!/usr/bin/env python3
"""Extraction stability benchmark — repeated runs per task per model."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.extraction_stability import (
    DEFAULT_BASE_SEED,
    DEFAULT_RUNS_PER_TASK,
    run_full_stability_study,
    write_stability_outputs,
)
from localgovbench.llm.model_benchmark import BENCHMARK_MODELS, DEFAULT_TASKS_PATH


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run each evidence extraction task N times per model and measure "
            "quote, evidence, and confidence stability."
        )
    )
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS_PATH)
    parser.add_argument("--models", nargs="*", default=list(BENCHMARK_MODELS))
    parser.add_argument(
        "--runs",
        type=int,
        default=DEFAULT_RUNS_PER_TASK,
        help=f"Runs per task (default {DEFAULT_RUNS_PER_TASK})",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_BASE_SEED)
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Deterministic mock with run-indexed variation (no Ollama)",
    )
    parser.add_argument(
        "--no-save-runs",
        action="store_true",
        help="Skip JSON run archives under results/extraction_stability_runs/",
    )
    parser.add_argument(
        "--fail-on-skip",
        action="store_true",
        help="Exit 1 if any live model is unavailable",
    )
    args = parser.parse_args()

    if args.runs < 1:
        print("error: --runs must be >= 1", file=sys.stderr)
        return 2

    runs, task_summaries, model_summaries, runs_dir = run_full_stability_study(
        models=tuple(args.models),
        tasks_path=args.tasks,
        repo_root=ROOT,
        n_runs=args.runs,
        base_seed=args.seed,
        base_url=args.base_url,
        mock=args.mock,
        skip_unavailable=not args.fail_on_skip,
        save_runs=not args.no_save_runs,
    )
    csv_path, report_path, _ = write_stability_outputs(
        runs,
        task_summaries,
        model_summaries,
        n_runs=args.runs,
        base_seed=args.seed,
        mock=args.mock,
        tasks_path=args.tasks.relative_to(ROOT),
        repo_root=ROOT,
    )

    print("Extraction stability benchmark")
    print("=" * 40)
    print(f"Mode: {'mock' if args.mock else 'live'}")
    print(f"Runs per task: {args.runs}")
    print(f"Total extractions: {len(runs)}")
    if args.mock:
        print("WARNING: Mock mode — not empirical Ollama stability.")
    print(f"Run archives: {runs_dir}")
    print(f"CSV: {csv_path}")
    print(f"Report: {report_path}")
    for row in model_summaries:
        if row.get("status") == "model_not_available":
            print(f"  {row['model']}: unavailable")
            continue
        print(
            f"  {row['model']}: overall={row.get('overall_stability')} "
            f"({row.get('variability_label')}) "
            f"quote={row.get('mean_quote_stability')} "
            f"evidence={row.get('mean_evidence_stability')} "
            f"confidence={row.get('mean_confidence_stability')}"
        )

    if args.fail_on_skip and any(r.get("status") == "model_not_available" for r in model_summaries):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
