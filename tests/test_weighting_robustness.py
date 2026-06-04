"""Tests for readiness weighting robustness analysis."""

from __future__ import annotations

from pathlib import Path

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS
from localgovbench.validation.weighting_robustness import (
    PREDEFINED_WEIGHT_SCHEMES,
    compare_rankings,
    kendall_tau,
    run_weighting_robustness,
    sample_random_weight_sets,
    score_cases,
    spearman_rank_correlation,
)

CASES_DIR = Path("validation/benchmark_cases")


def test_predefined_schemes_cover_all_dimensions() -> None:
    for name, weights in PREDEFINED_WEIGHT_SCHEMES.items():
        assert set(weights.keys()) == {d.id for d in GOVERNANCE_DIMENSIONS}


def test_uniform_matches_default_scoring_ranks() -> None:
    uniform = score_cases(CASES_DIR, PREDEFINED_WEIGHT_SCHEMES["uniform"])
    assert len(uniform) == 5
    by_id = {c.case_id: c for c in uniform}
    assert by_id["municipality_low_readiness"].rank == 5
    assert by_id["municipality_sovereign_ready"].rank == 1


def test_self_correlation_is_perfect() -> None:
    uniform = score_cases(CASES_DIR, PREDEFINED_WEIGHT_SCHEMES["uniform"])
    assert spearman_rank_correlation(uniform, uniform) == 1.0
    assert kendall_tau(uniform, uniform) == 1.0


def test_run_robustness_predefined_vs_uniform() -> None:
    scores, comparisons, random_summary = run_weighting_robustness(
        CASES_DIR, random_samples=50, seed=7
    )
    assert set(scores.keys()) == set(PREDEFINED_WEIGHT_SCHEMES.keys())
    assert len(comparisons) == 3
    for comp in comparisons:
        assert comp.reference == "uniform"
        assert -1.0 <= comp.spearman <= 1.0
        assert -1.0 <= comp.kendall_tau <= 1.0
    assert random_summary["sample_count"] == 50
    assert random_summary["spearman_mean"] >= random_summary["spearman_min"]


def test_random_weight_sets_sum_to_dimension_count() -> None:
    dim_count = len(PREDEFINED_WEIGHT_SCHEMES["uniform"])
    for weights in sample_random_weight_sets(20, seed=1):
        assert abs(sum(weights.values()) - dim_count) < 1e-9


def test_compare_rankings_displacement() -> None:
    uniform = score_cases(CASES_DIR, PREDEFINED_WEIGHT_SCHEMES["uniform"])
    comp = compare_rankings(
        uniform,
        uniform,
        reference_name="uniform",
        alternate_name="uniform",
    )
    assert comp.cases_rank_changed == 0
    assert comp.total_rank_displacement == 0
