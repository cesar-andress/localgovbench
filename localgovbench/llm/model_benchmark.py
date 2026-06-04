"""Compare Ollama models on LocalGovBench evidence extraction tasks."""

from __future__ import annotations

import csv
import hashlib
import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Protocol

from localgovbench.llm.benchmark_metrics import (
    TaskEvaluation,
    TaskGold,
    aggregate_metrics,
    evaluate_task,
    quote_is_verbatim,
)
from localgovbench.llm.evidence_extraction import (
    DEFAULT_OLLAMA_BASE_URL,
    EvidenceExtractionResult,
    OllamaClient,
    extract_evidence,
)

BENCHMARK_MODELS = (
    "llama3.1:8b",
    "qwen2.5:7b",
    "mistral:7b",
    "gemma2:9b",
    "phi3",
)

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_TASKS_PATH = REPO_ROOT / "data" / "benchmark" / "evidence_extraction_tasks.json"

MOCK_CSV_NAME = "model_benchmark_mock.csv"
MOCK_REPORT_NAME = "model_benchmark_mock.md"
LIVE_CSV_NAME = "model_benchmark_live.csv"
LIVE_REPORT_NAME = "model_benchmark_live.md"
LEGACY_CSV_NAME = "model_benchmark.csv"
LEGACY_REPORT_NAME = "model_benchmark.md"


def legacy_benchmark_output_paths(repo_root: Path | None = None) -> tuple[Path, Path]:
    """Deprecated generic paths — must not be written by the benchmark CLI."""
    root = repo_root or REPO_ROOT
    return (
        root / "results" / LEGACY_CSV_NAME,
        root / "reports" / LEGACY_REPORT_NAME,
    )


def remove_legacy_benchmark_outputs(repo_root: Path | None = None) -> list[Path]:
    """Remove legacy generic benchmark files if present (avoid manuscript confusion)."""
    removed: list[Path] = []
    for path in legacy_benchmark_output_paths(repo_root):
        if path.is_file():
            path.unlink()
            removed.append(path)
    return removed


def benchmark_output_paths(*, mock: bool, repo_root: Path | None = None) -> tuple[Path, Path]:
    """Return (csv_path, report_path) for mock or live benchmark runs."""
    root = repo_root or REPO_ROOT
    if mock:
        return (
            root / "results" / MOCK_CSV_NAME,
            root / "reports" / MOCK_REPORT_NAME,
        )
    return (
        root / "results" / LIVE_CSV_NAME,
        root / "reports" / LIVE_REPORT_NAME,
    )

CSV_FIELDNAMES = (
    "model",
    "n_tasks",
    "n_success",
    "evidence_precision",
    "quote_validity_rate",
    "hallucinated_evidence_rate",
    "insufficient_evidence_detection_rate",
    "mean_latency_seconds",
    "p95_latency_seconds",
    "memory_footprint_mb",
    "status",
    "mode",
)


class ExtractionRunner(Protocol):
    model: str

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
    ) -> tuple[EvidenceExtractionResult, float]:
        ...


@dataclass(frozen=True, slots=True)
class BenchmarkTask:
    gold: TaskGold
    document_text: str


def load_benchmark_tasks(
    tasks_path: Path,
    *,
    repo_root: Path,
) -> list[BenchmarkTask]:
    payload = json.loads(tasks_path.read_text(encoding="utf-8"))
    tasks: list[BenchmarkTask] = []
    for raw in payload["tasks"]:
        gold = TaskGold(
            task_id=raw["task_id"],
            document_path=raw["document"],
            indicator_id=raw["indicator_id"],
            gold_has_evidence=bool(raw["gold_has_evidence"]),
            gold_keywords=list(raw.get("gold_keywords", [])),
            gold_expect_insufficient=bool(raw["gold_expect_insufficient"]),
        )
        doc_path = repo_root / gold.document_path
        if not doc_path.is_file():
            raise FileNotFoundError(f"Benchmark document missing: {doc_path}")
        tasks.append(
            BenchmarkTask(
                gold=gold,
                document_text=doc_path.read_text(encoding="utf-8"),
            )
        )
    return tasks


def list_ollama_models(base_url: str = DEFAULT_OLLAMA_BASE_URL) -> set[str]:
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/api/tags", timeout=5) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return set()
    names: set[str] = set()
    for entry in body.get("models", []):
        name = entry.get("name") or entry.get("model")
        if name:
            names.add(str(name))
            if ":" not in str(name) and entry.get("name"):
                names.add(f"{name}:latest")
    return names


def fetch_model_memory_mb(
    model: str,
    *,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
) -> float | None:
    """Return VRAM usage (MiB) for a loaded model from Ollama ``/api/ps``."""
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/api/ps", timeout=5) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
        return None

    model_base = model.split(":")[0]
    best: float | None = None
    for entry in body.get("models", []):
        name = str(entry.get("name", ""))
        if name == model or name.startswith(f"{model_base}:") or model.startswith(name.split(":")[0]):
            vram = entry.get("size_vram") or entry.get("size")
            if vram is not None:
                mib = float(vram) / (1024 * 1024)
                best = mib if best is None else max(best, mib)
    return round(best, 1) if best is not None else None


def _deterministic_rate(model: str, metric: str, default: float) -> float:
    digest = hashlib.sha256(f"{model}:{metric}".encode()).hexdigest()
    bucket = int(digest[:8], 16) % 1000
    return default + (bucket - 500) / 5000.0


class LiveExtractionRunner:
    def __init__(
        self,
        model: str,
        *,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.model = model
        self._client = OllamaClient(
            base_url=base_url,
            model=model,
            timeout_seconds=timeout_seconds,
        )

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
    ) -> tuple[EvidenceExtractionResult, float]:
        del gold
        start = time.perf_counter()
        result = extract_evidence(document_text, indicator_id, client=self._client)
        return result, time.perf_counter() - start


class MockExtractionRunner:
    """Deterministic pseudo-extractions for reproducible reports without Ollama."""

    def __init__(self, model: str) -> None:
        self.model = model

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
    ) -> tuple[EvidenceExtractionResult, float]:
        seed = int(hashlib.sha256(f"{self.model}:{gold.task_id}".encode()).hexdigest()[:8], 16)
        start = time.perf_counter()
        time.sleep(0.001)

        halluc_bias = _deterministic_rate(self.model, "hallucination", 0.08)
        miss_bias = _deterministic_rate(self.model, "insufficient_miss", 0.12)
        bucket = seed % 1000
        hallucinate = gold.gold_has_evidence and bucket < int(halluc_bias * 1000)
        miss_insufficient = gold.gold_expect_insufficient and bucket < int(miss_bias * 1000)

        if gold.gold_has_evidence and not hallucinate:
            quote = _find_gold_quote(document_text, gold.gold_keywords) or gold.gold_keywords[0]
            result = EvidenceExtractionResult(
                indicator_id=indicator_id,
                candidate_evidence=f"Document addresses {gold.indicator_id}.",
                confidence_level="high",
                quoted_text_span=quote,
                insufficient_evidence_warning=None,
                model=self.model,
            )
        elif hallucinate:
            result = EvidenceExtractionResult(
                indicator_id=indicator_id,
                candidate_evidence="Fabricated governance control cited.",
                confidence_level="medium",
                quoted_text_span="This sentence does not appear in the municipal document.",
                insufficient_evidence_warning=None,
                model=self.model,
            )
        else:
            warning = None if miss_insufficient else (
                "Insufficient documentary evidence: add primary sources or "
                "clarify governance controls before scoring."
            )
            result = EvidenceExtractionResult(
                indicator_id=indicator_id,
                candidate_evidence="No explicit evidence identified.",
                confidence_level="low",
                quoted_text_span="",
                insufficient_evidence_warning=warning,
                model=self.model,
            )

        latency = 0.05 + (seed % 50) / 1000.0
        return result, time.perf_counter() - start + latency


def _find_gold_quote(document_text: str, keywords: list[str]) -> str | None:
    for keyword in keywords:
        idx = document_text.lower().find(keyword.lower())
        if idx >= 0:
            start = max(0, idx - 20)
            end = min(len(document_text), idx + len(keyword) + 40)
            snippet = document_text[start:end].strip()
            if quote_is_verbatim(snippet, document_text):
                return snippet
            if quote_is_verbatim(keyword, document_text):
                return keyword
    return None


def run_model_benchmark(
    model: str,
    tasks: list[BenchmarkTask],
    runner: ExtractionRunner,
) -> tuple[list[TaskEvaluation], dict[str, Any]]:
    evaluations: list[TaskEvaluation] = []
    for task in tasks:
        try:
            result, latency = runner.run(
                task.document_text,
                task.gold.indicator_id,
                gold=task.gold,
            )
            evaluation = evaluate_task(result, gold=task.gold, document_text=task.document_text)
            evaluation = replace(evaluation, latency_seconds=latency)
        except (ConnectionError, RuntimeError, ValueError, OSError) as exc:
            evaluation = TaskEvaluation(
                task_id=task.gold.task_id,
                indicator_id=task.gold.indicator_id,
                claims_evidence=False,
                quote_valid=False,
                hallucinated=False,
                precision_hit=False,
                insufficient_detected=False,
                gold_expect_insufficient=task.gold.gold_expect_insufficient,
                latency_seconds=0.0,
                error=str(exc),
            )
        evaluations.append(evaluation)

    metrics = aggregate_metrics(evaluations)
    return evaluations, metrics


def run_full_benchmark(
    *,
    models: tuple[str, ...] = BENCHMARK_MODELS,
    tasks_path: Path = DEFAULT_TASKS_PATH,
    repo_root: Path | None = None,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    mock: bool = False,
    skip_unavailable: bool = True,
) -> list[dict[str, Any]]:
    root = repo_root or tasks_path.resolve().parents[2]
    tasks = load_benchmark_tasks(tasks_path, repo_root=root)
    available = list_ollama_models(base_url) if not mock else set(models)
    rows: list[dict[str, Any]] = []

    def _model_available(name: str) -> bool:
        if name in available:
            return True
        base = name.split(":")[0]
        return any(tag == name or tag.startswith(f"{base}:") for tag in available)

    for model in models:
        if not mock and skip_unavailable and not _model_available(model):
            rows.append(
                {
                    "model": model,
                    "n_tasks": len(tasks),
                    "n_success": 0,
                    "evidence_precision": 0.0,
                    "quote_validity_rate": 0.0,
                    "hallucinated_evidence_rate": 0.0,
                    "insufficient_evidence_detection_rate": 0.0,
                    "mean_latency_seconds": 0.0,
                    "p95_latency_seconds": 0.0,
                    "memory_footprint_mb": "",
                    "status": "model_not_available",
                    "mode": "live",
                }
            )
            continue

        runner: ExtractionRunner = (
            MockExtractionRunner(model) if mock else LiveExtractionRunner(model, base_url=base_url)
        )
        _, metrics = run_model_benchmark(model, tasks, runner)
        memory_mb = None if mock else fetch_model_memory_mb(model, base_url=base_url)
        rows.append(
            {
                "model": model,
                **metrics,
                "memory_footprint_mb": memory_mb if memory_mb is not None else "",
                "status": "ok" if metrics["n_success"] == metrics["n_tasks"] else "partial",
                "mode": "mock" if mock else "live",
            }
        )
    return rows


def render_model_benchmark_report(
    rows: list[dict[str, Any]],
    *,
    tasks_path: Path,
    mock: bool,
    csv_path: Path | None = None,
    report_path: Path | None = None,
) -> str:
    mode = "mock" if mock else "live"
    csv_path = csv_path or benchmark_output_paths(mock=mock)[0]
    report_path = report_path or benchmark_output_paths(mock=mock)[1]

    if mock:
        mode_banner = (
            "> **GENERATION MODE: MOCK (testing only)** — Deterministic pseudo-extractions "
            "without Ollama. **Do not report these metrics as empirical model comparison results.**"
        )
    else:
        mode_banner = (
            "> **GENERATION MODE: LIVE** — Metrics from local Ollama inference on gold-labelled "
            "synthetic tasks. Suitable for reporting when models were actually run."
        )

    lines = [
        "# LocalGovBench LLM evidence extraction benchmark",
        "",
        mode_banner,
        "",
        "> Compares local **Ollama** models on GRB evidence extraction tasks with synthetic gold labels.",
        "",
        f"**Generation mode:** `{mode}` (this file: `{report_path.name}`)",
        f"**Results CSV:** `{csv_path}`",
        f"**Tasks:** `{tasks_path}`",
        "",
        "## Models",
        "",
        "| Model | Evidence precision | Quote validity | Hallucination rate | Insufficient detection | Mean latency (s) | P95 latency (s) | Memory (MiB) | Status |",
        "|-------|-------------------:|---------------:|-------------------:|-----------------------:|-----------------:|----------------:|-------------:|--------|",
    ]
    for row in rows:
        mem = row.get("memory_footprint_mb", "")
        mem_display = mem if mem != "" else "—"
        lines.append(
            f"| `{row['model']}` | {row['evidence_precision']:.4f} | {row['quote_validity_rate']:.4f} | "
            f"{row['hallucinated_evidence_rate']:.4f} | {row['insufficient_evidence_detection_rate']:.4f} | "
            f"{row['mean_latency_seconds']:.3f} | {row['p95_latency_seconds']:.3f} | {mem_display} | {row['status']} |"
        )

    lines.extend(
        [
            "",
            "## Metric definitions",
            "",
            "| Metric | Definition |",
            "|--------|------------|",
            "| Evidence precision | Share of tasks where positive/negative evidence claims align with gold labels and valid quotes |",
            "| Quote validity | Valid verbatim quotes / quotes emitted when claiming evidence |",
            "| Hallucinated evidence rate | Tasks with non-verbatim quotes among all tasks |",
            "| Insufficient evidence detection | Recall of gold insufficient tasks flagged via warning or low confidence |",
            "| Latency | Wall-clock seconds per extraction (mean and P95) |",
            "| Memory footprint | Ollama reported VRAM (`/api/ps`) after model run, MiB |",
            "",
            "## Reproduce",
            "",
            "Live (Ollama required):",
            "",
            "```bash",
            "ollama serve",
            "ollama pull llama3.1:8b",
            "python scripts/run_llm_model_benchmark.py",
            "# writes results/model_benchmark_live.csv and reports/model_benchmark_live.md",
            "```",
            "",
            "Mock (testing only, no Ollama):",
            "",
            "```bash",
            "python scripts/run_llm_model_benchmark.py --mock",
            "# writes results/model_benchmark_mock.csv and reports/model_benchmark_mock.md",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_benchmark_outputs(
    rows: list[dict[str, Any]],
    *,
    mock: bool,
    tasks_path: Path,
    repo_root: Path | None = None,
) -> tuple[Path, Path]:
    """Write CSV and Markdown report to mode-specific paths only."""
    root = repo_root or REPO_ROOT
    remove_legacy_benchmark_outputs(root)

    csv_path, report_path = benchmark_output_paths(mock=mock, repo_root=root)
    legacy_csv, legacy_report = legacy_benchmark_output_paths(root)
    if csv_path.name in (LEGACY_CSV_NAME, LEGACY_REPORT_NAME) or report_path.name in (
        LEGACY_CSV_NAME,
        LEGACY_REPORT_NAME,
    ):
        raise ValueError("Benchmark must not write legacy generic output filenames.")
    assert csv_path != legacy_csv and report_path != legacy_report

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in CSV_FIELDNAMES})

    root = repo_root or REPO_ROOT
    try:
        csv_display = csv_path.relative_to(root)
        report_display = report_path.relative_to(root)
    except ValueError:
        csv_display = csv_path
        report_display = report_path

    report_path.write_text(
        render_model_benchmark_report(
            rows,
            tasks_path=tasks_path,
            mock=mock,
            csv_path=csv_display,
            report_path=report_display,
        ),
        encoding="utf-8",
    )
    return csv_path, report_path
