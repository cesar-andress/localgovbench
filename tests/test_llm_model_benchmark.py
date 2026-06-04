"""Unit tests for LLM evidence extraction benchmark (no live Ollama)."""

from __future__ import annotations

import json

from localgovbench.llm.benchmark_metrics import (
    TaskGold,
    claims_evidence,
    evaluate_task,
    quote_is_verbatim,
)
from localgovbench.llm.evidence_extraction import (
    EvidenceExtractionResult,
    parse_extraction_response,
)
from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    LIVE_CSV_NAME,
    LIVE_REPORT_NAME,
    MOCK_CSV_NAME,
    MOCK_REPORT_NAME,
    MockExtractionRunner,
    benchmark_output_paths,
    load_benchmark_tasks,
    render_model_benchmark_report,
    run_full_benchmark,
    run_model_benchmark,
    write_benchmark_outputs,
)
from tests.conftest import MockOllamaClient

VALID_RESPONSE = json.dumps(
    {
        "candidate_evidence": "Policy requires named policy officer review of LLM drafts.",
        "confidence_level": "high",
        "quoted_text_span": "requires review by a named policy officer",
        "insufficient_evidence_warning": None,
    }
)

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = REPO_ROOT / "data" / "benchmark" / "evidence_extraction_tasks.json"


def test_quote_verbatim_substring() -> None:
    doc = "Section 4.2 requires review by a named policy officer."
    assert quote_is_verbatim("named policy officer", doc)
    assert not quote_is_verbatim("nonexistent clause", doc)


def test_evaluate_precision_positive() -> None:
    result = parse_extraction_response(
        VALID_RESPONSE,
        indicator_id="d2_oversight_design_01",
        model="test",
    )
    gold = TaskGold(
        task_id="t1",
        document_path="x.md",
        indicator_id="d2_oversight_design_01",
        gold_has_evidence=True,
        gold_keywords=["policy officer"],
        gold_expect_insufficient=False,
    )
    doc = "Section 4.2 requires review by a named policy officer."
    evaluation = evaluate_task(result, gold=gold, document_text=doc)
    assert evaluation.precision_hit
    assert evaluation.quote_valid
    assert not evaluation.hallucinated


def test_load_benchmark_tasks() -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    assert len(tasks) >= 10
    assert tasks[0].document_text


def test_benchmark_output_paths_distinct() -> None:
    mock_csv, mock_report = benchmark_output_paths(mock=True, repo_root=REPO_ROOT)
    live_csv, live_report = benchmark_output_paths(mock=False, repo_root=REPO_ROOT)
    assert mock_csv.name == MOCK_CSV_NAME
    assert mock_report.name == MOCK_REPORT_NAME
    assert live_csv.name == LIVE_CSV_NAME
    assert live_report.name == LIVE_REPORT_NAME
    assert mock_csv != live_csv
    assert mock_report != live_report
    assert "mock" in mock_csv.name and "live" not in mock_csv.name
    assert "live" in live_csv.name and "mock" not in live_csv.name


def test_write_benchmark_outputs_uses_mode_specific_paths(tmp_path: Path) -> None:
    rows = run_full_benchmark(
        models=("llama3.1:8b",),
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        mock=True,
    )
    csv_path, report_path = write_benchmark_outputs(
        rows,
        mock=True,
        tasks_path=Path("data/benchmark/evidence_extraction_tasks.json"),
        repo_root=tmp_path,
    )
    assert csv_path == tmp_path / "results" / MOCK_CSV_NAME
    assert report_path == tmp_path / "reports" / MOCK_REPORT_NAME
    assert csv_path.is_file()
    assert report_path.is_file()
    text = report_path.read_text(encoding="utf-8")
    assert "MOCK (testing only)" in text
    assert "mock" in text.lower()

    live_csv, live_report = benchmark_output_paths(mock=False, repo_root=tmp_path)
    assert not live_csv.exists()
    assert not live_report.exists()


def test_render_report_live_mode_banner() -> None:
    rows = [{"model": "m", "mode": "live", "evidence_precision": 0.5, "quote_validity_rate": 1.0,
             "hallucinated_evidence_rate": 0.0, "insufficient_evidence_detection_rate": 1.0,
             "mean_latency_seconds": 1.0, "p95_latency_seconds": 1.0, "memory_footprint_mb": "",
             "status": "ok"}]
    text = render_model_benchmark_report(rows, tasks_path=Path("tasks.json"), mock=False)
    assert "GENERATION MODE: LIVE" in text
    assert "MOCK (testing only)" not in text


def test_mock_benchmark_all_models() -> None:
    rows = run_full_benchmark(
        models=BENCHMARK_MODELS,
        tasks_path=TASKS_PATH,
        repo_root=REPO_ROOT,
        mock=True,
    )
    assert len(rows) == len(BENCHMARK_MODELS)
    for row in rows:
        assert row["status"] == "ok"
        assert row["n_tasks"] == 15
        assert 0.0 <= row["evidence_precision"] <= 1.0


def test_run_model_benchmark_with_mock_client() -> None:
    tasks = load_benchmark_tasks(TASKS_PATH, repo_root=REPO_ROOT)
    client = MockOllamaClient(VALID_RESPONSE)

    class ClientRunner:
        model = "mock"

        def run(self, document_text: str, indicator_id: str, *, gold: TaskGold):
            from localgovbench.llm.evidence_extraction import extract_evidence

            import time

            start = time.perf_counter()
            result = extract_evidence(document_text, indicator_id, client=client)
            return result, time.perf_counter() - start

    evaluations, metrics = run_model_benchmark("mock", tasks, ClientRunner())
    assert len(evaluations) == len(tasks)
    assert metrics["n_success"] == len(tasks)
    assert 0.0 <= metrics["evidence_precision"] <= 1.0


def test_hallucination_detected() -> None:
    result = EvidenceExtractionResult(
        indicator_id="d2_oversight_design_01",
        candidate_evidence="Claim",
        confidence_level="medium",
        quoted_text_span="text not in document",
        insufficient_evidence_warning=None,
        model="m",
    )
    gold = TaskGold(
        task_id="t",
        document_path="d.md",
        indicator_id="d2_oversight_design_01",
        gold_has_evidence=True,
        gold_keywords=["policy officer"],
        gold_expect_insufficient=False,
    )
    evaluation = evaluate_task(result, gold=gold, document_text="only real text here")
    assert evaluation.hallucinated
    assert not evaluation.precision_hit


def test_insufficient_detection() -> None:
    raw = json.dumps(
        {
            "candidate_evidence": "",
            "confidence_level": "low",
            "quoted_text_span": "",
            "insufficient_evidence_warning": "Weak evidence",
        }
    )
    result = parse_extraction_response(raw, indicator_id="d1_mandate_01", model="m")
    assert claims_evidence(result) is False
    gold = TaskGold(
        task_id="t",
        document_path="d.md",
        indicator_id="d1_mandate_01",
        gold_has_evidence=False,
        gold_keywords=[],
        gold_expect_insufficient=True,
    )
    evaluation = evaluate_task(result, gold=gold, document_text="short doc")
    assert evaluation.insufficient_detected
