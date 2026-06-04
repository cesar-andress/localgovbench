"""Tests for checklist generation."""

from __future__ import annotations

from localgovbench.framework.checklist import build_checklist
from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS


def test_checklist_covers_all_dimensions() -> None:
    checklist = build_checklist()
    dimension_ids = {item.dimension_id for item in checklist}
    expected = {d.id for d in GOVERNANCE_DIMENSIONS}
    assert expected == dimension_ids


def test_checklist_item_ids_unique() -> None:
    checklist = build_checklist()
    ids = [item.id for item in checklist]
    assert len(ids) == len(set(ids))


def test_checklist_item_id_prefix() -> None:
    checklist = build_checklist()
    for item in checklist:
        assert item.id.startswith(f"{item.dimension_id}_")
