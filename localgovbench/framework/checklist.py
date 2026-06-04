"""Checklist items derived from governance dimensions."""

from __future__ import annotations

from dataclasses import dataclass

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS


@dataclass(frozen=True, slots=True)
class ChecklistItem:
    """A single assessable control within a governance dimension."""

    id: str
    dimension_id: str
    prompt: str
    guidance: str


# Synthetic starter items — expand when empirical instrument is finalized.
_CHECKLIST_SEED: tuple[tuple[str, str, str], ...] = (
    (
        "strategy",
        "Documented local AI policy or roadmap exists.",
        "Look for council resolutions, digital strategy annexes, or mayoral mandates.",
    ),
    (
        "strategy",
        "Executive or political sponsor is named for AI initiatives.",
        "Identify a accountable role for portfolio oversight, not only IT ownership.",
    ),
    (
        "risk",
        "AI use cases are inventoried with risk classification.",
        "Inventory should note affected populations and decision significance.",
    ),
    (
        "risk",
        "Escalation path exists for harmful or biased outcomes.",
        "Include service desk, ethics board, or incident response linkages.",
    ),
    (
        "data",
        "Lawful basis and purpose are recorded for training/operational data.",
        "Cross-check with records of processing and DPIA references.",
    ),
    (
        "data",
        "Data quality and lineage are reviewed before deployment.",
        "Evidence may include data dictionaries or sampling protocols.",
    ),
    (
        "transparency",
        "Citizens can find information on significant AI-assisted services.",
        "Check public websites, privacy notices, and service charters.",
    ),
    (
        "transparency",
        "Limitations of automated outputs are communicated.",
        "Users should see when outputs are probabilistic or incomplete.",
    ),
    (
        "accountability",
        "Service owner is accountable for AI-supported decisions.",
        "Named owners should map to service lines, not vendors alone.",
    ),
    (
        "accountability",
        "Human review is defined where impacts are significant.",
        "Document triggers for manual review and appeal routes.",
    ),
    (
        "procurement",
        "Contracts address AI performance, monitoring, and exit.",
        "Include SLAs, update notification, and model change clauses.",
    ),
    (
        "procurement",
        "Vendor sub-processors and model updates are tracked.",
        "Maintain vendor register entries for AI components.",
    ),
    (
        "skills",
        "Staff receive role-appropriate AI literacy training.",
        "Training should differ for frontline, legal, and technical staff.",
    ),
    (
        "skills",
        "Access to legal/ethical/DPO expertise is established for AI projects.",
        "Early engagement reduces retrofitting of safeguards.",
    ),
)


def build_checklist() -> tuple[ChecklistItem, ...]:
    """Build the default checklist across all governance dimensions."""
    valid_ids = {d.id for d in GOVERNANCE_DIMENSIONS}
    items: list[ChecklistItem] = []
    counters: dict[str, int] = {}
    for dimension_id, prompt, guidance in _CHECKLIST_SEED:
        if dimension_id not in valid_ids:
            raise ValueError(f"Checklist references unknown dimension: {dimension_id}")
        counters[dimension_id] = counters.get(dimension_id, 0) + 1
        item_id = f"{dimension_id}_{counters[dimension_id]:02d}"
        items.append(
            ChecklistItem(
                id=item_id,
                dimension_id=dimension_id,
                prompt=prompt,
                guidance=guidance,
            )
        )
    return tuple(items)
