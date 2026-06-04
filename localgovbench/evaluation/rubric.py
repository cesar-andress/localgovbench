"""Maturity rubric labels and descriptions."""

from __future__ import annotations

MATURITY_LABELS: dict[int, str] = {
    0: "Absent",
    1: "Initial",
    2: "Defined",
    3: "Managed",
    4: "Optimized",
}


def describe_maturity(score: float) -> str:
    """Return a human-readable label for a numeric maturity score (0–4)."""
    if score < 0 or score > 4:
        raise ValueError(f"score must be between 0 and 4, got {score}")
    level = int(round(score))
    level = max(0, min(4, level))
    return MATURITY_LABELS[level]
