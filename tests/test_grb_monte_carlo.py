"""Tests for GRB Monte Carlo sensitivity."""

from __future__ import annotations

import random

import pytest

from localgovbench.grb.monte_carlo import (
    DISTRIBUTION_PRESETS,
    ScoreDistribution,
    build_random_responses,
    percentile,
    resolve_distribution,
    run_monte_carlo_study,
    summarize_monte_carlo,
)
from localgovbench.grb.specification import indicator_count


def test_indicator_count_is_54() -> None:
    assert indicator_count() == 54


def test_build_random_responses_range() -> None:
    rng = random.Random(0)
    dist = DISTRIBUTION_PRESETS["uniform"]
    responses = build_random_responses(rng, dist)
    assert len(responses) == 54
    assert all(0 <= score <= 4 for score in responses.values())


def test_score_distribution_rejects_bad_weights() -> None:
    with pytest.raises(ValueError):
        ScoreDistribution("bad", (1.0, 1.0))


def test_percentile_monotonic() -> None:
    values = [float(i) for i in range(101)]
    prev = -1.0
    for p in (5, 25, 50, 75, 95):
        current = percentile(values, p)
        assert current >= prev
        prev = current


def test_run_monte_carlo_small_sample() -> None:
    results, summary = run_monte_carlo_study(
        profile_count=120,
        distribution_name="baseline",
        seed=7,
    )
    assert len(results) == 120
    assert summary["profile_count"] == 120
    assert summary["distribution"] == "baseline"
    assert 0.0 <= summary["safeguard_applied_fraction"] <= 1.0
    assert set(summary["dimension_means"]) == {"d1", "d2", "d3", "d4", "d5", "d6"}
    assert "p50" in summary["percentiles_final"]


def test_mixed_regimes_uses_regime_labels() -> None:
    results, _ = run_monte_carlo_study(
        profile_count=40,
        distribution_name="mixed_regimes",
        seed=1,
    )
    labels = {r.distribution for r in results}
    assert labels.issubset({"uniform", "baseline", "low", "high"})


def test_resolve_distribution_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown distribution"):
        resolve_distribution("nonexistent")


def test_summarize_requires_results() -> None:
    with pytest.raises(ValueError):
        summarize_monte_carlo([], distribution_name="uniform", seed=0)
