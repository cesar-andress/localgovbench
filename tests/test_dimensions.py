"""Tests for governance dimensions."""

from __future__ import annotations

import pytest

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS, get_dimension


def test_dimension_count() -> None:
    assert len(GOVERNANCE_DIMENSIONS) == 7


def test_dimension_ids_unique() -> None:
    ids = [d.id for d in GOVERNANCE_DIMENSIONS]
    assert len(ids) == len(set(ids))


def test_get_dimension_known() -> None:
    dim = get_dimension("strategy")
    assert dim.name == "Strategy & leadership"


def test_get_dimension_unknown() -> None:
    with pytest.raises(KeyError):
        get_dimension("nonexistent")
