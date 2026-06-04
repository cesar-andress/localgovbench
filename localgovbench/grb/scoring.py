"""GRB scoring, readiness bands, safeguard cap, and evidence rules."""

from __future__ import annotations

from dataclasses import dataclass, field

from localgovbench.grb.specification import (
    GRB_SPEC_VERSION,
    GRB_DIMENSIONS,
    SAFEGUARD_DIMENSION_IDS,
    all_indicator_ids,
)

MIN_SCORE = 0
MAX_SCORE = 4
SAFEGUARD_CAP = 60.0
SAFEGUARD_THRESHOLD = 2.0


@dataclass(frozen=True, slots=True)
class ReadinessBand:
    """Readiness band on 0–100 scale."""

    label: str
    min_score: float
    max_score: float


READINESS_BANDS: tuple[ReadinessBand, ...] = (
    ReadinessBand("Not ready", 0.0, 24.0),
    ReadinessBand("Emerging", 25.0, 49.0),
    ReadinessBand("Substantially ready", 50.0, 74.0),
    ReadinessBand("Advanced readiness", 75.0, 100.0),
)


@dataclass(frozen=True, slots=True)
class EvidenceIssue:
    """Missing or insufficient evidence for a scored indicator."""

    indicator_id: str
    score: int
    message: str


@dataclass
class GRBAssessmentResult:
    """Full GRB assessment output."""

    municipality: str
    framework_version: str
    indicator_scores: dict[str, int]
    subdimension_scores: dict[str, float]
    dimension_scores: dict[str, float]
    overall_maturity: float
    readiness_raw: float
    readiness_final: float
    readiness_band: str
    safeguard_applied: bool
    safeguard_reason: str | None
    evidence_issues: list[EvidenceIssue] = field(default_factory=list)


def validate_indicator_score(score: int | float) -> int:
    """Coerce and validate a maturity score (0–4)."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError(f"Score must be numeric, got {type(score).__name__}")
    rounded = int(round(score))
    if rounded < MIN_SCORE or rounded > MAX_SCORE:
        raise ValueError(f"Score must be between {MIN_SCORE} and {MAX_SCORE}, got {rounded}")
    return rounded


def check_evidence_rules(
    responses: dict[str, int | float],
    evidence: dict[str, list[str]] | None,
) -> list[EvidenceIssue]:
    """
    Evidence gate (E2): scores >= 3 require at least one evidence reference.

    Scores 4 additionally require >= 2 references (E3) in this experiment.
    """
    issues: list[EvidenceIssue] = []
    evidence = evidence or {}
    for indicator_id, raw in responses.items():
        score = validate_indicator_score(raw)
        refs = evidence.get(indicator_id, [])
        if score >= 3 and len(refs) < 1:
            issues.append(
                EvidenceIssue(
                    indicator_id=indicator_id,
                    score=score,
                    message="Score >= 3 requires at least one evidence reference.",
                )
            )
        if score >= 4 and len(refs) < 2:
            issues.append(
                EvidenceIssue(
                    indicator_id=indicator_id,
                    score=score,
                    message="Score 4 requires at least two evidence references.",
                )
            )
    return issues


def apply_safeguard_cap(
    dimension_scores: dict[str, float],
    readiness: float,
    *,
    threshold: float = SAFEGUARD_THRESHOLD,
    cap: float = SAFEGUARD_CAP,
) -> tuple[float, bool, str | None]:
    """
    Rule G1: if D2 or D4 dimension maturity < threshold, cap readiness at *cap*.
    """
    triggered_dims = [
        dim_id
        for dim_id in SAFEGUARD_DIMENSION_IDS
        if dimension_scores.get(dim_id, 0.0) < threshold
    ]
    if not triggered_dims:
        return readiness, False, None
    capped = min(readiness, cap)
    if capped >= readiness:
        return readiness, False, None
    reason = (
        f"Safeguard G1: dimension(s) {', '.join(sorted(triggered_dims))} "
        f"below {threshold}; readiness reduced from {readiness:.2f} to {capped:.2f}."
    )
    return capped, True, reason


def classify_readiness_band(readiness: float) -> str:
    """Map readiness index (0–100) to band label."""
    for band in READINESS_BANDS:
        if band.min_score <= readiness <= band.max_score:
            return band.label
    if readiness < 0:
        raise ValueError("readiness must be non-negative")
    return READINESS_BANDS[-1].label


def compute_grb_assessment(
    payload: dict,
    *,
    specification: tuple | None = None,
) -> GRBAssessmentResult:
    """
    Compute subdimension, dimension, and readiness scores from assessment YAML payload.

    Expected keys: ``metadata``, ``responses`` (54 indicators), optional ``evidence``.
    """
    spec = specification or GRB_DIMENSIONS
    metadata = payload.get("metadata") or {}
    responses = payload.get("responses") or {}
    evidence = payload.get("evidence")

    expected_ids = set(all_indicator_ids())
    provided_ids = set(responses.keys())
    missing = expected_ids - provided_ids
    extra = provided_ids - expected_ids
    if missing:
        raise ValueError(f"Missing {len(missing)} indicator scores: {sorted(missing)[:5]}...")
    if extra:
        raise ValueError(f"Unknown indicator ids: {sorted(extra)[:5]}...")

    indicator_scores: dict[str, int] = {
        ind_id: validate_indicator_score(responses[ind_id]) for ind_id in expected_ids
    }

    subdimension_scores: dict[str, float] = {}
    dimension_scores: dict[str, float] = {}

    for dimension in spec:
        dim_indicator_scores: list[int] = []
        for subdimension in dimension.subdimensions:
            sub_scores = [indicator_scores[i.id] for i in subdimension.indicators]
            sub_key = f"{dimension.id}_{subdimension.id}"
            subdimension_scores[sub_key] = round(sum(sub_scores) / len(sub_scores), 3)
            dim_indicator_scores.extend(sub_scores)
        dimension_scores[dimension.id] = round(
            sum(dim_indicator_scores) / len(dim_indicator_scores), 3
        )

    overall_maturity = round(
        sum(dimension_scores.values()) / len(dimension_scores), 3
    )
    readiness_raw = round(100.0 * overall_maturity / MAX_SCORE, 2)
    readiness_final, safeguard_applied, safeguard_reason = apply_safeguard_cap(
        dimension_scores, readiness_raw
    )
    evidence_issues = check_evidence_rules(indicator_scores, evidence)

    return GRBAssessmentResult(
        municipality=str(metadata.get("municipality", metadata.get("title", "Unknown"))),
        framework_version=str(metadata.get("grb_version", GRB_SPEC_VERSION)),
        indicator_scores=indicator_scores,
        subdimension_scores=subdimension_scores,
        dimension_scores=dimension_scores,
        overall_maturity=overall_maturity,
        readiness_raw=readiness_raw,
        readiness_final=readiness_final,
        readiness_band=classify_readiness_band(readiness_final),
        safeguard_applied=safeguard_applied,
        safeguard_reason=safeguard_reason,
        evidence_issues=evidence_issues,
    )


def render_markdown_report(result: GRBAssessmentResult) -> str:
    """Render assessment result as Markdown."""
    lines = [
        "# GRB Assessment Report",
        "",
        f"**Municipality:** {result.municipality}",
        f"**GRB version:** {result.framework_version}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Overall maturity (0–4) | {result.overall_maturity} |",
        f"| Readiness (raw, 0–100) | {result.readiness_raw} |",
        f"| Readiness (final, 0–100) | {result.readiness_final} |",
        f"| Readiness band | {result.readiness_band} |",
        f"| Safeguard G1 applied | {result.safeguard_applied} |",
        "",
    ]
    if result.safeguard_reason:
        lines.extend([f"> {result.safeguard_reason}", ""])

    lines.extend(["## Dimension scores", "", "| Dimension | Score (0–4) |", "|-----------|-------------|"])
    for dim_id in sorted(result.dimension_scores):
        lines.append(f"| `{dim_id}` | {result.dimension_scores[dim_id]} |")
    lines.append("")

    lines.extend(["## Subdimension scores", "", "| Subdimension | Score (0–4) |", "|--------------|-------------|"])
    for sub_id in sorted(result.subdimension_scores):
        lines.append(f"| `{sub_id}` | {result.subdimension_scores[sub_id]} |")
    lines.append("")

    if result.evidence_issues:
        lines.extend(["## Evidence issues", ""])
        for issue in result.evidence_issues:
            lines.append(f"- `{issue.indicator_id}` (score {issue.score}): {issue.message}")
        lines.append("")
    else:
        lines.extend(["## Evidence issues", "", "None detected under E2/E3 rules.", ""])

    lines.append("---")
    lines.append("*Synthetic validation experiment — not empirical field data.*")
    return "\n".join(lines)
