"""Tests for governance dimensions."""

from __future__ import annotations

import pytest

from localgovbench.framework.dimensions import (
    FRAMEWORK_VERSION,
    GOVERNANCE_DIMENSIONS,
    get_criterion,
    get_dimension,
)


def test_framework_version() -> None:
    assert FRAMEWORK_VERSION == "0.1"


def test_dimension_count() -> None:
    assert len(GOVERNANCE_DIMENSIONS) == 5


def test_dimension_ids_unique() -> None:
    ids = [d.id for d in GOVERNANCE_DIMENSIONS]
    assert len(ids) == len(set(ids))


def test_each_dimension_has_five_criteria() -> None:
    for dimension in GOVERNANCE_DIMENSIONS:
        assert len(dimension.criteria) == 5
        criterion_ids = [c.id for c in dimension.criteria]
        assert len(criterion_ids) == len(set(criterion_ids))


def test_criterion_has_evidence_and_risk() -> None:
    criterion = get_criterion("legal_regulatory", "gdpr_readiness")
    assert criterion.suggested_evidence
    assert criterion.risk_if_missing


def test_get_dimension_known() -> None:
    dim = get_dimension("technical_security")
    assert dim.name == "Technical and Security Readiness"


def test_get_dimension_unknown() -> None:
    with pytest.raises(KeyError):
        get_dimension("nonexistent")


def test_get_criterion_unknown() -> None:
    with pytest.raises(KeyError):
        get_criterion("operational", "nonexistent")
