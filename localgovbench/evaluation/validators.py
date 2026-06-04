"""Validators for assessment payloads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from localgovbench.framework.scoring import MAX_SCORE, MIN_SCORE


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single validation finding."""

    field: str
    message: str


def validate_assessment(payload: dict[str, Any]) -> list[ValidationIssue]:
    """
    Validate a minimal assessment document structure.

    Expected keys: ``metadata``, ``responses`` (item_id -> score).
    """
    issues: list[ValidationIssue] = []

    if "metadata" not in payload:
        issues.append(ValidationIssue("metadata", "Missing required section 'metadata'."))
    elif not isinstance(payload["metadata"], dict):
        issues.append(ValidationIssue("metadata", "'metadata' must be a mapping."))

    responses = payload.get("responses")
    if responses is None:
        issues.append(ValidationIssue("responses", "Missing required section 'responses'."))
        return issues
    if not isinstance(responses, dict):
        issues.append(ValidationIssue("responses", "'responses' must be a mapping."))
        return issues
    if not responses:
        issues.append(ValidationIssue("responses", "'responses' must not be empty."))

    for item_id, score in responses.items():
        if not isinstance(item_id, str):
            issues.append(
                ValidationIssue("responses", f"Item key must be str, got {type(item_id).__name__}.")
            )
            continue
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            issues.append(
                ValidationIssue(
                    f"responses.{item_id}",
                    f"Score must be numeric, got {type(score).__name__}.",
                )
            )
            continue
        rounded = int(round(score))
        if rounded < MIN_SCORE or rounded > MAX_SCORE:
            issues.append(
                ValidationIssue(
                    f"responses.{item_id}",
                    f"Score must be between {MIN_SCORE} and {MAX_SCORE}.",
                )
            )

    metadata = payload.get("metadata")
    if isinstance(metadata, dict):
        synthetic = metadata.get("synthetic")
        if synthetic is not True:
            issues.append(
                ValidationIssue(
                    "metadata.synthetic",
                    "Early-stage releases require metadata.synthetic: true for sample data.",
                )
            )

    return issues
