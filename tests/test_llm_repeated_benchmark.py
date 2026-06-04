"""Tests for repeated LLM evidence extraction benchmark (mock only)."""

from __future__ import annotations

import json
from pathlib import Path

from localgovbench.llm.model_benchmark import BENCHMARK_MODELS, load_benchmark_tasks
from localgovbench.llm.repeated_benchmark import (
    REPEATED_CSV_NAME,
    REPEATED_REPORT_NAME,
    aggregate_repeated_runs,
    mean_std_ci95,
    repeated_output_paths,
    run_full_repeated_benchmark,
    run_repeated_benchmark_for_model,
    shuffle_tasks,
    t_critical_975,
    write_repeated_benchmark_outputs,
)
from localgovbench.llm.model_benchmark import MockExtractionRunner

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = REPO_ROOT / "data" / "benchmark" / "evidence_extraction_tasks.json"


def test_mean_std_ci95_single_value() -> None:
    stats = mean_std_ci95([0.4])
    assert stats["mean"] == 0.4
    assert stats["std"] == 0.0
    assert stats["ci95_low"] == 0.4
    assert stats["ci95_high"] == 0.4


def test_mean_std_ci95_two_values() -> None:
    stats = mean_std_ci95([0.2, 0.4])
    assert abs(stats["mean"] - 0.3) < 1e-9
    assert stats["std"] is not None and stats["std"] > 0
    assert stats["ci95_low"] is not None and stats["ci95_high"] is not None
    assert stats["ci95_low"] < stats["mean"] < stats["ci95_high"]


def test_shuffle_tasks_reproducible() -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    a = [t.gold.task_id for t in shuffle_tasks(tasks, 99)]
    b = [t.gold.task_id for t in shuffle_tasks(tasks, 99)]
    c = [t.gold.task_id for t in shuffle_tasks(tasks, 100)]
    assert a == b
    assert sorted(a) == sorted(c)
    assert a != c or len(a) <= 1


def test_run_repeated_benchmark_saves_individual_runs(tmp_path: Path) -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    runs_dir = tmp_path / "repeated_runs"
    records = run_repeated_benchmark_for_model(
        "phi3",
        tasks,
        n_repetitions=3,
        base_seed=7,
        runner=MockExtractionRunner("phi3"),
        runs_dir=runs_dir,
        save_runs=True,
    )
    assert len(records) == 3
    for i in range(3):
        path = runs_dir / "phi3" / f"run_{i:03d}.json"
        assert path.is_file()
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["run_index"] == i
        assert payload["seed"] == 7 + i
        assert len(payload["task_order"]) == len(tasks)
        assert "evidence_precision" in payload["metrics"]


def test_aggregate_repeated_runs_fields() -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    records = run_repeated_benchmark_for_model(
        "llama3.1:8b",
        tasks,
        n_repetitions=4,
        base_seed=1,
        runner=MockExtractionRunner("llama3.1:8b"),
        runs_dir=Path("/tmp/unused"),
        save_runs=False,
    )
    row = aggregate_repeated_runs(records)
    assert row["model"] == "llama3.1:8b"
    assert row["n_repetitions"] == 4
    assert "mean_evidence_precision" in row
    assert "std_evidence_precision" in row
    assert "ci95_evidence_precision_low" in row
    assert "ci95_hallucinated_evidence_rate_high" in row
    assert "mean_mean_latency_seconds" in row


def test_mock_full_repeated_benchmark(tmp_path: Path) -> None:
    rows, runs_dir = run_full_repeated_benchmark(
        models=("phi3", "gemma2:9b"),
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        n_repetitions=2,
        base_seed=42,
        mock=True,
        save_runs=True,
    )
    assert len(rows) == 2
    assert all(r["n_repetitions"] == 2 for r in rows)
    assert (runs_dir / "phi3" / "run_000.json").is_file()

    csv_path, report_path, _ = write_repeated_benchmark_outputs(
        rows,
        n_repetitions=2,
        base_seed=42,
        mock=True,
        tasks_path=Path("data/benchmark/evidence_extraction_tasks.json"),
        repo_root=tmp_path,
    )
    assert csv_path == tmp_path / "results" / REPEATED_CSV_NAME
    assert report_path == tmp_path / "reports" / REPEATED_REPORT_NAME
    assert "MOCK repeated benchmark" in report_path.read_text(encoding="utf-8")
    text = csv_path.read_text(encoding="utf-8")
    assert "mean_evidence_precision" in text
    assert "ci95_evidence_precision_low" in text


def test_repeated_output_paths() -> None:
    csv_path, report_path, runs_dir = repeated_output_paths(REPO_ROOT)
    assert csv_path.name == REPEATED_CSV_NAME
    assert report_path.name == REPEATED_REPORT_NAME
    assert runs_dir.name == "repeated_runs"


def test_t_critical_975_large_df() -> None:
    assert t_critical_975(30) == 1.96


def test_all_benchmark_models_mock_two_reps() -> None:
    rows, _ = run_full_repeated_benchmark(
        models=BENCHMARK_MODELS,
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        n_repetitions=2,
        base_seed=0,
        mock=True,
        save_runs=False,
    )
    assert len(rows) == len(BENCHMARK_MODELS)
    for row in rows:
        assert row["status"] in ("ok", "partial")
