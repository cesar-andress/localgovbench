"""Maturity rubric labels and descriptions."""

from __future__ import annotations

from localgovbench.framework.scoring import MATURITY_LABELS, describe_level


def describe_maturity(score: float) -> str:
    """Return a human-readable label for a numeric maturity score (0–4)."""
    if score < 0 or score > 4:
        raise ValueError(f"score must be between 0 and 4, got {score}")
    level = int(round(score))
    level = max(0, min(4, level))
    return MATURITY_LABELS[level]


__all__ = ["MATURITY_LABELS", "describe_level", "describe_maturity"]
