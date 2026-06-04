"""Tests for checklist generation."""

from __future__ import annotations

from localgovbench.framework.checklist import build_checklist, checklist_framework_version
from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS


def test_checklist_framework_version() -> None:
    assert checklist_framework_version() == "0.1"


def test_checklist_item_count() -> None:
    checklist = build_checklist()
    assert len(checklist) == 25


def test_checklist_covers_all_dimensions() -> None:
    checklist = build_checklist()
    dimension_ids = {item.dimension_id for item in checklist}
    expected = {d.id for d in GOVERNANCE_DIMENSIONS}
    assert expected == dimension_ids


def test_checklist_item_ids_unique() -> None:
    checklist = build_checklist()
    ids = [item.id for item in checklist]
    assert len(ids) == len(set(ids))


def test_checklist_item_matches_criteria() -> None:
    checklist = build_checklist()
    for item in checklist:
        assert item.id == f"{item.dimension_id}_{item.criterion_id}"
        assert item.prompt
        assert item.guidance
        assert item.risk_if_missing
