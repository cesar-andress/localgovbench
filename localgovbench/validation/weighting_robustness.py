"""Readiness ranking robustness under alternative dimension weights (v0.1 synthetic cases)."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS
from localgovbench.framework.scoring import compute_maturity_score
from localgovbench.validation.discriminant import load_benchmark_case, readiness_index

DIMENSION_IDS: tuple[str, ...] = tuple(d.id for d in GOVERNANCE_DIMENSIONS)

PREDEFINED_WEIGHT_SCHEMES: dict[str, dict[str, float]] = {
    "uniform": {dim_id: 1.0 for dim_id in DIMENSION_IDS},
    "oversight_heavy": {
        "operational": 3.0,
        "organizational": 2.0,
        **{dim_id: 1.0 for dim_id in DIMENSION_IDS if dim_id not in ("operational", "organizational")},
    },
    "data_governance_heavy": {
        "legal_regulatory": 3.0,
        **{dim_id: 1.0 for dim_id in DIMENSION_IDS if dim_id != "legal_regulatory"},
    },
    "sovereignty_heavy": {
        "strategic_sovereignty": 3.0,
        "technical_security": 2.0,
        **{
            dim_id: 1.0
            for dim_id in DIMENSION_IDS
            if dim_id not in ("strategic_sovereignty", "technical_security")
        },
    },
}

DEFAULT_RANDOM_SAMPLES = 1000


@dataclass(frozen=True, slots=True)
class CaseReadiness:
    """Readiness for one benchmark case under a weight configuration."""

    case_id: str
    overall_maturity: float
    readiness_index: float
    rank: int


@dataclass(frozen=True, slots=True)
class RankingComparison:
    """Rank correlation between two weight configurations."""

    reference: str
    alternate: str
    spearman: float
    kendall_tau: float
    cases_rank_changed: int
    total_rank_displacement: int
    rank_shifts: dict[str, int]


def sample_random_weight_sets(
    n_samples: int,
    *,
    seed: int = 42,
) -> list[dict[str, float]]:
    """
    Draw *n_samples* weight vectors from a symmetric Dirichlet on the simplex.

    Scales weights so their sum equals ``len(DIMENSION_IDS)`` (same total mass as uniform).
    """
    rng = random.Random(seed)
    dim_count = len(DIMENSION_IDS)
    samples: list[dict[str, float]] = []
    for _ in range(n_samples):
        draws = [rng.gammavariate(1.0, 1.0) for _ in DIMENSION_IDS]
        total = sum(draws)
        scale = dim_count / total
        samples.append(
            {dim_id: draws[i] * scale for i, dim_id in enumerate(DIMENSION_IDS)}
        )
    return samples


def score_cases(
    cases_dir: Path,
    dimension_weights: dict[str, float],
) -> list[CaseReadiness]:
    """Score all ``municipality_*.yaml`` cases and assign readiness ranks (1 = highest)."""
    scored: list[tuple[str, float, float]] = []
    for path in sorted(cases_dir.glob("municipality_*.yaml")):
        payload = load_benchmark_case(path)
        metadata = payload.get("metadata") or {}
        case_id = str(metadata.get("case_id", path.stem))
        responses = payload.get("responses") or {}
        result = compute_maturity_score(responses, dimension_weights=dimension_weights)
        index = readiness_index(result.overall)
        scored.append((case_id, result.overall, index))

    if not scored:
        raise ValueError(f"No benchmark cases found in {cases_dir}")

    ranks = average_ranks({case_id: idx for case_id, _, idx in scored}, higher_is_better=True)
    return [
        CaseReadiness(
            case_id=case_id,
            overall_maturity=overall,
            readiness_index=index,
            rank=int(ranks[case_id]),
        )
        for case_id, overall, index in scored
    ]


def average_ranks(
    values: dict[str, float],
    *,
    higher_is_better: bool,
) -> dict[str, float]:
    """Assign 1-based average ranks; ties share the mean of occupied positions."""
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


def spearman_rank_correlation(
    reference: Iterable[CaseReadiness],
    alternate: Iterable[CaseReadiness],
) -> float:
    """Spearman rho between readiness rankings (average ranks for ties)."""
    ref_ranks = {c.case_id: float(c.rank) for c in reference}
    alt_ranks = {c.case_id: float(c.rank) for c in alternate}
    keys = sorted(ref_ranks.keys())
    n = len(keys)
    if n < 2:
        return 1.0
    d_sq = sum((ref_ranks[k] - alt_ranks[k]) ** 2 for k in keys)
    return 1.0 - (6.0 * d_sq) / (n * (n * n - 1))


def kendall_tau(
    reference: Iterable[CaseReadiness],
    alternate: Iterable[CaseReadiness],
) -> float:
    """Kendall tau-a on pairwise order concordance (ties ignored in pairs)."""
    ref_rank = {c.case_id: c.rank for c in reference}
    alt_rank = {c.case_id: c.rank for c in alternate}
    keys = sorted(ref_rank.keys())
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
    if total == 0:
        return 1.0
    return (concordant - discordant) / total


def _pair_sign(left: int, right: int) -> int:
    if left < right:
        return 1
    if left > right:
        return -1
    return 0


def compare_rankings(
    reference: list[CaseReadiness],
    alternate: list[CaseReadiness],
    *,
    reference_name: str,
    alternate_name: str,
) -> RankingComparison:
    """Compare alternate rankings to a reference configuration."""
    ref_by_id = {c.case_id: c for c in reference}
    alt_by_id = {c.case_id: c for c in alternate}
    shifts = {
        case_id: alt_by_id[case_id].rank - ref_by_id[case_id].rank
        for case_id in sorted(ref_by_id.keys())
    }
    changed = sum(1 for delta in shifts.values() if delta != 0)
    displacement = sum(abs(delta) for delta in shifts.values())
    return RankingComparison(
        reference=reference_name,
        alternate=alternate_name,
        spearman=spearman_rank_correlation(reference, alternate),
        kendall_tau=kendall_tau(reference, alternate),
        cases_rank_changed=changed,
        total_rank_displacement=displacement,
        rank_shifts=shifts,
    )


def run_weighting_robustness(
    cases_dir: Path,
    *,
    random_samples: int = DEFAULT_RANDOM_SAMPLES,
    seed: int = 42,
) -> tuple[dict[str, list[CaseReadiness]], list[RankingComparison], dict[str, Any]]:
    """
    Score cases under predefined and random weights; compare all to uniform baseline.

    Returns (scores_by_config, comparisons_vs_uniform, random_summary).
    """
    scores: dict[str, list[CaseReadiness]] = {}
    for name, weights in PREDEFINED_WEIGHT_SCHEMES.items():
        scores[name] = score_cases(cases_dir, weights)

    random_comparisons: list[RankingComparison] = []
    uniform = scores["uniform"]
    for idx, weights in enumerate(sample_random_weight_sets(random_samples, seed=seed)):
        alt = score_cases(cases_dir, weights)
        random_comparisons.append(
            compare_rankings(
                uniform,
                alt,
                reference_name="uniform",
                alternate_name=f"random_{idx:04d}",
            )
        )

    comparisons: list[RankingComparison] = []
    for name in PREDEFINED_WEIGHT_SCHEMES:
        if name == "uniform":
            continue
        comparisons.append(
            compare_rankings(
                uniform,
                scores[name],
                reference_name="uniform",
                alternate_name=name,
            )
        )

    spearman_vals = [c.spearman for c in random_comparisons]
    kendall_vals = [c.kendall_tau for c in random_comparisons]
    random_summary = {
        "sample_count": random_samples,
        "seed": seed,
        "spearman_mean": _mean(spearman_vals),
        "spearman_min": min(spearman_vals),
        "spearman_std": _std(spearman_vals),
        "kendall_mean": _mean(kendall_vals),
        "kendall_min": min(kendall_vals),
        "kendall_std": _std(kendall_vals),
        "perfect_spearman_fraction": sum(1 for v in spearman_vals if math.isclose(v, 1.0)) / len(
            spearman_vals
        ),
        "cases_rank_changed_mean": _mean([c.cases_rank_changed for c in random_comparisons]),
    }

    return scores, comparisons, random_summary


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = _mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)
