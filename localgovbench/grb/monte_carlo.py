"""GRB Monte Carlo sensitivity — random synthetic indicator profiles."""

from __future__ import annotations

import math
import random
from collections import Counter
from pathlib import Path
from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Any, Iterable, Sequence

from localgovbench.grb.scoring import SAFEGUARD_CAP, SAFEGUARD_THRESHOLD, compute_grb_assessment
from localgovbench.grb.specification import GRB_SPEC_VERSION, SAFEGUARD_DIMENSION_IDS, all_indicator_ids

DEFAULT_PROFILE_COUNT = 10_000
PERCENTILE_POINTS: tuple[int, ...] = (5, 10, 25, 50, 75, 90, 95)
DIMENSION_IDS: tuple[str, ...] = ("d1", "d2", "d3", "d4", "d5", "d6")

PROFILE_CSV_FIELDS: tuple[str, ...] = (
    "record_type",
    "profile_id",
    "distribution",
    "d1_score",
    "d2_score",
    "d3_score",
    "d4_score",
    "d5_score",
    "d6_score",
    "overall_maturity",
    "readiness_raw",
    "readiness_final",
    "readiness_band",
    "safeguard_applied",
    "readiness_delta_raw_final",
    "metric",
    "value",
    "count",
    "fraction",
)


@dataclass(frozen=True, slots=True)
class ScoreDistribution:
    """Discrete distribution over maturity levels 0–4."""

    name: str
    weights: tuple[float, float, float, float, float]

    def __post_init__(self) -> None:
        if len(self.weights) != 5:
            raise ValueError("weights must have five entries for levels 0–4")
        if any(w < 0 for w in self.weights):
            raise ValueError("weights must be non-negative")
        total = sum(self.weights)
        if total <= 0:
            raise ValueError("weights must sum to a positive value")

    def sample(self, rng: random.Random) -> int:
        return rng.choices(range(5), weights=self.weights, k=1)[0]

    @property
    def normalized_weights(self) -> tuple[float, ...]:
        total = sum(self.weights)
        return tuple(w / total for w in self.weights)


DISTRIBUTION_PRESETS: dict[str, ScoreDistribution] = {
    "uniform": ScoreDistribution("uniform", (1.0, 1.0, 1.0, 1.0, 1.0)),
    "baseline": ScoreDistribution("baseline", (0.02, 0.05, 0.13, 0.55, 0.25)),
    "low": ScoreDistribution("low", (0.25, 0.25, 0.20, 0.20, 0.10)),
    "high": ScoreDistribution("high", (0.05, 0.10, 0.20, 0.35, 0.30)),
    "mixed_regimes": ScoreDistribution("mixed_regimes", (1.0, 1.0, 1.0, 1.0, 1.0)),
}


@dataclass(frozen=True, slots=True)
class MonteCarloProfileResult:
    """Scored Monte Carlo profile."""

    profile_id: str
    distribution: str
    dimension_scores: dict[str, float]
    overall_maturity: float
    readiness_raw: float
    readiness_final: float
    readiness_band: str
    safeguard_applied: bool
    readiness_delta: float
    safeguard_dims_below_threshold: tuple[str, ...]


def resolve_distribution(name: str) -> ScoreDistribution:
    key = name.strip().lower()
    if key not in DISTRIBUTION_PRESETS:
        known = ", ".join(sorted(DISTRIBUTION_PRESETS))
        raise ValueError(f"Unknown distribution {name!r}; choose from: {known}")
    return DISTRIBUTION_PRESETS[key]


def _mixed_regime_distribution(rng: random.Random) -> ScoreDistribution:
    """Per-profile regime: uniform, baseline, low, or high."""
    regimes = (
        DISTRIBUTION_PRESETS["uniform"],
        DISTRIBUTION_PRESETS["baseline"],
        DISTRIBUTION_PRESETS["low"],
        DISTRIBUTION_PRESETS["high"],
    )
    return rng.choice(regimes)


def build_random_responses(
    rng: random.Random,
    distribution: ScoreDistribution,
) -> dict[str, int]:
    """Sample each of the 54 indicators independently from *distribution*."""
    return {indicator_id: distribution.sample(rng) for indicator_id in all_indicator_ids()}


def score_monte_carlo_profile(
    profile_id: str,
    responses: dict[str, int],
    *,
    distribution: str,
) -> MonteCarloProfileResult:
    payload = {
        "metadata": {
            "municipality": f"GRB Monte Carlo {profile_id}",
            "profile": profile_id,
            "scenario": "monte_carlo",
            "synthetic": True,
        },
        "responses": responses,
        "evidence": {},
    }
    result = compute_grb_assessment(payload)
    below = tuple(
        dim_id
        for dim_id in sorted(SAFEGUARD_DIMENSION_IDS)
        if result.dimension_scores.get(dim_id, 0.0) < SAFEGUARD_THRESHOLD
    )
    return MonteCarloProfileResult(
        profile_id=profile_id,
        distribution=distribution,
        dimension_scores=dict(result.dimension_scores),
        overall_maturity=result.overall_maturity,
        readiness_raw=result.readiness_raw,
        readiness_final=result.readiness_final,
        readiness_band=result.readiness_band,
        safeguard_applied=result.safeguard_applied,
        readiness_delta=round(result.readiness_raw - result.readiness_final, 2),
        safeguard_dims_below_threshold=below,
    )


def run_monte_carlo_study(
    *,
    profile_count: int = DEFAULT_PROFILE_COUNT,
    distribution_name: str = "uniform",
    seed: int = 42,
) -> tuple[list[MonteCarloProfileResult], dict[str, Any]]:
    """Generate and score *profile_count* random GRB profiles."""
    if profile_count < 1:
        raise ValueError("profile_count must be >= 1")

    preset = resolve_distribution(distribution_name)
    rng = random.Random(seed)
    results: list[MonteCarloProfileResult] = []

    for idx in range(profile_count):
        profile_id = f"grb_mc_{idx:05d}"
        if preset.name == "mixed_regimes":
            regime = _mixed_regime_distribution(rng)
            responses = build_random_responses(rng, regime)
            dist_label = regime.name
        else:
            responses = build_random_responses(rng, preset)
            dist_label = preset.name
        results.append(
            score_monte_carlo_profile(profile_id, responses, distribution=dist_label)
        )

    return results, summarize_monte_carlo(results, distribution_name=distribution_name, seed=seed)


def percentile(values: Sequence[float], p: float) -> float:
    """Linear-interpolation percentile on sorted *values*."""
    if not values:
        raise ValueError("values must not be empty")
    if p <= 0:
        return float(min(values))
    if p >= 100:
        return float(max(values))
    ordered = sorted(values)
    rank = (len(ordered) - 1) * (p / 100.0)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return float(ordered[int(rank)])
    weight = rank - lower
    return float(ordered[lower] * (1.0 - weight) + ordered[upper] * weight)


def summarize_monte_carlo(
    results: Iterable[MonteCarloProfileResult],
    *,
    distribution_name: str,
    seed: int,
) -> dict[str, Any]:
    """Aggregate readiness distribution, safeguards, dimensions, and percentiles."""
    rows = list(results)
    n = len(rows)
    if n == 0:
        raise ValueError("results must not be empty")

    readiness_raw = [r.readiness_raw for r in rows]
    readiness_final = [r.readiness_final for r in rows]
    safeguarded = [r for r in rows if r.safeguard_applied]

    dim_means = {
        dim_id: round(mean(r.dimension_scores[dim_id] for r in rows), 3)
        for dim_id in DIMENSION_IDS
    }
    dim_sum = sum(dim_means.values())
    dim_contribution_pct = {
        dim_id: round(100.0 * dim_means[dim_id] / dim_sum, 2) if dim_sum else 0.0
        for dim_id in DIMENSION_IDS
    }

    band_counts = Counter(r.readiness_band for r in rows)
    d2_below = sum(1 for r in rows if "d2" in r.safeguard_dims_below_threshold)
    d4_below = sum(1 for r in rows if "d4" in r.safeguard_dims_below_threshold)

    percentiles_raw = {f"p{p}": round(percentile(readiness_raw, p), 2) for p in PERCENTILE_POINTS}
    percentiles_final = {
        f"p{p}": round(percentile(readiness_final, p), 2) for p in PERCENTILE_POINTS
    }

    return {
        "profile_count": n,
        "distribution": distribution_name,
        "seed": seed,
        "grb_version": GRB_SPEC_VERSION,
        "readiness_raw_mean": round(mean(readiness_raw), 2),
        "readiness_raw_std": round(pstdev(readiness_raw), 2) if n > 1 else 0.0,
        "readiness_final_mean": round(mean(readiness_final), 2),
        "readiness_final_std": round(pstdev(readiness_final), 2) if n > 1 else 0.0,
        "safeguard_applied_count": len(safeguarded),
        "safeguard_applied_fraction": round(len(safeguarded) / n, 4),
        "safeguard_mean_cap_delta": round(mean(r.readiness_delta for r in safeguarded), 2)
        if safeguarded
        else 0.0,
        "d2_below_threshold_count": d2_below,
        "d4_below_threshold_count": d4_below,
        "dimension_means": dim_means,
        "dimension_contribution_pct": dim_contribution_pct,
        "readiness_band_counts": dict(sorted(band_counts.items())),
        "percentiles_raw": percentiles_raw,
        "percentiles_final": percentiles_final,
        "safeguard_cap": SAFEGUARD_CAP,
        "safeguard_threshold": SAFEGUARD_THRESHOLD,
    }


def profile_to_csv_row(result: MonteCarloProfileResult) -> dict[str, str | float | int | bool]:
    return {
        "record_type": "profile",
        "profile_id": result.profile_id,
        "distribution": result.distribution,
        "d1_score": result.dimension_scores["d1"],
        "d2_score": result.dimension_scores["d2"],
        "d3_score": result.dimension_scores["d3"],
        "d4_score": result.dimension_scores["d4"],
        "d5_score": result.dimension_scores["d5"],
        "d6_score": result.dimension_scores["d6"],
        "overall_maturity": result.overall_maturity,
        "readiness_raw": result.readiness_raw,
        "readiness_final": result.readiness_final,
        "readiness_band": result.readiness_band,
        "safeguard_applied": result.safeguard_applied,
        "readiness_delta_raw_final": result.readiness_delta,
        "metric": "",
        "value": "",
        "count": "",
        "fraction": "",
    }


def build_csv_rows(
    results: list[MonteCarloProfileResult],
    summary: dict[str, Any],
) -> list[dict[str, str | float | int | bool]]:
    rows = [profile_to_csv_row(r) for r in results]

    def _summary_row(
        record_type: str,
        metric: str,
        value: str | float = "",
        count: str | int = "",
        fraction: str | float = "",
    ) -> dict[str, str | float | int | bool]:
        return {
            "record_type": record_type,
            "profile_id": "",
            "distribution": str(summary["distribution"]),
            "d1_score": "",
            "d2_score": "",
            "d3_score": "",
            "d4_score": "",
            "d5_score": "",
            "d6_score": "",
            "overall_maturity": "",
            "readiness_raw": "",
            "readiness_final": "",
            "readiness_band": "",
            "safeguard_applied": "",
            "readiness_delta_raw_final": "",
            "metric": metric,
            "value": value,
            "count": count,
            "fraction": fraction,
        }

    rows.append(
        _summary_row(
            "study_meta",
            "profile_count",
            value=summary["profile_count"],
        )
    )
    rows.append(_summary_row("study_meta", "seed", value=summary["seed"]))
    rows.append(_summary_row("study_meta", "grb_version", value=summary["grb_version"]))

    for label, val in (
        ("readiness_raw_mean", summary["readiness_raw_mean"]),
        ("readiness_raw_std", summary["readiness_raw_std"]),
        ("readiness_final_mean", summary["readiness_final_mean"]),
        ("readiness_final_std", summary["readiness_final_std"]),
        ("safeguard_applied_fraction", summary["safeguard_applied_fraction"]),
        ("safeguard_mean_cap_delta", summary["safeguard_mean_cap_delta"]),
    ):
        rows.append(_summary_row("readiness_distribution", label, value=val))

    rows.append(
        _summary_row(
            "safeguard",
            "safeguard_applied",
            count=summary["safeguard_applied_count"],
            fraction=summary["safeguard_applied_fraction"],
        )
    )
    rows.append(
        _summary_row(
            "safeguard",
            "d2_below_threshold",
            count=summary["d2_below_threshold_count"],
            fraction=round(summary["d2_below_threshold_count"] / summary["profile_count"], 4),
        )
    )
    rows.append(
        _summary_row(
            "safeguard",
            "d4_below_threshold",
            count=summary["d4_below_threshold_count"],
            fraction=round(summary["d4_below_threshold_count"] / summary["profile_count"], 4),
        )
    )

    for dim_id in DIMENSION_IDS:
        rows.append(
            _summary_row(
                "dimension_contribution",
                f"{dim_id}_mean",
                value=summary["dimension_means"][dim_id],
            )
        )
        rows.append(
            _summary_row(
                "dimension_contribution",
                f"{dim_id}_contribution_pct",
                value=summary["dimension_contribution_pct"][dim_id],
            )
        )

    for band, count in summary["readiness_band_counts"].items():
        rows.append(
            _summary_row(
                "readiness_band",
                band,
                count=count,
                fraction=round(count / summary["profile_count"], 4),
            )
        )

    for p_label, val in summary["percentiles_raw"].items():
        rows.append(_summary_row("percentile_raw", p_label, value=val))
    for p_label, val in summary["percentiles_final"].items():
        rows.append(_summary_row("percentile_final", p_label, value=val))

    return rows


def render_monte_carlo_report(summary: dict[str, Any]) -> str:
    """Markdown report for GRB Monte Carlo sensitivity."""
    n = summary["profile_count"]
    dim_rows = "\n".join(
        f"| `{dim_id}` | {summary['dimension_means'][dim_id]} | "
        f"{summary['dimension_contribution_pct'][dim_id]}% |"
        for dim_id in DIMENSION_IDS
    )
    band_rows = "\n".join(
        f"| {band} | {count} | {100.0 * count / n:.1f}% |"
        for band, count in summary["readiness_band_counts"].items()
    )
    pct_raw = " | ".join(
        f"{label} {summary['percentiles_raw'][label]}" for label in summary["percentiles_raw"]
    )
    pct_final = " | ".join(
        f"{label} {summary['percentiles_final'][label]}"
        for label in summary["percentiles_final"]
    )

    lines = [
        "# GRB Monte Carlo Sensitivity Study",
        "",
        "## Objective",
        "",
        "Estimate the **distribution of GRB readiness** and **safeguard G1 activation** under "
        "stochastic synthetic profiles where each of the 54 indicators is drawn independently "
        "from a configurable discrete distribution on maturity levels 0–4.",
        "",
        "This extends deterministic dimension sweeps with **Monte Carlo** structural exploration — "
        "not empirical municipal validation.",
        "",
        "## Method",
        "",
        f"- **GRB version:** {summary['grb_version']} (frozen specification)",
        f"- **Profiles:** {n:,} synthetic draws",
        f"- **Distribution preset:** `{summary['distribution']}`",
        f"- **Random seed:** {summary['seed']}",
        f"- **Safeguard G1:** cap at {summary['safeguard_cap']} when D2 or D4 dimension score "
        f"< {summary['safeguard_threshold']}",
        "",
        "### Available distribution presets",
        "",
        "| Preset | Characterisation |",
        "|--------|------------------|",
        "| `uniform` | Equal probability on levels 0–4 |",
        "| `baseline` | Peaked at level 3 (managed maturity) |",
        "| `low` | Skew toward low maturity |",
        "| `high` | Skew toward high maturity |",
        "| `mixed_regimes` | Each profile draws uniform, baseline, low, or high regime |",
        "",
        "## Readiness distribution",
        "",
        f"| Statistic | Raw (0–100) | Final (0–100) |",
        f"|-----------|-------------|---------------|",
        f"| Mean | {summary['readiness_raw_mean']} | {summary['readiness_final_mean']} |",
        f"| Std. dev. | {summary['readiness_raw_std']} | {summary['readiness_final_std']} |",
        "",
        f"**Percentiles (raw):** {pct_raw}",
        "",
        f"**Percentiles (final):** {pct_final}",
        "",
        "## Safeguard G1 activation",
        "",
        f"- Applied: **{summary['safeguard_applied_count']:,}** profiles "
        f"({summary['safeguard_applied_fraction']:.1%})",
        f"- Mean cap reduction when applied: **{summary['safeguard_mean_cap_delta']}** points",
        f"- D2 dimension below threshold: **{summary['d2_below_threshold_count']:,}** profiles",
        f"- D4 dimension below threshold: **{summary['d4_below_threshold_count']:,}** profiles",
        "",
        "## Dimension contribution (mean scores)",
        "",
        "Mean dimension maturity (0–4) and share of total mean maturity mass:",
        "",
        "| Dimension | Mean score | Contribution share |",
        "|-----------|------------|--------------------|",
        dim_rows,
        "",
        "## Readiness bands (final)",
        "",
        "| Band | Count | Share |",
        "|------|-------|-------|",
        band_rows,
        "",
        "## Visualisations",
        "",
        "| Figure | Description |",
        "|--------|-------------|",
        "| `figures/grb_monte_carlo/readiness_distribution.png` | Histogram of raw vs final readiness |",
        "| `figures/grb_monte_carlo/safeguard_activation.png` | Safeguard G1 activation rate |",
        "| `figures/grb_monte_carlo/dimension_contribution.png` | Mean dimension scores |",
        "| `figures/grb_monte_carlo/percentile_bands.png` | Percentile bands (raw and final) |",
        "",
        "## Limitations",
        "",
        "- Independent indicator draws (no within-dimension correlation structure).",
        "- Evidence gates E2/E3 not exercised (empty evidence map).",
        "- Synthetic structural study only.",
        "",
        "---",
        "*Generated by `scripts/run_grb_monte_carlo.py`*",
    ]
    return "\n".join(lines)


def write_monte_carlo_figures(
    results: list[MonteCarloProfileResult],
    summary: dict[str, Any],
    output_dir: Path,
) -> list[Path]:
    """Write PNG visualisations; requires matplotlib."""
    import matplotlib.pyplot as plt

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    readiness_raw = [r.readiness_raw for r in results]
    readiness_final = [r.readiness_final for r in results]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(readiness_raw, bins=30, alpha=0.55, label="Raw readiness", color="#4c72b0")
    ax.hist(readiness_final, bins=30, alpha=0.55, label="Final readiness", color="#dd8452")
    ax.axvline(summary["safeguard_cap"], color="#c44e52", linestyle="--", linewidth=1.2, label="G1 cap (60)")
    ax.set_xlabel("Readiness index (0–100)")
    ax.set_ylabel("Profile count")
    ax.set_title(f"GRB readiness distribution (n={summary['profile_count']:,})")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "readiness_distribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(path)

    fig, ax = plt.subplots(figsize=(6, 4))
    applied = summary["safeguard_applied_count"]
    not_applied = summary["profile_count"] - applied
    ax.bar(
        ["Not applied", "G1 applied"],
        [not_applied, applied],
        color=["#55a868", "#c44e52"],
    )
    ax.set_ylabel("Profiles")
    ax.set_title(
        f"Safeguard G1 activation ({summary['safeguard_applied_fraction']:.1%}, n={summary['profile_count']:,})"
    )
    fig.tight_layout()
    path = output_dir / "safeguard_activation.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(path)

    fig, ax = plt.subplots(figsize=(8, 5))
    means = [summary["dimension_means"][d] for d in DIMENSION_IDS]
    ax.barh(DIMENSION_IDS, means, color="#8172b3")
    ax.set_xlabel("Mean dimension maturity (0–4)")
    ax.set_title("Dimension contribution (mean scores)")
    ax.set_xlim(0, 4)
    fig.tight_layout()
    path = output_dir / "dimension_contribution.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(path)

    fig, ax = plt.subplots(figsize=(8, 5))
    labels = [f"p{p}" for p in PERCENTILE_POINTS]
    raw_vals = [summary["percentiles_raw"][label] for label in labels]
    final_vals = [summary["percentiles_final"][label] for label in labels]
    x = range(len(labels))
    ax.plot(x, raw_vals, marker="o", label="Raw", color="#4c72b0")
    ax.plot(x, final_vals, marker="s", label="Final", color="#dd8452")
    ax.fill_between(x, raw_vals, alpha=0.12, color="#4c72b0")
    ax.fill_between(x, final_vals, alpha=0.12, color="#dd8452")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Readiness (0–100)")
    ax.set_title("Readiness percentile bands")
    ax.legend()
    fig.tight_layout()
    path = output_dir / "percentile_bands.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    written.append(path)

    return written
