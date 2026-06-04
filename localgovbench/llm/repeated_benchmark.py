"""Repeated-run protocol for LocalGovBench LLM evidence extraction benchmark."""

from __future__ import annotations

import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    DEFAULT_TASKS_PATH,
    ExtractionRunner,
    LiveExtractionRunner,
    MockExtractionRunner,
    REPO_ROOT,
    list_ollama_models,
    load_benchmark_tasks,
    run_model_benchmark,
)

REPEATED_CSV_NAME = "model_benchmark_repeated.csv"
REPEATED_REPORT_NAME = "model_benchmark_repeated.md"
REPEATED_RUNS_DIRNAME = "repeated_runs"

METRIC_KEYS = (
    "evidence_precision",
    "quote_validity_rate",
    "hallucinated_evidence_rate",
    "insufficient_evidence_detection_rate",
    "mean_latency_seconds",
)

# Two-sided 95% t critical values (df = n - 1) for run-level means; df >= 30 -> 1.96
_T_CRITICAL_975: dict[int, float] = {
    1: 12.706,
    2: 4.303,
    3: 3.182,
    4: 2.776,
    5: 2.571,
    6: 2.447,
    7: 2.365,
    8: 2.306,
    9: 2.262,
    10: 2.228,
    11: 2.201,
    12: 2.179,
    13: 2.16,
    14: 2.145,
    15: 2.131,
    20: 2.086,
    25: 2.06,
    29: 2.045,
}


def repeated_output_paths(repo_root: Path | None = None) -> tuple[Path, Path, Path]:
    """Return (csv_path, report_path, runs_dir)."""
    root = repo_root or REPO_ROOT
    return (
        root / "results" / REPEATED_CSV_NAME,
        root / "reports" / REPEATED_REPORT_NAME,
        root / "results" / REPEATED_RUNS_DIRNAME,
    )


def _model_dir_name(model: str) -> str:
    return model.replace(":", "_").replace("/", "_")


def shuffle_tasks(tasks: list, seed: int) -> list:
    """Return a new list with tasks in randomized order."""
    ordered = list(tasks)
    rng = random.Random(seed)
    rng.shuffle(ordered)
    return ordered


def t_critical_975(df: int) -> float:
    """Two-sided 95% Student-t critical value for *df* degrees of freedom."""
    if df <= 0:
        return 0.0
    if df >= 30:
        return 1.96
    return _T_CRITICAL_975.get(df, 2.0)


def mean_std_ci95(values: list[float]) -> dict[str, float | None]:
    """Sample mean, sample stdev (ddof=1), and 95% CI for the mean."""
    n = len(values)
    if n == 0:
        return {
            "mean": None,
            "std": None,
            "ci95_low": None,
            "ci95_high": None,
            "n": 0,
        }
    mean = statistics.mean(values)
    if n == 1:
        return {
            "mean": mean,
            "std": 0.0,
            "ci95_low": mean,
            "ci95_high": mean,
            "n": 1,
        }
    std = statistics.stdev(values)
    margin = t_critical_975(n - 1) * std / math.sqrt(n)
    return {
        "mean": mean,
        "std": std,
        "ci95_low": mean - margin,
        "ci95_high": mean + margin,
        "n": n,
    }


@dataclass(frozen=True, slots=True)
class SingleRunRecord:
    model: str
    run_index: int
    seed: int
    task_order: tuple[str, ...]
    metrics: dict[str, Any]
    status: str


def run_single_repetition(
    model: str,
    tasks_shuffled: list,
    runner: ExtractionRunner,
) -> tuple[dict[str, Any], str]:
    """Run one repetition; return (aggregate metrics dict, status)."""
    _, metrics = run_model_benchmark(model, tasks_shuffled, runner)
    n_tasks = metrics["n_tasks"]
    n_success = metrics["n_success"]
    if n_success == 0:
        status = "failed"
    elif n_success < n_tasks:
        status = "partial"
    else:
        status = "ok"
    return metrics, status


def run_repeated_benchmark_for_model(
    model: str,
    base_tasks: list,
    *,
    n_repetitions: int,
    base_seed: int,
    runner: ExtractionRunner,
    runs_dir: Path,
    save_runs: bool = True,
) -> list[SingleRunRecord]:
    """Execute *n_repetitions* with shuffled task order per repetition."""
    model_dir = runs_dir / _model_dir_name(model)
    if save_runs:
        model_dir.mkdir(parents=True, exist_ok=True)

    records: list[SingleRunRecord] = []
    for run_index in range(n_repetitions):
        seed = base_seed + run_index
        tasks_ordered = shuffle_tasks(base_tasks, seed)
        task_order = tuple(t.gold.task_id for t in tasks_ordered)
        metrics, status = run_single_repetition(model, tasks_ordered, runner)
        record = SingleRunRecord(
            model=model,
            run_index=run_index,
            seed=seed,
            task_order=task_order,
            metrics=metrics,
            status=status,
        )
        records.append(record)
        if save_runs:
            payload = {
                "model": model,
                "run_index": run_index,
                "seed": seed,
                "task_order": list(task_order),
                "metrics": metrics,
                "status": status,
            }
            out_path = model_dir / f"run_{run_index:03d}.json"
            out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return records


def aggregate_repeated_runs(records: list[SingleRunRecord]) -> dict[str, Any]:
    """Compute mean/std/CI95 per metric across repetitions for one model."""
    if not records:
        return {"model": "", "n_repetitions": 0, "status": "no_runs"}

    model = records[0].model
    n = len(records)
    row: dict[str, Any] = {
        "model": model,
        "n_repetitions": n,
        "n_tasks_per_run": records[0].metrics.get("n_tasks", 0),
        "status": "ok" if all(r.status == "ok" for r in records) else "partial",
    }

    for key in METRIC_KEYS:
        values = [float(r.metrics[key]) for r in records if key in r.metrics]
        stats = mean_std_ci95(values)
        row[f"mean_{key}"] = round(stats["mean"], 4) if stats["mean"] is not None else ""
        row[f"std_{key}"] = round(stats["std"], 4) if stats["std"] is not None else ""
        low = stats["ci95_low"]
        high = stats["ci95_high"]
        row[f"ci95_{key}_low"] = round(low, 4) if low is not None else ""
        row[f"ci95_{key}_high"] = round(high, 4) if high is not None else ""

    return row


def run_full_repeated_benchmark(
    *,
    models: tuple[str, ...] = BENCHMARK_MODELS,
    tasks_path: Path = DEFAULT_TASKS_PATH,
    repo_root: Path | None = None,
    n_repetitions: int = 10,
    base_seed: int = 42,
    base_url: str = "http://127.0.0.1:11434",
    mock: bool = False,
    skip_unavailable: bool = True,
    save_runs: bool = True,
) -> tuple[list[dict[str, Any]], Path]:
    """Run repeated benchmark for all models; return summary rows and runs directory."""
    root = repo_root or REPO_ROOT
    tasks_path = tasks_path if tasks_path.is_absolute() else root / tasks_path
    base_tasks = load_benchmark_tasks(tasks_path, repo_root=root)
    _, _, runs_dir = repeated_output_paths(root)

    available = list_ollama_models(base_url) if not mock else set(models)

    def _model_available(name: str) -> bool:
        if name in available:
            return True
        base = name.split(":")[0]
        return any(tag == name or tag.startswith(f"{base}:") for tag in available)

    summary_rows: list[dict[str, Any]] = []

    for model in models:
        if not mock and skip_unavailable and not _model_available(model):
            summary_rows.append(_unavailable_summary_row(model, n_repetitions, len(base_tasks)))
            continue

        runner: ExtractionRunner = (
            MockExtractionRunner(model) if mock else LiveExtractionRunner(model, base_url=base_url)
        )
        records = run_repeated_benchmark_for_model(
            model,
            base_tasks,
            n_repetitions=n_repetitions,
            base_seed=base_seed,
            runner=runner,
            runs_dir=runs_dir,
            save_runs=save_runs,
        )
        summary_rows.append(aggregate_repeated_runs(records))

    return summary_rows, runs_dir


def _unavailable_summary_row(model: str, n_repetitions: int, n_tasks: int) -> dict[str, Any]:
    row: dict[str, Any] = {
        "model": model,
        "n_repetitions": n_repetitions,
        "n_tasks_per_run": n_tasks,
        "status": "model_not_available",
    }
    for key in METRIC_KEYS:
        row[f"mean_{key}"] = ""
        row[f"std_{key}"] = ""
        row[f"ci95_{key}_low"] = ""
        row[f"ci95_{key}_high"] = ""
    return row


def repeated_csv_fieldnames() -> list[str]:
    fields = ["model", "n_repetitions", "n_tasks_per_run", "status"]
    for key in METRIC_KEYS:
        fields.extend(
            [
                f"mean_{key}",
                f"std_{key}",
                f"ci95_{key}_low",
                f"ci95_{key}_high",
            ]
        )
    return fields


def render_repeated_benchmark_report(
    rows: list[dict[str, Any]],
    *,
    n_repetitions: int,
    base_seed: int,
    mock: bool,
    tasks_path: Path,
    runs_dir: Path,
    csv_path: Path,
) -> str:
    mode = "mock" if mock else "live"
    if mock:
        banner = (
            "> **MOCK repeated benchmark (testing only)** — deterministic pseudo-extractions. "
            "Do not cite as empirical Ollama comparison."
        )
    else:
        banner = (
            "> **LIVE repeated benchmark** — each model run *N* times with randomized task order per repetition."
        )

    lines = [
        "# LocalGovBench repeated LLM evidence extraction benchmark",
        "",
        banner,
        "",
        f"**Repetitions per model:** {n_repetitions}",
        f"**Base seed:** {base_seed} (run *i* uses seed = base_seed + i)",
        f"**Tasks:** `{tasks_path}`",
        f"**Summary CSV:** `{csv_path.name}`",
        f"**Individual runs:** `{runs_dir}/<model>/run_XXX.json`",
        "",
        "## Summary (mean ± std across repetitions)",
        "",
        "95% confidence intervals (CI) apply to the **mean of per-run metrics** (Student-t, df = N−1).",
        "",
        "| Model | Prec. mean±std | Prec. 95% CI | Halluc. mean±std | Latency mean±std (s) | Status |",
        "|-------|----------------|--------------|------------------|----------------------|--------|",
    ]
    for row in rows:
        if row.get("status") == "model_not_available":
            lines.append(f"| `{row['model']}` | — | — | — | — | unavailable |")
            continue
        prec_m = row.get("mean_evidence_precision", "")
        prec_s = row.get("std_evidence_precision", "")
        prec_lo = row.get("ci95_evidence_precision_low", "")
        prec_hi = row.get("ci95_evidence_precision_high", "")
        hall_m = row.get("mean_hallucinated_evidence_rate", "")
        hall_s = row.get("std_hallucinated_evidence_rate", "")
        lat_m = row.get("mean_mean_latency_seconds", "")
        lat_s = row.get("std_mean_latency_seconds", "")
        lines.append(
            f"| `{row['model']}` | {prec_m}±{prec_s} | [{prec_lo}, {prec_hi}] | "
            f"{hall_m}±{hall_s} | {lat_m}±{lat_s} | {row.get('status', '')} |"
        )

    lines.extend(
        [
            "",
            "## Full metrics",
            "",
            "See `results/model_benchmark_repeated.csv` for all means, standard deviations, and CI bounds:",
            "",
            "- `evidence_precision`",
            "- `quote_validity_rate`",
            "- `hallucinated_evidence_rate`",
            "- `insufficient_evidence_detection_rate`",
            "- `mean_latency_seconds`",
            "",
            "## Reproduce",
            "",
            "```bash",
            "python scripts/run_llm_model_benchmark_repeated.py --mock --repetitions 3",
            "python scripts/run_llm_model_benchmark_repeated.py --repetitions 10",
            "```",
            "",
            f"Mode: `{mode}`",
            "",
        ]
    )
    return "\n".join(lines)


def write_repeated_benchmark_outputs(
    rows: list[dict[str, Any]],
    *,
    n_repetitions: int,
    base_seed: int,
    mock: bool,
    tasks_path: Path,
    repo_root: Path | None = None,
) -> tuple[Path, Path, Path]:
    """Write summary CSV, Markdown report, and return runs directory path."""
    root = repo_root or REPO_ROOT
    csv_path, report_path, runs_dir = repeated_output_paths(root)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = repeated_csv_fieldnames()
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})

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
        render_repeated_benchmark_report(
            rows,
            n_repetitions=n_repetitions,
            base_seed=base_seed,
            mock=mock,
            tasks_path=tasks_display,
            runs_dir=runs_display,
            csv_path=csv_display,
        ),
        encoding="utf-8",
    )
    return csv_path, report_path, runs_dir
