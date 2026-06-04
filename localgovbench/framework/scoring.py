"""Maturity scoring for the Local AI Governance Framework (v0.1)."""

from __future__ import annotations

from dataclasses import dataclass

from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS, FRAMEWORK_VERSION

MIN_SCORE = 0
MAX_SCORE = 4

# Maturity scale for criterion-level responses (not empirically calibrated in v0.1).
MATURITY_LEVELS: dict[int, tuple[str, str]] = {
    0: ("Absent", "No observable practice for the criterion."),
    1: ("Ad hoc", "Practice exists informally without consistent documentation."),
    2: ("Partially defined", "Documented practice applied inconsistently across teams or sites."),
    3: ("Managed", "Practice is assigned, monitored, and reviewed on a defined cadence."),
    4: ("Optimized", "Practice is evidence-informed with continuous improvement mechanisms."),
}

MATURITY_LABELS: dict[int, str] = {level: label for level, (label, _) in MATURITY_LEVELS.items()}


@dataclass(frozen=True, slots=True)
class MaturityResult:
    """Aggregated maturity scores for an assessment."""

    overall: float
    by_dimension: dict[str, float]
    item_count: int
    framework_version: str = FRAMEWORK_VERSION


def validate_score(score: int | float) -> int:
    """Validate and coerce a maturity score to integer 0–4."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError(f"Score must be numeric, got {type(score).__name__}")
    rounded = int(round(score))
    if rounded < MIN_SCORE or rounded > MAX_SCORE:
        raise ValueError(f"Score must be between {MIN_SCORE} and {MAX_SCORE}, got {rounded}")
    return rounded


def describe_level(level: int) -> tuple[str, str]:
    """Return label and description for a maturity level (0–4)."""
    if level not in MATURITY_LEVELS:
        raise ValueError(f"level must be between {MIN_SCORE} and {MAX_SCORE}, got {level}")
    return MATURITY_LEVELS[level]


def compute_maturity_score(
    responses: dict[str, int | float],
    *,
    dimension_weights: dict[str, float] | None = None,
) -> MaturityResult:
    """
    Compute overall and per-dimension maturity from item_id -> score mappings.

    Item ids are expected from ``build_checklist()`` as
    ``{dimension_id}_{criterion_id}``. Scores use the v0.1 scale (0–4).
    """
    if not responses:
        raise ValueError("responses must not be empty")

    weights = dimension_weights or {d.id: d.weight for d in GOVERNANCE_DIMENSIONS}
    by_dimension_scores: dict[str, list[int]] = {d.id: [] for d in GOVERNANCE_DIMENSIONS}

    validated: list[int] = []
    for item_id, raw in responses.items():
        score = validate_score(raw)
        validated.append(score)
        dimension_id = dimension_id_from_item_id(item_id)
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
    return MaturityResult(
        overall=overall,
        by_dimension=by_dimension,
        item_count=len(validated),
    )


def dimension_id_from_item_id(item_id: str) -> str:
    """Resolve checklist item id to a known governance dimension id."""
    known_ids = tuple(d.id for d in GOVERNANCE_DIMENSIONS)
    for dimension_id in sorted(known_ids, key=len, reverse=True):
        prefix = f"{dimension_id}_"
        if item_id == dimension_id or item_id.startswith(prefix):
            return dimension_id
    if "_" in item_id:
        return item_id.rsplit("_", 1)[0]
    return item_id
