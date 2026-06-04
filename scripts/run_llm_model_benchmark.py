#!/usr/bin/env python3
"""Benchmark local Ollama models on LocalGovBench evidence extraction tasks."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    CSV_FIELDNAMES,
    DEFAULT_TASKS_PATH,
    render_model_benchmark_report,
    run_full_benchmark,
)

CSV_PATH = ROOT / "results" / "model_benchmark.csv"
REPORT_PATH = ROOT / "reports" / "model_benchmark.md"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in CSV_FIELDNAMES})


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
        help="Deterministic mock extractions (no Ollama required)",
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
    write_csv(CSV_PATH, rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        render_model_benchmark_report(rows, tasks_path=args.tasks.relative_to(ROOT)),
        encoding="utf-8",
    )

    print("LocalGovBench LLM model benchmark")
    print("=" * 40)
    print(f"Mode: {'mock' if args.mock else 'live'}")
    print(f"Tasks: {rows[0]['n_tasks'] if rows else 0} per model")
    print(f"CSV: {CSV_PATH}")
    print(f"Report: {REPORT_PATH}")
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
