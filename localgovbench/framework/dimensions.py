"""Governance dimension definitions for LocalGovBench."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GovernanceDimension:
    """A thematic area of local AI governance."""

    id: str
    name: str
    description: str
    weight: float = 1.0


GOVERNANCE_DIMENSIONS: tuple[GovernanceDimension, ...] = (
    GovernanceDimension(
        id="strategy",
        name="Strategy & leadership",
        description="Political mandate, AI strategy, and executive accountability for AI use.",
    ),
    GovernanceDimension(
        id="risk",
        name="Risk management",
        description="Identification, assessment, and treatment of AI-related risks in public services.",
    ),
    GovernanceDimension(
        id="data",
        name="Data governance",
        description="Lawful, quality-assured, and purpose-limited data used by AI systems.",
    ),
    GovernanceDimension(
        id="transparency",
        name="Transparency & explainability",
        description="Public-facing disclosure and documentation of AI-assisted processes.",
    ),
    GovernanceDimension(
        id="accountability",
        name="Accountability & oversight",
        description="Clear roles, auditability, and human oversight of AI outcomes.",
    ),
    GovernanceDimension(
        id="procurement",
        name="Procurement & vendor management",
        description="Governance of third-party AI products and implementation partners.",
    ),
    GovernanceDimension(
        id="skills",
        name="Skills & capacity",
        description="Training, staffing, and access to interdisciplinary AI expertise.",
    ),
)


def get_dimension(dimension_id: str) -> GovernanceDimension:
    """Return a dimension by id or raise KeyError."""
    for dimension in GOVERNANCE_DIMENSIONS:
        if dimension.id == dimension_id:
            return dimension
    raise KeyError(f"Unknown governance dimension: {dimension_id!r}")
