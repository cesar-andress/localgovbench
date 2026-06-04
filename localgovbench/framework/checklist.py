"""Checklist generation from Local AI Governance Framework (v0.1) dimensions."""

from __future__ import annotations

from dataclasses import dataclass

from localgovbench.framework.dimensions import (
    FRAMEWORK_VERSION,
    GOVERNANCE_DIMENSIONS,
    GovernanceCriterion,
    GovernanceDimension,
)


@dataclass(frozen=True, slots=True)
class ChecklistItem:
    """A single assessable control within a governance dimension."""

    id: str
    dimension_id: str
    criterion_id: str
    prompt: str
    guidance: str
    risk_if_missing: str


def build_checklist() -> tuple[ChecklistItem, ...]:
    """
    Build the v0.1 checklist from framework criteria (one item per criterion).

    Item ids follow ``{dimension_id}_{criterion_id}``.
    """
    items: list[ChecklistItem] = []
    for dimension in GOVERNANCE_DIMENSIONS:
        items.extend(_items_for_dimension(dimension))
    return tuple(items)


def _items_for_dimension(dimension: GovernanceDimension) -> list[ChecklistItem]:
    result: list[ChecklistItem] = []
    for criterion in dimension.criteria:
        result.append(_criterion_to_item(dimension, criterion))
    return result


def _criterion_to_item(
    dimension: GovernanceDimension,
    criterion: GovernanceCriterion,
) -> ChecklistItem:
    item_id = f"{dimension.id}_{criterion.id}"
    return ChecklistItem(
        id=item_id,
        dimension_id=dimension.id,
        criterion_id=criterion.id,
        prompt=criterion.statement,
        guidance=criterion.suggested_evidence,
        risk_if_missing=criterion.risk_if_missing,
    )


def checklist_framework_version() -> str:
    """Return the framework version associated with generated checklists."""
    return FRAMEWORK_VERSION
