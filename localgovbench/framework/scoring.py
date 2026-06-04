"""Maturity scoring for governance assessments."""

from __future__ import annotations

from dataclasses import dataclass

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS

MIN_SCORE = 0
MAX_SCORE = 4


@dataclass(frozen=True, slots=True)
class MaturityResult:
    """Aggregated maturity scores for an assessment."""

    overall: float
    by_dimension: dict[str, float]
    item_count: int


def validate_score(score: int | float) -> int:
    """Validate and coerce a maturity score to integer 0–4."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError(f"Score must be numeric, got {type(score).__name__}")
    rounded = int(round(score))
    if rounded < MIN_SCORE or rounded > MAX_SCORE:
        raise ValueError(f"Score must be between {MIN_SCORE} and {MAX_SCORE}, got {rounded}")
    return rounded


def compute_maturity_score(
    responses: dict[str, int | float],
    *,
    dimension_weights: dict[str, float] | None = None,
) -> MaturityResult:
    """
    Compute overall and per-dimension maturity from item_id -> score mappings.

    Item ids are expected to use the prefix ``{dimension_id}_`` as produced by
    ``build_checklist()``. Unknown item ids are ignored for dimension averages
    but still count toward the overall mean if present in *responses*.
    """
    if not responses:
        raise ValueError("responses must not be empty")

    weights = dimension_weights or {d.id: d.weight for d in GOVERNANCE_DIMENSIONS}
    by_dimension_scores: dict[str, list[int]] = {d.id: [] for d in GOVERNANCE_DIMENSIONS}

    validated: list[int] = []
    for item_id, raw in responses.items():
        score = validate_score(raw)
        validated.append(score)
        dimension_id = _dimension_from_item_id(item_id)
        if dimension_id in by_dimension_scores:
            by_dimension_scores[dimension_id].append(score)

    by_dimension: dict[str, float] = {}
    weighted_sum = 0.0
    weight_total = 0.0
    for dimension_id, scores in by_dimension_scores.items():
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        by_dimension[dimension_id] = round(avg, 3)
        w = weights.get(dimension_id, 1.0)
        weighted_sum += avg * w
        weight_total += w

    overall = round(weighted_sum / weight_total, 3) if weight_total else round(
        sum(validated) / len(validated), 3
    )
    return MaturityResult(overall=overall, by_dimension=by_dimension, item_count=len(validated))


def _dimension_from_item_id(item_id: str) -> str:
    """Extract dimension id prefix from a checklist item id."""
    if "_" not in item_id:
        return item_id
    return item_id.rsplit("_", 1)[0]
