#!/usr/bin/env python3
"""Repeated LocalGovBench LLM evidence extraction benchmark (N runs per model, shuffled task order)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.model_benchmark import BENCHMARK_MODELS, DEFAULT_TASKS_PATH
from localgovbench.llm.repeated_benchmark import (
    run_full_repeated_benchmark,
    write_repeated_benchmark_outputs,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run each Ollama model N times on evidence extraction tasks with "
            "randomized task order per repetition."
        )
    )
    parser.add_argument(
        "--tasks",
        type=Path,
        default=DEFAULT_TASKS_PATH,
        help="Path to evidence_extraction_tasks.json",
    )
    parser.add_argument(
        "--models",
        nargs="*",
        default=list(BENCHMARK_MODELS),
        help="Ollama model names to benchmark",
    )
    parser.add_argument(
        "--repetitions",
        type=int,
        default=10,
        metavar="N",
        help="Number of repetitions per model (default: 10)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base RNG seed; repetition i uses seed + i",
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:11434",
        help="Ollama API base URL",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Deterministic mock extractions (no Ollama); for CI and tests",
    )
    parser.add_argument(
        "--no-save-runs",
        action="store_true",
        help="Skip writing individual run JSON files under results/repeated_runs/",
    )
    parser.add_argument(
        "--fail-on-skip",
        action="store_true",
        help="Exit with code 1 if any live model is unavailable",
    )
    args = parser.parse_args()

    if args.repetitions < 1:
        print("error: --repetitions must be >= 1", file=sys.stderr)
        return 2

    rows, runs_dir = run_full_repeated_benchmark(
        models=tuple(args.models),
        tasks_path=args.tasks,
        repo_root=ROOT,
        n_repetitions=args.repetitions,
        base_seed=args.seed,
        base_url=args.base_url,
        mock=args.mock,
        skip_unavailable=not args.fail_on_skip,
        save_runs=not args.no_save_runs,
    )
    csv_path, report_path, _ = write_repeated_benchmark_outputs(
        rows,
        n_repetitions=args.repetitions,
        base_seed=args.seed,
        mock=args.mock,
        tasks_path=args.tasks.relative_to(ROOT),
        repo_root=ROOT,
    )

    print("LocalGovBench repeated LLM model benchmark")
    print("=" * 40)
    print(f"Mode: {'mock' if args.mock else 'live'}")
    print(f"Repetitions per model: {args.repetitions}")
    print(f"Base seed: {args.seed}")
    if args.mock:
        print("WARNING: Mock mode — not empirical Ollama results.")
    print(f"Individual runs: {runs_dir}")
    print(f"Summary CSV: {csv_path}")
    print(f"Report: {report_path}")
    for row in rows:
        if row.get("status") == "model_not_available":
            print(f"  {row['model']}: unavailable")
            continue
        print(
            f"  {row['model']}: precision={row.get('mean_evidence_precision')} "
            f"± {row.get('std_evidence_precision')} "
            f"CI95=[{row.get('ci95_evidence_precision_low')}, {row.get('ci95_evidence_precision_high')}]"
        )

    if args.fail_on_skip and any(r.get("status") == "model_not_available" for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
