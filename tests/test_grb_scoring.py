"""Tests for GRB scoring experiment."""

from __future__ import annotations

import pytest

from localgovbench.grb.scoring import (
    SAFEGUARD_CAP,
    apply_safeguard_cap,
    check_evidence_rules,
    classify_readiness_band,
    compute_grb_assessment,
)
from localgovbench.grb.specification import (
    SAFEGUARD_DIMENSION_IDS,
    all_indicator_ids,
    indicator_count,
)


def _full_responses(constant: int) -> dict[str, int]:
    return {ind_id: constant for ind_id in all_indicator_ids()}


def test_indicator_count_is_54() -> None:
    assert indicator_count() == 54


def test_score_aggregation_dimension_mean() -> None:
    payload = {
        "metadata": {"municipality": "Test"},
        "responses": _full_responses(3),
        "evidence": {iid: ["E1", "E2"] for iid in all_indicator_ids()},
    }
    result = compute_grb_assessment(payload)
    assert result.overall_maturity == 3.0
    assert result.readiness_raw == 75.0
    assert all(score == 3.0 for score in result.dimension_scores.values())
    assert len(result.subdimension_scores) == 18


def test_readiness_band_classification() -> None:
    assert classify_readiness_band(10.0) == "Not ready"
    assert classify_readiness_band(30.0) == "Emerging"
    assert classify_readiness_band(60.0) == "Substantially ready"
    assert classify_readiness_band(80.0) == "Advanced readiness"


def test_safeguard_cap_when_d2_below_threshold() -> None:
    readiness, applied, reason = apply_safeguard_cap({"d2": 1.5, "d4": 3.0}, 72.0)
    assert applied is True
    assert readiness == SAFEGUARD_CAP
    assert reason is not None
    assert "d2" in reason


def test_safeguard_cap_not_triggered() -> None:
    readiness, applied, _ = apply_safeguard_cap({"d2": 2.5, "d4": 2.0}, 55.0)
    assert applied is False
    assert readiness == 55.0


def test_safeguard_cap_on_full_assessment() -> None:
    responses = _full_responses(4)
    for ind_id in all_indicator_ids():
        if ind_id.startswith("d2_") or ind_id.startswith("d4_"):
            responses[ind_id] = 1
    payload = {
        "metadata": {"municipality": "Cap Test"},
        "responses": responses,
        "evidence": {},
    }
    result = compute_grb_assessment(payload)
    assert result.readiness_raw > SAFEGUARD_CAP
    assert result.readiness_final == SAFEGUARD_CAP
    assert result.safeguard_applied is True


def test_missing_evidence_rule_score_3() -> None:
    issues = check_evidence_rules({"d1_mandate_01": 3}, {"d1_mandate_01": []})
    assert len(issues) == 1
    assert "at least one" in issues[0].message


def test_missing_evidence_rule_score_4_requires_two() -> None:
    issues = check_evidence_rules({"d1_mandate_01": 4}, {"d1_mandate_01": ["only_one"]})
    assert any("two" in i.message for i in issues)


def test_missing_evidence_rule_score_2_ok() -> None:
    issues = check_evidence_rules({"d1_mandate_01": 2}, {})
    assert issues == []


def test_compute_requires_all_indicators() -> None:
    with pytest.raises(ValueError, match="Missing"):
        compute_grb_assessment({"metadata": {}, "responses": {"d1_mandate_01": 2}})


def test_safeguard_dimensions_are_d2_and_d4() -> None:
    assert SAFEGUARD_DIMENSION_IDS == frozenset({"d2", "d4"})
