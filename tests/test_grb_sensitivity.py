"""Tests for GRB sensitivity analysis helpers."""

from __future__ import annotations

from localgovbench.grb.profiles import build_responses
from localgovbench.grb.scoring import SAFEGUARD_CAP, compute_grb_assessment
from localgovbench.grb.specification import all_indicator_ids


def test_build_responses_has_54_indicators() -> None:
    responses = build_responses(dimension_levels={"d2": 2})
    assert len(responses) == 54
    assert all(ind.startswith("d2_") for ind in responses if responses[ind] == 2)


def test_d6_increase_raises_readiness() -> None:
    low = compute_grb_assessment(
        {
            "metadata": {"municipality": "A"},
            "responses": build_responses(dimension_levels={"d6": 1}),
        }
    )
    high = compute_grb_assessment(
        {
            "metadata": {"municipality": "B"},
            "responses": build_responses(dimension_levels={"d6": 4}),
        }
    )
    assert high.readiness_final > low.readiness_final


def test_d2_decrease_lowers_readiness_without_cap_when_raw_below_60() -> None:
    high = compute_grb_assessment(
        {
            "metadata": {"municipality": "A"},
            "responses": build_responses(dimension_levels={"d2": 4}),
        }
    )
    low = compute_grb_assessment(
        {
            "metadata": {"municipality": "B"},
            "responses": build_responses(dimension_levels={"d2": 0}),
        }
    )
    assert low.readiness_final < high.readiness_final


def test_d2_weak_with_strong_baseline_triggers_safeguard() -> None:
    result = compute_grb_assessment(
        {
            "metadata": {"municipality": "Cap"},
            "responses": build_responses(dimension_levels={"d2": 1}, default_level=4),
        }
    )
    assert result.readiness_raw > SAFEGUARD_CAP
    assert result.readiness_final == SAFEGUARD_CAP
    assert result.safeguard_applied is True
