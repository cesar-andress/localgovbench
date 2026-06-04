"""Tests for maturity scoring."""

from __future__ import annotations

import pytest

from localgovbench.framework.scoring import (
    MATURITY_LABELS,
    compute_maturity_score,
    describe_level,
    dimension_id_from_item_id,
    validate_score,
)


def test_maturity_labels_v01() -> None:
    assert MATURITY_LABELS[1] == "Ad hoc"
    assert MATURITY_LABELS[2] == "Partially defined"
    assert describe_level(3)[0] == "Managed"


def test_validate_score_range() -> None:
    assert validate_score(0) == 0
    assert validate_score(4) == 4
    assert validate_score(3.6) == 4


def test_validate_score_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        validate_score(5)


def test_dimension_id_from_item_id_compound() -> None:
    assert dimension_id_from_item_id("legal_regulatory_gdpr_readiness") == "legal_regulatory"
    assert dimension_id_from_item_id("strategic_sovereignty_portability") == "strategic_sovereignty"


def test_compute_maturity_score() -> None:
    responses = {
        "legal_regulatory_gdpr_readiness": 3,
        "legal_regulatory_ai_act_alignment": 1,
        "technical_security_logging": 4,
        "technical_security_access_control": 2,
    }
    result = compute_maturity_score(responses)
    assert result.item_count == 4
    assert result.framework_version == "0.1"
    assert result.by_dimension["legal_regulatory"] == 2.0
    assert result.by_dimension["technical_security"] == 3.0
    assert 0 <= result.overall <= 4


def test_compute_empty_raises() -> None:
    with pytest.raises(ValueError):
        compute_maturity_score({})
