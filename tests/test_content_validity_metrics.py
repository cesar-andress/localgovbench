"""Tests for content validity metrics (CVI, CVR)."""

from __future__ import annotations

from localgovbench.validation.content_validity import (
    compute_item_cvi,
    compute_lawshe_cvr,
    compute_scale_cvi_ave,
    load_relevance_survey,
)


def test_item_cvi_perfect_agreement() -> None:
    result = compute_item_cvi("c1", [5, 5, 5, 5, 5, 5])
    assert result.i_cvi == 1.0
    assert result.passes_threshold is True


def test_item_cvi_below_threshold() -> None:
    result = compute_item_cvi("c1", [2, 3, 2, 3, 2, 3])
    assert result.i_cvi < 0.78
    assert result.passes_threshold is False


def test_scale_cvi_ave() -> None:
    scale = compute_scale_cvi_ave(
        {
            "a": [5, 5, 5, 5, 5, 5],
            "b": [4, 4, 5, 5, 4, 5],
        }
    )
    assert 0.0 < scale.s_cvi_ave <= 1.0


def test_lawshe_cvr() -> None:
    result = compute_lawshe_cvr("c1", [True, True, True, True, True, False], minimum_cvr=0.5)
    assert abs(result.cvr - 5 / 6) < 0.01


def test_load_relevance_survey_example() -> None:
    from pathlib import Path

    ratings = load_relevance_survey(
        Path("validation/content_validity/indicator_relevance_survey_results.example.yaml")
    )
    assert "legal_regulatory_gdpr_readiness" in ratings
    assert len(ratings["legal_regulatory_gdpr_readiness"]) >= 3

