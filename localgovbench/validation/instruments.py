"""LocalGovBench instrument registry (v0.1 — 25 criteria, five dimensions)."""

from __future__ import annotations

from dataclasses import dataclass

from localgovbench.framework.checklist import build_checklist
from localgovbench.framework.dimensions import FRAMEWORK_VERSION

INSTRUMENT_V01 = "localgovbench-v0.1"


@dataclass(frozen=True, slots=True)
class InstrumentSpec:
    """Registered benchmark instrument."""

    id: str
    framework_version: str
    criterion_ids: tuple[str, ...]
    dimension_ids: tuple[str, ...]


def all_criterion_ids() -> tuple[str, ...]:
    """Return checklist item ids for LocalGovBench v0.1."""
    return tuple(item.id for item in build_checklist())


def get_instrument(instrument_id: str = INSTRUMENT_V01) -> InstrumentSpec:
    """Return instrument metadata."""
    if instrument_id != INSTRUMENT_V01:
        raise KeyError(f"Unknown instrument: {instrument_id!r}")
    checklist = build_checklist()
    dimension_ids = tuple(dict.fromkeys(item.dimension_id for item in checklist))
    return InstrumentSpec(
        id=INSTRUMENT_V01,
        framework_version=FRAMEWORK_VERSION,
        criterion_ids=tuple(item.id for item in checklist),
        dimension_ids=dimension_ids,
    )
