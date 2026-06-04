"""GRB dimension ablation — measure readiness, ranking, and safeguard effects."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Sequence

from localgovbench.grb.profiles import build_assessment_payload
from localgovbench.grb.scoring import (
    MAX_SCORE,
    SAFEGUARD_CAP,
    SAFEGUARD_THRESHOLD,
    classify_readiness_band,
    compute_grb_assessment,
)
from localgovbench.grb.sensitivity import ProfileSpec, generate_profile_specs
from localgovbench.grb.specification import GRB_SPEC_VERSION, SAFEGUARD_DIMENSION_IDS

DIMENSION_IDS: tuple[str, ...] = ("d1", "d2", "d3", "d4", "d5", "d6")

ABLATION_CONFIGS: dict[str, frozenset[str]] = {
    "full": frozenset(),
    "without_d2": frozenset({"d2"}),
    "without_d4": frozenset({"d4"}),
    "without_d6": frozenset({"d6"}),
}


@dataclass(frozen=True, slots=True)
class AblationScore:
    """Readiness for one profile under one ablation configuration."""

    profile_id: str
    profile_group: str
    configuration: str
    excluded_dimensions: frozenset[str]
    overall_maturity: float
    readiness_raw: float
    readiness_final: float
    readiness_band: str
    safeguard_applied: bool
    rank: int = 0
    readiness_delta_vs_full: float = 0.0
    safeguard_delta_vs_full: int = 0


@dataclass(frozen=True, slots=True)
class AblationComparison:
    """Ranking and readiness comparison vs full model."""

    reference: str
    alternate: str
    spearman: float
    kendall_tau: float
    profiles_rank_changed: int
    total_rank_displacement: int
    mean_readiness_delta: float
    mean_abs_readiness_delta: float
    safeguard_applied_full: int
    safeguard_applied_alternate: int
    safeguard_activation_delta: int


def active_dimensions(excluded: frozenset[str]) -> tuple[str, ...]:
    return tuple(d for d in DIMENSION_IDS if d not in excluded)


def _apply_safeguard_on_active_dims(
    dimension_scores: dict[str, float],
    readiness: float,
    *,
    active_safeguard_dims: set[str],
) -> tuple[float, bool, str | None]:
    """Apply G1 only for safeguard dimensions included in the ablated model."""
    triggered = [
        dim_id
        for dim_id in sorted(active_safeguard_dims)
        if dimension_scores.get(dim_id, 0.0) < SAFEGUARD_THRESHOLD
    ]
    if not triggered:
        return readiness, False, None
    capped = min(readiness, SAFEGUARD_CAP)
    if capped >= readiness:
        return readiness, False, None
    reason = (
        f"Safeguard G1: dimension(s) {', '.join(triggered)} "
        f"below {SAFEGUARD_THRESHOLD}; readiness reduced from {readiness:.2f} to {capped:.2f}."
    )
    return capped, True, reason


def compute_ablated_readiness(
    dimension_scores: dict[str, float],
    *,
    excluded_dimensions: frozenset[str],
) -> tuple[float, float, float, bool, str | None]:
    """
    Re-aggregate maturity and readiness excluding dropped dimensions.

    Safeguard G1 applies only to safeguard dimensions still present in the model.
    """
    active = active_dimensions(excluded_dimensions)
    if not active:
        raise ValueError("at least one dimension must remain active")

    active_scores = [dimension_scores[dim_id] for dim_id in active]
    overall = round(sum(active_scores) / len(active_scores), 3)
    readiness_raw = round(100.0 * overall / MAX_SCORE, 2)

    safeguard_dims = SAFEGUARD_DIMENSION_IDS & set(active)
    readiness_final, applied, reason = _apply_safeguard_on_active_dims(
        dimension_scores,
        readiness_raw,
        active_safeguard_dims=safeguard_dims,
    )

    return overall, readiness_raw, readiness_final, applied, reason


def score_profile_ablation(
    spec: ProfileSpec,
    configuration: str,
    excluded_dimensions: frozenset[str],
) -> AblationScore:
    """Score one sensitivity profile under an ablation configuration."""
    payload = build_assessment_payload(
        spec.profile_id,
        dimension_levels=spec.dimension_levels,
        scenario=spec.profile_group,
    )
    full = compute_grb_assessment(payload)
    overall, readiness_raw, readiness_final, applied, _ = compute_ablated_readiness(
        full.dimension_scores,
        excluded_dimensions=excluded_dimensions,
    )
    return AblationScore(
        profile_id=spec.profile_id,
        profile_group=spec.profile_group,
        configuration=configuration,
        excluded_dimensions=excluded_dimensions,
        overall_maturity=overall,
        readiness_raw=readiness_raw,
        readiness_final=readiness_final,
        readiness_band=classify_readiness_band(readiness_final),
        safeguard_applied=applied,
    )


def assign_ranks(scores: list[AblationScore]) -> list[AblationScore]:
    """Rank profiles by final readiness (1 = highest)."""
    readiness = {s.profile_id: s.readiness_final for s in scores}
    ranks = _average_ranks(readiness, higher_is_better=True)
    return [
        AblationScore(
            profile_id=s.profile_id,
            profile_group=s.profile_group,
            configuration=s.configuration,
            excluded_dimensions=s.excluded_dimensions,
            overall_maturity=s.overall_maturity,
            readiness_raw=s.readiness_raw,
            readiness_final=s.readiness_final,
            readiness_band=s.readiness_band,
            safeguard_applied=s.safeguard_applied,
            rank=int(ranks[s.profile_id]),
        )
        for s in scores
    ]


def enrich_with_full_deltas(
    full_scores: list[AblationScore],
    alternate_scores: list[AblationScore],
) -> list[AblationScore]:
    """Attach readiness and safeguard deltas relative to the full model."""
    full_by_id = {s.profile_id: s for s in full_scores}
    enriched: list[AblationScore] = []
    for alt in alternate_scores:
        ref = full_by_id[alt.profile_id]
        enriched.append(
            AblationScore(
                profile_id=alt.profile_id,
                profile_group=alt.profile_group,
                configuration=alt.configuration,
                excluded_dimensions=alt.excluded_dimensions,
                overall_maturity=alt.overall_maturity,
                readiness_raw=alt.readiness_raw,
                readiness_final=alt.readiness_final,
                readiness_band=alt.readiness_band,
                safeguard_applied=alt.safeguard_applied,
                rank=alt.rank,
                readiness_delta_vs_full=round(alt.readiness_final - ref.readiness_final, 2),
                safeguard_delta_vs_full=int(alt.safeguard_applied) - int(ref.safeguard_applied),
            )
        )
    return enriched


def run_ablation_study(
    specs: Sequence[ProfileSpec] | None = None,
) -> tuple[dict[str, list[AblationScore]], list[AblationComparison], dict[str, Any]]:
    """Score all sensitivity profiles under each ablation configuration."""
    profile_specs = list(specs or generate_profile_specs())
    if not profile_specs:
        raise ValueError("no profiles to score")

    by_config: dict[str, list[AblationScore]] = {}
    for config_name, excluded in ABLATION_CONFIGS.items():
        scored = [
            score_profile_ablation(spec, config_name, excluded) for spec in profile_specs
        ]
        by_config[config_name] = assign_ranks(scored)

    full_scores = by_config["full"]
    comparisons: list[AblationComparison] = []
    all_scores: dict[str, list[AblationScore]] = {"full": full_scores}

    for config_name in ABLATION_CONFIGS:
        if config_name == "full":
            continue
        alt_ranked = by_config[config_name]
        alt_enriched = enrich_with_full_deltas(full_scores, alt_ranked)
        all_scores[config_name] = alt_enriched
        comparisons.append(compare_ablation_configurations(full_scores, alt_enriched, config_name))

    summary = build_summary(all_scores, comparisons, profile_count=len(profile_specs))
    return all_scores, comparisons, summary


def compare_ablation_configurations(
    reference: list[AblationScore],
    alternate: list[AblationScore],
    alternate_name: str,
) -> AblationComparison:
    """Compare alternate ablation to full model."""
    ref_by_id = {s.profile_id: s for s in reference}
    alt_by_id = {s.profile_id: s for s in alternate}
    deltas = [
        alt_by_id[pid].readiness_final - ref_by_id[pid].readiness_final
        for pid in sorted(ref_by_id)
    ]
    rank_shifts = {
        pid: alt_by_id[pid].rank - ref_by_id[pid].rank for pid in sorted(ref_by_id)
    }
    safeguard_full = sum(1 for s in reference if s.safeguard_applied)
    safeguard_alt = sum(1 for s in alternate if s.safeguard_applied)
    return AblationComparison(
        reference="full",
        alternate=alternate_name,
        spearman=_spearman(reference, alternate),
        kendall_tau=_kendall(reference, alternate),
        profiles_rank_changed=sum(1 for d in rank_shifts.values() if d != 0),
        total_rank_displacement=sum(abs(d) for d in rank_shifts.values()),
        mean_readiness_delta=round(mean(deltas), 2),
        mean_abs_readiness_delta=round(mean(abs(d) for d in deltas), 2),
        safeguard_applied_full=safeguard_full,
        safeguard_applied_alternate=safeguard_alt,
        safeguard_activation_delta=safeguard_alt - safeguard_full,
    )


def build_summary(
    scores_by_config: dict[str, list[AblationScore]],
    comparisons: list[AblationComparison],
    *,
    profile_count: int,
) -> dict[str, Any]:
    full = scores_by_config["full"]
    return {
        "profile_count": profile_count,
        "grb_version": GRB_SPEC_VERSION,
        "configurations": list(ABLATION_CONFIGS.keys()),
        "full_mean_readiness_final": round(mean(s.readiness_final for s in full), 2),
        "full_safeguard_fraction": round(
            sum(1 for s in full if s.safeguard_applied) / len(full), 4
        ),
        "comparisons": comparisons,
        "safeguard_cap": SAFEGUARD_CAP,
        "safeguard_threshold": SAFEGUARD_THRESHOLD,
    }


CSV_FIELDS: tuple[str, ...] = (
    "record_type",
    "configuration",
    "profile_id",
    "profile_group",
    "excluded_dimensions",
    "overall_maturity",
    "readiness_raw",
    "readiness_final",
    "readiness_band",
    "safeguard_applied",
    "rank",
    "readiness_delta_vs_full",
    "safeguard_delta_vs_full",
    "reference",
    "alternate",
    "spearman",
    "kendall_tau",
    "profiles_rank_changed",
    "total_rank_displacement",
    "mean_readiness_delta",
    "mean_abs_readiness_delta",
    "safeguard_applied_full",
    "safeguard_applied_alternate",
    "safeguard_activation_delta",
)


def build_csv_rows(
    scores_by_config: dict[str, list[AblationScore]],
    comparisons: list[AblationComparison],
    summary: dict[str, Any],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for config_name, scores in scores_by_config.items():
        excluded = ",".join(sorted(ABLATION_CONFIGS[config_name])) or "none"
        for score in scores:
            rows.append(
                {
                    "record_type": "profile",
                    "configuration": config_name,
                    "profile_id": score.profile_id,
                    "profile_group": score.profile_group,
                    "excluded_dimensions": excluded,
                    "overall_maturity": score.overall_maturity,
                    "readiness_raw": score.readiness_raw,
                    "readiness_final": score.readiness_final,
                    "readiness_band": score.readiness_band,
                    "safeguard_applied": score.safeguard_applied,
                    "rank": score.rank,
                    "readiness_delta_vs_full": score.readiness_delta_vs_full
                    if config_name != "full"
                    else "",
                    "safeguard_delta_vs_full": score.safeguard_delta_vs_full
                    if config_name != "full"
                    else "",
                }
            )

    for comp in comparisons:
        rows.append(
            {
                "record_type": "comparison",
                "configuration": "",
                "profile_id": "",
                "profile_group": "",
                "excluded_dimensions": "",
                "reference": comp.reference,
                "alternate": comp.alternate,
                "spearman": f"{comp.spearman:.6f}",
                "kendall_tau": f"{comp.kendall_tau:.6f}",
                "profiles_rank_changed": comp.profiles_rank_changed,
                "total_rank_displacement": comp.total_rank_displacement,
                "mean_readiness_delta": comp.mean_readiness_delta,
                "mean_abs_readiness_delta": comp.mean_abs_readiness_delta,
                "safeguard_applied_full": comp.safeguard_applied_full,
                "safeguard_applied_alternate": comp.safeguard_applied_alternate,
                "safeguard_activation_delta": comp.safeguard_activation_delta,
            }
        )

    rows.append(
        {
            "record_type": "study_meta",
            "configuration": "all",
            "profile_id": "",
            "profile_group": "",
            "excluded_dimensions": "",
            "mean_readiness_delta": summary["full_mean_readiness_final"],
            "safeguard_applied_full": summary["full_safeguard_fraction"],
            "profiles_rank_changed": summary["profile_count"],
        }
    )
    return rows


def render_ablation_report(
    scores_by_config: dict[str, list[AblationScore]],
    comparisons: list[AblationComparison],
    summary: dict[str, Any],
) -> str:
    """Markdown report for GRB ablation study."""
    comp_rows = "\n".join(
        f"| `{c.alternate}` | {c.mean_readiness_delta:+.2f} | {c.mean_abs_readiness_delta:.2f} | "
        f"{c.spearman:.4f} | {c.kendall_tau:.4f} | {c.profiles_rank_changed} | "
        f"{c.safeguard_applied_full} → {c.safeguard_applied_alternate} "
        f"({c.safeguard_activation_delta:+d}) |"
        for c in comparisons
    )

    lines = [
        "# GRB Dimension Ablation Study",
        "",
        "## Objective",
        "",
        "Measure how **readiness**, **profile rankings**, and **safeguard G1 activation** change when "
        "individual GRB dimensions are removed from the aggregation model (structural ablation on "
        "synthetic sensitivity profiles).",
        "",
        "> Frozen GRB specification — synthetic profiles only; not municipal validation.",
        "",
        "## Method",
        "",
        f"- **GRB version:** {summary['grb_version']}",
        f"- **Profiles:** {summary['profile_count']} (deterministic sensitivity set)",
        f"- **Configurations:** {', '.join(f'`{c}`' for c in summary['configurations'])}",
        f"- **Full-model mean readiness (final):** {summary['full_mean_readiness_final']}",
        f"- **Full-model safeguard rate:** {summary['full_safeguard_fraction']:.1%}",
        f"- **Safeguard G1:** cap at {summary['safeguard_cap']} when active D2 or D4 score "
        f"< {summary['safeguard_threshold']}",
        "",
        "### Ablation rules",
        "",
        "| Configuration | Excluded | Active dimensions | Safeguard check |",
        "|---------------|----------|-------------------|-----------------|",
        "| `full` | none | d1–d6 | D2 and D4 |",
        "| `without_d2` | D2 | d1, d3–d6 | D4 only |",
        "| `without_d4` | D4 | d1–d3, d5–d6 | D2 only |",
        "| `without_d6` | D6 | d1–d5 | D2 and D4 |",
        "",
        "Indicator-level scores are unchanged; only the **dimension mean** entering overall maturity "
        "and applicable safeguards are ablated.",
        "",
        "## Comparison vs full model",
        "",
        "| Configuration | Mean Δ readiness | Mean |Δ| | Spearman ρ | Kendall τ | Rank changes | "
        "Safeguard activations |",
        "|---------------|------------------|----------|------------|-----------|--------------|"
        "-----------------------|",
        comp_rows,
        "",
        "## Interpretation notes",
        "",
        "- Removing **D2** eliminates human-oversight maturity from the index and prevents D2 from "
        "triggering G1; profiles with weak D2 may show **higher** readiness under ablation.",
        "- Removing **D4** removes data-legitimacy from the index and D4 safeguard triggers.",
        "- Removing **D6** drops strategic-sovereignty from the mean only; safeguard behaviour matches "
        "the full model.",
        "- Large rank displacement indicates sensitivity of **relative ordering** to dimension set choice.",
        "",
        "## Limitations",
        "",
        "- Uniform within-dimension scores per profile (sensitivity protocol).",
        "- Ablation is a structural stress test, not a normative recommendation to omit dimensions.",
        "- Does not re-run evidence gates item-by-item.",
        "",
        "---",
        "*Generated by `scripts/run_grb_ablation.py`*",
    ]
    return "\n".join(lines)


def _average_ranks(values: dict[str, float], *, higher_is_better: bool) -> dict[str, float]:
    ordered = sorted(
        values.items(),
        key=lambda kv: (-kv[1], kv[0]) if higher_is_better else (kv[1], kv[0]),
    )
    ranks: dict[str, float] = {}
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and ordered[j][1] == ordered[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[ordered[k][0]] = avg_rank
        i = j
    return ranks


def _spearman(reference: list[AblationScore], alternate: list[AblationScore]) -> float:
    ref_ranks = {s.profile_id: float(s.rank) for s in reference}
    alt_ranks = {s.profile_id: float(s.rank) for s in alternate}
    keys = sorted(ref_ranks)
    n = len(keys)
    if n < 2:
        return 1.0
    d_sq = sum((ref_ranks[k] - alt_ranks[k]) ** 2 for k in keys)
    return 1.0 - (6.0 * d_sq) / (n * (n * n - 1))


def _kendall(reference: list[AblationScore], alternate: list[AblationScore]) -> float:
    ref_rank = {s.profile_id: s.rank for s in reference}
    alt_rank = {s.profile_id: s.rank for s in alternate}
    keys = sorted(ref_rank)
    concordant = discordant = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            ref_sign = _pair_sign(ref_rank[a], ref_rank[b])
            alt_sign = _pair_sign(alt_rank[a], alt_rank[b])
            if ref_sign == 0 or alt_sign == 0:
                continue
            if ref_sign == alt_sign:
                concordant += 1
            else:
                discordant += 1
    total = concordant + discordant
    return 1.0 if total == 0 else (concordant - discordant) / total


def _pair_sign(left: int, right: int) -> int:
    if left < right:
        return 1
    if left > right:
        return -1
    return 0
