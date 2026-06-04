"""Tests for maturity scoring."""

from __future__ import annotations

import pytest

from localgovbench.framework.scoring import (
    compute_maturity_score,
    validate_score,
)


def test_validate_score_range() -> None:
    assert validate_score(0) == 0
    assert validate_score(4) == 4
    assert validate_score(3.6) == 4


def test_validate_score_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        validate_score(5)


def test_compute_maturity_score() -> None:
    responses = {
        "strategy_01": 2,
        "strategy_02": 2,
        "risk_01": 0,
        "risk_02": 0,
    }
    result = compute_maturity_score(responses)
    assert result.item_count == 4
    assert result.by_dimension["strategy"] == 2.0
    assert result.by_dimension["risk"] == 0.0
    assert 0 <= result.overall <= 4


def test_compute_empty_raises() -> None:
    with pytest.raises(ValueError):
        compute_maturity_score({})
