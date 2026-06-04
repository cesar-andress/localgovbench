"""Extraction stability — repeated runs per task to measure output variability."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from statistics import mean
from typing import Any, Protocol

from localgovbench.llm.evidence_extraction import (
    DEFAULT_OLLAMA_BASE_URL,
    EvidenceExtractionResult,
)
from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    DEFAULT_TASKS_PATH,
    BenchmarkTask,
    LiveExtractionRunner,
    MockExtractionRunner,
    REPO_ROOT,
    TaskGold,
    _deterministic_rate,
    _find_gold_quote,
    list_ollama_models,
    load_benchmark_tasks,
)

DEFAULT_RUNS_PER_TASK = 20
DEFAULT_BASE_SEED = 42

STABILITY_CSV_NAME = "extraction_stability.csv"
STABILITY_REPORT_NAME = "extraction_stability.md"
STABILITY_RUNS_DIRNAME = "extraction_stability_runs"

CONFIDENCE_LEVELS: tuple[str, ...] = ("low", "medium", "high")


@dataclass(frozen=True, slots=True)
class ExtractionRun:
    """One extraction attempt for stability analysis."""

    model: str
    task_id: str
    indicator_id: str
    run_index: int
    candidate_evidence: str
    quoted_text_span: str
    confidence_level: str
    error: str | None = None


@dataclass(frozen=True, slots=True)
class TaskStabilitySummary:
    """Stability metrics for one model × task."""

    model: str
    task_id: str
    indicator_id: str
    n_runs: int
    n_success: int
    quote_stability: float
    evidence_stability: float
    confidence_stability: float
    unique_quotes: int
    unique_evidence: int
    unique_confidence: int


class StabilityRunner(Protocol):
    """Runner that may vary outputs across *run_index* (mock) or via sampling (live)."""

    model: str

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
        run_index: int,
    ) -> ExtractionRun:
        ...


def stability_output_paths(repo_root: Path | None = None) -> tuple[Path, Path, Path]:
    root = repo_root or REPO_ROOT
    return (
        root / "results" / STABILITY_CSV_NAME,
        root / "reports" / STABILITY_REPORT_NAME,
        root / "results" / STABILITY_RUNS_DIRNAME,
    )


def normalize_text(value: str) -> str:
    """Normalize text for stability comparison."""
    return " ".join(value.split()).casefold()


def field_stability(values: list[str]) -> tuple[float, int]:
    """
    Return (modal share, unique count) for normalized *values*.

    Stability is the fraction of runs matching the most frequent normalized value.
    """
    if not values:
        return 0.0, 0
    normed = [normalize_text(v) for v in values]
    counts = Counter(normed)
    mode_count = counts.most_common(1)[0][1]
    return mode_count / len(normed), len(counts)


def summarize_task_runs(runs: list[ExtractionRun]) -> TaskStabilitySummary:
    """Compute quote, evidence, and confidence stability for one task."""
    successful = [r for r in runs if r.error is None]
    quotes = [r.quoted_text_span for r in successful]
    evidence = [r.candidate_evidence for r in successful]
    confidence = [r.confidence_level for r in successful]

    quote_stab, unique_quotes = field_stability(quotes)
    evidence_stab, unique_evidence = field_stability(evidence)
    conf_stab, unique_confidence = field_stability(confidence)

    return TaskStabilitySummary(
        model=runs[0].model,
        task_id=runs[0].task_id,
        indicator_id=runs[0].indicator_id,
        n_runs=len(runs),
        n_success=len(successful),
        quote_stability=round(quote_stab, 4),
        evidence_stability=round(evidence_stab, 4),
        confidence_stability=round(conf_stab, 4),
        unique_quotes=unique_quotes,
        unique_evidence=unique_evidence,
        unique_confidence=unique_confidence,
    )


class StabilityLiveRunner:
    """Live Ollama extractions (stochasticity from model sampling)."""

    def __init__(
        self,
        model: str,
        *,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.model = model
        self._runner = LiveExtractionRunner(
            model,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
        )

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
        run_index: int,
    ) -> ExtractionRun:
        del run_index
        try:
            result, _ = self._runner.run(
                document_text,
                indicator_id,
                gold=gold,
            )
            return _result_to_run(result, gold.task_id, run_index=run_index)
        except (ConnectionError, RuntimeError, ValueError, OSError) as exc:
            return ExtractionRun(
                model=self.model,
                task_id=gold.task_id,
                indicator_id=indicator_id,
                run_index=run_index,
                candidate_evidence="",
                quoted_text_span="",
                confidence_level="low",
                error=str(exc),
            )


class StabilityMockRunner:
    """
    Mock runner with run-dependent variation for reproducible stability tests.

    Models have different ``output_stability`` rates (deterministic from model name).
    """

    def __init__(self, model: str, *, base_seed: int = DEFAULT_BASE_SEED) -> None:
        self.model = model
        self.base_seed = base_seed
        self._base = MockExtractionRunner(model)

    def run(
        self,
        document_text: str,
        indicator_id: str,
        *,
        gold: TaskGold,
        run_index: int,
    ) -> ExtractionRun:
        base_result, _ = self._base.run(
            document_text,
            indicator_id,
            gold=gold,
        )
        bucket = int(
            hashlib.sha256(
                f"{self.model}:{gold.task_id}:{run_index}:{self.base_seed}".encode()
            ).hexdigest()[:8],
            16,
        )
        stability_rate = _deterministic_rate(self.model, "output_stability", 0.72)
        if (bucket % 1000) / 1000.0 < stability_rate:
            return _result_to_run(base_result, gold.task_id, run_index=run_index)

        variant = (bucket // 17) % 5
        confidence = CONFIDENCE_LEVELS[(bucket // 3) % 3]
        evidence = (
            base_result.candidate_evidence
            if variant == 0
            else f"{base_result.candidate_evidence} [stability variant {variant}]"
        )
        if base_result.quoted_text_span:
            quote = (
                base_result.quoted_text_span
                if variant <= 1
                else f"{base_result.quoted_text_span} (run {run_index % 3})"
            )
        elif gold.gold_keywords:
            quote = _find_gold_quote(document_text, gold.gold_keywords) or ""
            if variant >= 2:
                quote = f"{quote} alt-{variant}".strip()
        else:
            quote = f"synthetic variant {variant}" if variant else ""

        varied = replace(
            base_result,
            candidate_evidence=evidence,
            quoted_text_span=quote,
            confidence_level=confidence,  # type: ignore[arg-type]
        )
        return _result_to_run(varied, gold.task_id, run_index=run_index)


def _result_to_run(
    result: EvidenceExtractionResult,
    task_id: str,
    *,
    run_index: int,
) -> ExtractionRun:
    return ExtractionRun(
        model=result.model,
        task_id=task_id,
        indicator_id=result.indicator_id,
        run_index=run_index,
        candidate_evidence=result.candidate_evidence,
        quoted_text_span=result.quoted_text_span,
        confidence_level=result.confidence_level,
    )


def run_task_stability(
    model: str,
    task: BenchmarkTask,
    runner: StabilityRunner,
    *,
    n_runs: int = DEFAULT_RUNS_PER_TASK,
) -> list[ExtractionRun]:
    """Execute *n_runs* extractions for a single task."""
    runs: list[ExtractionRun] = []
    for run_index in range(n_runs):
        runs.append(
            runner.run(
                task.document_text,
                task.gold.indicator_id,
                gold=task.gold,
                run_index=run_index,
            )
        )
    return runs


def run_model_stability(
    model: str,
    tasks: list[BenchmarkTask],
    runner: StabilityRunner,
    *,
    n_runs: int = DEFAULT_RUNS_PER_TASK,
    runs_dir: Path | None = None,
    save_runs: bool = True,
) -> list[TaskStabilitySummary]:
    """Run stability protocol for all tasks for one model."""
    summaries: list[TaskStabilitySummary] = []
    model_dir: Path | None = None
    if save_runs and runs_dir is not None:
        model_dir = runs_dir / model.replace(":", "_").replace("/", "_")
        model_dir.mkdir(parents=True, exist_ok=True)

    for task in tasks:
        runs = run_task_stability(model, task, runner, n_runs=n_runs)
        summary = summarize_task_runs(runs)
        summaries.append(summary)
        if model_dir is not None:
            payload = {
                "model": model,
                "task_id": task.gold.task_id,
                "summary": asdict(summary),
                "runs": [asdict(r) for r in runs],
            }
            out_path = model_dir / f"{task.gold.task_id}.json"
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return summaries


def aggregate_model_stability(summaries: list[TaskStabilitySummary]) -> dict[str, Any]:
    """Mean stability metrics across tasks for one model."""
    if not summaries:
        return {}
    successful = [s for s in summaries if s.n_success > 0]

    def _mean(attr: str) -> float:
        vals = [getattr(s, attr) for s in successful]
        return round(mean(vals), 4) if vals else 0.0

    return {
        "model": summaries[0].model,
        "n_tasks": len(summaries),
        "mean_quote_stability": _mean("quote_stability"),
        "mean_evidence_stability": _mean("evidence_stability"),
        "mean_confidence_stability": _mean("confidence_stability"),
        "min_quote_stability": round(min((s.quote_stability for s in successful), default=0.0), 4),
        "min_evidence_stability": round(
            min((s.evidence_stability for s in successful), default=0.0), 4
        ),
        "status": "ok" if all(s.n_success == s.n_runs for s in summaries) else "partial",
    }


def interpret_variability(mean_stability: float) -> str:
    """Short interpretation label for mean stability (across fields)."""
    if mean_stability >= 0.9:
        return "highly stable"
    if mean_stability >= 0.7:
        return "moderately stable"
    if mean_stability >= 0.5:
        return "variable"
    return "highly variable"


def run_full_stability_study(
    *,
    models: tuple[str, ...] = BENCHMARK_MODELS,
    tasks_path: Path = DEFAULT_TASKS_PATH,
    repo_root: Path | None = None,
    n_runs: int = DEFAULT_RUNS_PER_TASK,
    base_seed: int = DEFAULT_BASE_SEED,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    mock: bool = False,
    skip_unavailable: bool = True,
    save_runs: bool = True,
) -> tuple[list[ExtractionRun], list[TaskStabilitySummary], list[dict[str, Any]], Path]:
    """Run stability study for all models; return runs, task summaries, model summaries."""
    root = repo_root or REPO_ROOT
    tasks_path = tasks_path if tasks_path.is_absolute() else root / tasks_path
    tasks = load_benchmark_tasks(tasks_path, repo_root=root)
    _, _, runs_dir = stability_output_paths(root)
    if save_runs:
        runs_dir.mkdir(parents=True, exist_ok=True)

    available = list_ollama_models(base_url) if not mock else set(models)

    def _model_available(name: str) -> bool:
        if name in available:
            return True
        base = name.split(":")[0]
        return any(tag == name or tag.startswith(f"{base}:") for tag in available)

    all_runs: list[ExtractionRun] = []
    all_task_summaries: list[TaskStabilitySummary] = []
    model_summaries: list[dict[str, Any]] = []

    for model in models:
        if not mock and skip_unavailable and not _model_available(model):
            model_summaries.append(
                {
                    "model": model,
                    "n_tasks": len(tasks),
                    "status": "model_not_available",
                    "mean_quote_stability": "",
                    "mean_evidence_stability": "",
                    "mean_confidence_stability": "",
                }
            )
            continue

        runner: StabilityRunner = (
            StabilityMockRunner(model, base_seed=base_seed)
            if mock
            else StabilityLiveRunner(model, base_url=base_url)
        )
        task_summaries: list[TaskStabilitySummary] = []
        model_dir = None
        if save_runs:
            model_dir = runs_dir / model.replace(":", "_").replace("/", "_")
            model_dir.mkdir(parents=True, exist_ok=True)

        for task in tasks:
            runs = run_task_stability(model, task, runner, n_runs=n_runs)
            all_runs.extend(runs)
            summary = summarize_task_runs(runs)
            task_summaries.append(summary)
            if model_dir is not None:
                payload = {
                    "model": model,
                    "task_id": task.gold.task_id,
                    "summary": asdict(summary),
                    "runs": [asdict(r) for r in runs],
                }
                (model_dir / f"{task.gold.task_id}.json").write_text(
                    json.dumps(payload, indent=2),
                    encoding="utf-8",
                )

        all_task_summaries.extend(task_summaries)
        model_row = aggregate_model_stability(task_summaries)
        model_row["mode"] = "mock" if mock else "live"
        model_row["n_runs_per_task"] = n_runs
        model_row["overall_stability"] = round(
            (
                model_row["mean_quote_stability"]
                + model_row["mean_evidence_stability"]
                + model_row["mean_confidence_stability"]
            )
            / 3.0,
            4,
        )
        model_row["variability_label"] = interpret_variability(model_row["overall_stability"])
        model_summaries.append(model_row)

    return all_runs, all_task_summaries, model_summaries, runs_dir


CSV_FIELDNAMES: tuple[str, ...] = (
    "record_type",
    "model",
    "task_id",
    "indicator_id",
    "run_index",
    "candidate_evidence",
    "quoted_text_span",
    "confidence_level",
    "error",
    "n_runs",
    "n_success",
    "quote_stability",
    "evidence_stability",
    "confidence_stability",
    "unique_quotes",
    "unique_evidence",
    "unique_confidence",
    "mean_quote_stability",
    "mean_evidence_stability",
    "mean_confidence_stability",
    "overall_stability",
    "variability_label",
    "status",
    "mode",
)


def build_csv_rows(
    runs: list[ExtractionRun],
    task_summaries: list[TaskStabilitySummary],
    model_summaries: list[dict[str, Any]],
    *,
    n_runs: int,
    base_seed: int,
    mock: bool,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for run in runs:
        rows.append(
            {
                "record_type": "run",
                "model": run.model,
                "task_id": run.task_id,
                "indicator_id": run.indicator_id,
                "run_index": run.run_index,
                "candidate_evidence": run.candidate_evidence,
                "quoted_text_span": run.quoted_text_span,
                "confidence_level": run.confidence_level,
                "error": run.error or "",
            }
        )
    for summary in task_summaries:
        rows.append(
            {
                "record_type": "task_summary",
                "model": summary.model,
                "task_id": summary.task_id,
                "indicator_id": summary.indicator_id,
                "n_runs": summary.n_runs,
                "n_success": summary.n_success,
                "quote_stability": summary.quote_stability,
                "evidence_stability": summary.evidence_stability,
                "confidence_stability": summary.confidence_stability,
                "unique_quotes": summary.unique_quotes,
                "unique_evidence": summary.unique_evidence,
                "unique_confidence": summary.unique_confidence,
            }
        )
    for model_row in model_summaries:
        rows.append(
            {
                "record_type": "model_summary",
                "model": model_row.get("model", ""),
                "n_runs": n_runs,
                "mean_quote_stability": model_row.get("mean_quote_stability", ""),
                "mean_evidence_stability": model_row.get("mean_evidence_stability", ""),
                "mean_confidence_stability": model_row.get("mean_confidence_stability", ""),
                "overall_stability": model_row.get("overall_stability", ""),
                "variability_label": model_row.get("variability_label", ""),
                "status": model_row.get("status", ""),
                "mode": model_row.get("mode", "live" if not mock else "mock"),
            }
        )
    rows.append(
        {
            "record_type": "study_meta",
            "n_runs": n_runs,
            "mode": "mock" if mock else "live",
            "status": f"seed={base_seed}",
        }
    )
    return rows


def render_stability_report(
    task_summaries: list[TaskStabilitySummary],
    model_summaries: list[dict[str, Any]],
    *,
    n_runs: int,
    base_seed: int,
    mock: bool,
    tasks_path: Path,
    runs_dir: Path,
    csv_path: Path,
) -> str:
    mode = "mock" if mock else "live"
    banner = (
        "> **MOCK stability benchmark (testing only)** — run-indexed pseudo-variation. "
        "Do not cite as empirical Ollama stability."
        if mock
        else "> **LIVE stability benchmark** — repeated extractions per task (Ollama sampling)."
    )

    lines = [
        "# Extraction stability benchmark",
        "",
        banner,
        "",
        "Evaluates whether the **same model** returns **similar evidence** when the identical "
        "task is executed repeatedly.",
        "",
        f"**Runs per task:** {n_runs}",
        f"**Base seed (mock):** {base_seed}",
        f"**Tasks:** `{tasks_path}`",
        f"**Results CSV:** `{csv_path.name}`",
        f"**Per-task JSON:** `{runs_dir}/<model>/<task_id>.json`",
        "",
        "## Stability metrics",
        "",
        "| Metric | Definition |",
        "|--------|------------|",
        "| Quote stability | Share of runs whose normalized `quoted_text_span` matches the modal quote |",
        "| Evidence stability | Share of runs whose normalized `candidate_evidence` matches the modal summary |",
        "| Confidence stability | Share of runs whose `confidence_level` matches the modal level |",
        "",
        "Values range 0–1 (1 = identical outputs every run). `unique_*` counts distinct normalized values.",
        "",
        "## Model summary",
        "",
        "| Model | Quote | Evidence | Confidence | Overall | Interpretation | Status |",
        "|-------|------:|---------:|-----------:|--------:|----------------|--------|",
    ]

    for row in model_summaries:
        if row.get("status") == "model_not_available":
            lines.append(f"| `{row['model']}` | — | — | — | — | unavailable | unavailable |")
            continue
        lines.append(
            f"| `{row['model']}` | {row.get('mean_quote_stability', '')} | "
            f"{row.get('mean_evidence_stability', '')} | {row.get('mean_confidence_stability', '')} | "
            f"{row.get('overall_stability', '')} | {row.get('variability_label', '')} | "
            f"{row.get('status', '')} |"
        )

    lines.extend(
        [
            "",
            "## Variability interpretation",
            "",
        ]
    )

    if mock:
        lines.append(
            "Mock mode injects controlled cross-run variation using a deterministic "
            "per-model **output_stability** rate. Models with lower configured stability "
            "produce more alternate quotes, evidence strings, and confidence labels — "
            "mirroring operational inconsistency without calling Ollama."
        )
    else:
        lines.append(
            "Live mode reflects Ollama default sampling. Low stability may indicate temperature, "
            "prompt sensitivity, or ambiguous documents — not necessarily incorrect extractions. "
            "Human verification remains mandatory regardless of stability scores."
        )

    lines.extend(
        [
            "",
            "### Reading guide",
            "",
            "- **Highly stable (≥0.9):** reviewers can expect near-identical candidate evidence across reruns.",
            "- **Moderately stable (0.7–0.9):** minor wording drift; verify quotes before scoring.",
            "- **Variable (0.5–0.7):** substantive disagreement; do not auto-accept evidence.",
            "- **Highly variable (<0.5):** unsuitable for unattended extraction pipelines.",
            "",
            "Confidence stability below quote stability often means the model hedges with alternating "
            "`low` / `medium` / `high` labels while paraphrasing similar content.",
            "",
            "## Task-level detail",
            "",
            "See `results/extraction_stability.csv` (`record_type=task_summary`) for per-task stability.",
            "",
            "## Reproduce",
            "",
            "```bash",
            "python scripts/run_extraction_stability.py --mock",
            "python scripts/run_extraction_stability.py  # requires Ollama",
            "```",
            "",
            f"Mode: `{mode}`",
            "",
        ]
    )

    # Highlight least stable tasks per model (first model only in report if many)
    unstable = sorted(
        [s for s in task_summaries if s.quote_stability < 0.7],
        key=lambda s: s.quote_stability,
    )[:5]
    if unstable:
        lines.append("### Least stable tasks (sample)")
        lines.append("")
        for s in unstable:
            lines.append(
                f"- `{s.model}` / `{s.task_id}`: quote={s.quote_stability}, "
                f"evidence={s.evidence_stability}, confidence={s.confidence_stability}"
            )
        lines.append("")

    return "\n".join(lines)


def write_stability_outputs(
    runs: list[ExtractionRun],
    task_summaries: list[TaskStabilitySummary],
    model_summaries: list[dict[str, Any]],
    *,
    n_runs: int,
    base_seed: int,
    mock: bool,
    tasks_path: Path,
    repo_root: Path | None = None,
) -> tuple[Path, Path, Path]:
    """Write CSV, Markdown report; return paths including runs_dir."""
    root = repo_root or REPO_ROOT
    csv_path, report_path, runs_dir = stability_output_paths(root)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    rows = build_csv_rows(
        runs,
        task_summaries,
        model_summaries,
        n_runs=n_runs,
        base_seed=base_seed,
        mock=mock,
    )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    try:
        tasks_display = tasks_path.relative_to(root)
    except ValueError:
        tasks_display = tasks_path
    try:
        runs_display = runs_dir.relative_to(root)
    except ValueError:
        runs_display = runs_dir
    try:
        csv_display = csv_path.relative_to(root)
    except ValueError:
        csv_display = csv_path

    report_path.write_text(
        render_stability_report(
            task_summaries,
            model_summaries,
            n_runs=n_runs,
            base_seed=base_seed,
            mock=mock,
            tasks_path=tasks_display,
            runs_dir=runs_display,
            csv_path=csv_display,
        ),
        encoding="utf-8",
    )
    return csv_path, report_path, runs_dir
