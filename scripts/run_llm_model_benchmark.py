#!/usr/bin/env python3
"""Benchmark local Ollama models on LocalGovBench evidence extraction tasks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    DEFAULT_TASKS_PATH,
    benchmark_output_paths,
    run_full_benchmark,
    write_benchmark_outputs,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare Ollama models on LocalGovBench evidence extraction."
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
        "--base-url",
        default="http://127.0.0.1:11434",
        help="Ollama API base URL",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Deterministic mock extractions (no Ollama); writes *_mock.* outputs only",
    )
    parser.add_argument(
        "--fail-on-skip",
        action="store_true",
        help="Exit with code 1 if any live model is unavailable",
    )
    args = parser.parse_args()

    rows = run_full_benchmark(
        models=tuple(args.models),
        tasks_path=args.tasks,
        repo_root=ROOT,
        base_url=args.base_url,
        mock=args.mock,
        skip_unavailable=not args.fail_on_skip,
    )
    csv_path, report_path = write_benchmark_outputs(
        rows,
        mock=args.mock,
        tasks_path=args.tasks.relative_to(ROOT),
        repo_root=ROOT,
    )

    print("LocalGovBench LLM model benchmark")
    print("=" * 40)
    print(f"Mode: {'mock' if args.mock else 'live'}")
    if args.mock:
        print("WARNING: Mock outputs are for testing only — not empirical model results.")
    print(f"Tasks: {rows[0]['n_tasks'] if rows else 0} per model")
    print(f"CSV: {csv_path}")
    print(f"Report: {report_path}")
    for row in rows:
        print(
            f"  {row['model']}: precision={row['evidence_precision']:.4f} "
            f"hallucination={row['hallucinated_evidence_rate']:.4f} "
            f"status={row['status']}"
        )

    if args.fail_on_skip and any(r["status"] == "model_not_available" for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
