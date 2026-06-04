"""Tests for extraction stability benchmark (mock)."""

from __future__ import annotations

import json
from pathlib import Path

from localgovbench.llm.extraction_stability import (
    DEFAULT_RUNS_PER_TASK,
    StabilityMockRunner,
    field_stability,
    normalize_text,
    run_full_stability_study,
    run_task_stability,
    summarize_task_runs,
    write_stability_outputs,
)
from localgovbench.llm.model_benchmark import load_benchmark_tasks

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = REPO_ROOT / "data" / "benchmark" / "evidence_extraction_tasks.json"


def test_field_stability_identical() -> None:
    stab, unique = field_stability(["Hello", "hello", "  Hello  "])
    assert stab == 1.0
    assert unique == 1


def test_field_stability_split() -> None:
    stab, unique = field_stability(["a", "b", "a", "a"])
    assert abs(stab - 0.75) < 1e-9
    assert unique == 2


def test_mock_runner_varies_across_runs() -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    runner = StabilityMockRunner("phi3", base_seed=42)
    runs = run_task_stability("phi3", tasks[0], runner, n_runs=10)
    summary = summarize_task_runs(runs)
    assert summary.n_runs == 10
    assert summary.quote_stability < 1.0 or summary.evidence_stability < 1.0


def test_run_full_stability_study_mock(tmp_path: Path) -> None:
    runs, task_summaries, model_summaries, _ = run_full_stability_study(
        models=("phi3",),
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        n_runs=5,
        base_seed=7,
        mock=True,
        save_runs=False,
    )
    assert len(runs) == 5 * 15
    assert len(task_summaries) == 15
    assert len(model_summaries) == 1
    assert model_summaries[0]["overall_stability"] > 0


def test_write_outputs_and_default_runs(tmp_path: Path) -> None:
    runs, task_summaries, model_summaries, _ = run_full_stability_study(
        models=("llama3.1:8b",),
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        n_runs=3,
        mock=True,
        save_runs=False,
    )
    import localgovbench.llm.extraction_stability as mod

    csv_path = tmp_path / "results" / mod.STABILITY_CSV_NAME
    report_path = tmp_path / "reports" / mod.STABILITY_REPORT_NAME
    mod.stability_output_paths = lambda root=None: (csv_path, report_path, tmp_path / "runs")
    write_stability_outputs(
        runs,
        task_summaries,
        model_summaries,
        n_runs=3,
        base_seed=1,
        mock=True,
        tasks_path=TASKS_PATH,
        repo_root=tmp_path,
    )
    assert csv_path.is_file()
    assert report_path.is_file()
    assert "Extraction stability" in report_path.read_text(encoding="utf-8")


def test_default_runs_per_task_is_twenty() -> None:
    assert DEFAULT_RUNS_PER_TASK == 20
