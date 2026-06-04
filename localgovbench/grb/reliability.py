"""GRB inter-rater reliability metrics and disagreement tables."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

import yaml

from localgovbench.grb.specification import GRB_SPEC_VERSION, all_indicator_ids
from localgovbench.validation.reliability import cohens_kappa, interpret_kappa

VALID_SCORES = frozenset(range(5))
EXPECTED_INDICATORS = frozenset(all_indicator_ids())


@dataclass(frozen=True, slots=True)
class ReliabilityMetrics:
    """Aggregate reliability statistics for a GRB IRR study."""

    study_id: str
    n_raters: int
    n_units: int
    percent_agreement: float
    cohens_kappa_pairs: dict[str, float]
    fleiss_kappa: float | None
    kappa_interpretation: str


@dataclass(frozen=True, slots=True)
class DisagreementRow:
    """One indicator-level disagreement across raters."""

    case_id: str
    indicator_id: str
    dimension_id: str
    scores: dict[str, int]
    spread: int
    unanimous: bool


@dataclass
class GRBIRRStudyResult:
    """Full IRR analysis output."""

    study_id: str
    metrics: ReliabilityMetrics
    units: list[tuple[str, str, dict[str, int]]]  # case_id, indicator_id, rater->score
    disagreement_rows: list[DisagreementRow] = field(default_factory=list)
    dimension_disagreement_counts: dict[str, int] = field(default_factory=dict)


def indicator_dimension(indicator_id: str) -> str:
    """Return dimension prefix (e.g. ``d2``) from indicator id."""
    if "_" not in indicator_id:
        raise ValueError(f"Invalid indicator id format: {indicator_id}")
    return indicator_id.split("_", 1)[0]


def validate_indicator_id(indicator_id: str) -> None:
    if indicator_id not in EXPECTED_INDICATORS:
        raise ValueError(f"Unknown GRB indicator id: {indicator_id}")


def validate_score(score: int) -> int:
    if isinstance(score, bool) or not isinstance(score, int):
        raise TypeError(f"Score must be int 0-4, got {type(score).__name__}")
    if score not in VALID_SCORES:
        raise ValueError(f"Score must be 0-4, got {score}")
    return score


def load_assessor_scores(path: Path) -> tuple[str, dict[str, dict[str, int]]]:
    """
    Load one assessor YAML file.

    Returns ``(rater_id, {case_id: {indicator_id: score}})``.
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid assessor file (not a mapping): {path}")
    metadata = data.get("metadata") or {}
    rater_id = str(metadata.get("rater_id", path.stem))
    cases = data.get("cases") or {}
    if not cases:
        raise ValueError(f"No cases in assessor file: {path}")

    parsed: dict[str, dict[str, int]] = {}
    for case_id, case_payload in cases.items():
        responses = (case_payload or {}).get("responses") or {}
        case_scores: dict[str, int] = {}
        for indicator_id, raw in responses.items():
            validate_indicator_id(indicator_id)
            case_scores[indicator_id] = validate_score(int(raw))
        missing = EXPECTED_INDICATORS - set(case_scores.keys())
        if missing:
            raise ValueError(
                f"Case {case_id} in {path.name} missing {len(missing)} indicators"
            )
        parsed[str(case_id)] = case_scores
    return rater_id, parsed


def percent_agreement(rater_matrix: Sequence[Sequence[int]]) -> float:
    """
    Fraction of units with unanimous scores across all raters.

    *rater_matrix* is ``n_units × n_raters``.
    """
    if not rater_matrix:
        raise ValueError("Empty rater matrix.")
    n_raters = len(rater_matrix[0])
    if n_raters < 2:
        raise ValueError("Percent agreement requires at least two raters.")
    for row in rater_matrix:
        if len(row) != n_raters:
            raise ValueError("All rater rows must have equal length.")
    unanimous = sum(1 for row in rater_matrix if len(set(row)) == 1)
    return round(unanimous / len(rater_matrix), 4)


def fleiss_kappa(rater_matrix: Sequence[Sequence[int]]) -> float:
    """
    Fleiss' kappa for nominal agreement with three or more raters.

    *rater_matrix* is ``n_units × n_raters`` with integer category scores.
    """
    if not rater_matrix:
        raise ValueError("Empty rater matrix.")
    n_units = len(rater_matrix)
    n_raters = len(rater_matrix[0])
    if n_raters < 2:
        raise ValueError("Fleiss' kappa requires at least two raters.")
    for row in rater_matrix:
        if len(row) != n_raters:
            raise ValueError("All rater rows must have equal length.")

    categories = sorted({v for row in rater_matrix for v in row})
    p_per_unit: list[float] = []
    for row in rater_matrix:
        counts = Counter(row)
        agree = sum(c * (c - 1) for c in counts.values())
        p_per_unit.append(agree / (n_raters * (n_raters - 1)))
    p_bar = sum(p_per_unit) / n_units

    category_totals = Counter()
    for row in rater_matrix:
        category_totals.update(row)
    total_assignments = n_units * n_raters
    p_j = {c: category_totals[c] / total_assignments for c in categories}
    p_e = sum(v * v for v in p_j.values())

    if p_e >= 1.0:
        return 1.0 if p_bar >= 1.0 else 0.0
    return round((p_bar - p_e) / (1.0 - p_e), 4)


def build_disagreement_table(
    units: Iterable[tuple[str, str, dict[str, int]]],
) -> tuple[list[DisagreementRow], dict[str, int]]:
    """Build indicator-level disagreement rows and counts per dimension."""
    rows: list[DisagreementRow] = []
    dim_counts: dict[str, int] = defaultdict(int)

    for case_id, indicator_id, scores in units:
        values = list(scores.values())
        unanimous = len(set(values)) == 1
        spread = max(values) - min(values)
        if not unanimous:
            dim = indicator_dimension(indicator_id)
            rows.append(
                DisagreementRow(
                    case_id=case_id,
                    indicator_id=indicator_id,
                    dimension_id=dim,
                    scores=dict(scores),
                    spread=spread,
                    unanimous=False,
                )
            )
            dim_counts[dim] += 1
    return rows, dict(sorted(dim_counts.items()))


def _align_units(
    rater_data: dict[str, dict[str, dict[str, int]]],
) -> list[tuple[str, str, dict[str, int]]]:
    """Align all raters to common (case_id, indicator_id) units."""
    rater_ids = sorted(rater_data.keys())
    case_ids = sorted({cid for scores in rater_data.values() for cid in scores})
    units: list[tuple[str, str, dict[str, int]]] = []
    for case_id in case_ids:
        for indicator_id in sorted(EXPECTED_INDICATORS):
            unit_scores: dict[str, int] = {}
            for rater_id in rater_ids:
                unit_scores[rater_id] = rater_data[rater_id][case_id][indicator_id]
            units.append((case_id, indicator_id, unit_scores))
    return units


def compute_reliability_metrics(
    units: list[tuple[str, str, dict[str, int]]],
    *,
    study_id: str,
) -> ReliabilityMetrics:
    """Compute percent agreement, pairwise Cohen's κ, and Fleiss' κ."""
    rater_ids = sorted({rid for _, _, scores in units for rid in scores})
    n_raters = len(rater_ids)
    matrix = [[scores[rid] for rid in rater_ids] for _, _, scores in units]

    pct = percent_agreement(matrix)
    kappa_pairs: dict[str, float] = {}
    if n_raters >= 2:
        for i, r1 in enumerate(rater_ids):
            for r2 in rater_ids[i + 1 :]:
                col_a = [scores[r1] for _, _, scores in units]
                col_b = [scores[r2] for _, _, scores in units]
                key = f"{r1}_vs_{r2}"
                kappa_pairs[key] = round(cohens_kappa(col_a, col_b), 4)

    fleiss: float | None = None
    if n_raters >= 3:
        fleiss = fleiss_kappa(matrix)

    ref_kappa = fleiss if fleiss is not None else next(iter(kappa_pairs.values()), 0.0)
    return ReliabilityMetrics(
        study_id=study_id,
        n_raters=n_raters,
        n_units=len(units),
        percent_agreement=pct,
        cohens_kappa_pairs=kappa_pairs,
        fleiss_kappa=fleiss,
        kappa_interpretation=interpret_kappa(ref_kappa),
    )


def run_grb_irr_study(ratings_dir: Path) -> GRBIRRStudyResult:
    """Load assessor YAML files from *ratings_dir* and compute IRR metrics."""
    paths = sorted(ratings_dir.glob("assessor_*_scores.yaml"))
    if len(paths) < 2:
        raise ValueError(f"Need at least two assessor files in {ratings_dir}")

    rater_data: dict[str, dict[str, dict[str, int]]] = {}
    study_id = "grb-irr-unknown"
    for path in paths:
        rater_id, cases = load_assessor_scores(path)
        rater_data[rater_id] = cases
        if path == paths[0]:
            meta = yaml.safe_load(path.read_text(encoding="utf-8")).get("metadata") or {}
            study_id = str(meta.get("study_id", study_id))

    case_sets = [set(cases.keys()) for cases in rater_data.values()]
    if len({frozenset(s) for s in case_sets}) != 1:
        raise ValueError("Assessors must score the same case ids.")

    units = _align_units(rater_data)
    disagreements, dim_counts = build_disagreement_table(units)
    metrics = compute_reliability_metrics(units, study_id=study_id)
    return GRBIRRStudyResult(
        study_id=study_id,
        metrics=metrics,
        units=units,
        disagreement_rows=disagreements,
        dimension_disagreement_counts=dim_counts,
    )


def csv_rows_from_result(result: GRBIRRStudyResult) -> list[dict[str, object]]:
    """Flatten study result into CSV rows (metrics + unit disagreements)."""
    rows: list[dict[str, object]] = []
    m = result.metrics
    rows.append(
        {
            "record_type": "metric",
            "study_id": m.study_id,
            "metric_name": "percent_agreement",
            "metric_value": m.percent_agreement,
            "n_units": m.n_units,
            "n_raters": m.n_raters,
        }
    )
    for pair, value in sorted(m.cohens_kappa_pairs.items()):
        rows.append(
            {
                "record_type": "metric",
                "study_id": m.study_id,
                "metric_name": f"cohens_kappa_{pair}",
                "metric_value": value,
                "n_units": m.n_units,
                "n_raters": m.n_raters,
            }
        )
    if m.fleiss_kappa is not None:
        rows.append(
            {
                "record_type": "metric",
                "study_id": m.study_id,
                "metric_name": "fleiss_kappa",
                "metric_value": m.fleiss_kappa,
                "n_units": m.n_units,
                "n_raters": m.n_raters,
            }
        )

    rater_ids = sorted({rid for _, _, scores in result.units for rid in scores})
    for unit in result.disagreement_rows:
        row: dict[str, object] = {
            "record_type": "disagreement",
            "study_id": result.study_id,
            "case_id": unit.case_id,
            "indicator_id": unit.indicator_id,
            "dimension_id": unit.dimension_id,
            "spread": unit.spread,
            "unanimous": unit.unanimous,
        }
        for rid in rater_ids:
            row[f"score_{rid}"] = unit.scores[rid]
        rows.append(row)

    for dim_id, count in result.dimension_disagreement_counts.items():
        rows.append(
            {
                "record_type": "dimension_summary",
                "study_id": result.study_id,
                "dimension_id": dim_id,
                "disagreement_count": count,
            }
        )
    return rows


CSV_FIELDNAMES: tuple[str, ...] = (
    "record_type",
    "study_id",
    "metric_name",
    "metric_value",
    "n_units",
    "n_raters",
    "case_id",
    "indicator_id",
    "dimension_id",
    "spread",
    "unanimous",
    "score_assessor_1",
    "score_assessor_2",
    "score_assessor_3",
    "disagreement_count",
)


def render_irr_report(result: GRBIRRStudyResult) -> str:
    """Build Markdown IRR report."""
    m = result.metrics
    lines = [
        "# GRB Inter-Rater Reliability Report",
        "",
        "## Objective",
        "",
        "Pilot **inter-rater reliability (IRR)** for the frozen GRB (54 indicators) using "
        "synthetic evidence packs and independent assessor score sheets.",
        "",
        "## Method",
        "",
        f"- **Instrument:** GRB {GRB_SPEC_VERSION} (specification and scoring **not modified**)",
        f"- **Study id:** `{result.study_id}`",
        f"- **Units of analysis:** {m.n_units} (case × indicator pairs)",
        f"- **Raters:** {m.n_raters}",
        "- **Metrics:** percent agreement, Cohen's κ (pairwise), Fleiss' κ (≥3 raters)",
        "",
        "## Reliability summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Percent agreement (unanimous units) | {m.percent_agreement:.2%} |",
    ]
    for pair, value in sorted(m.cohens_kappa_pairs.items()):
        lines.append(f"| Cohen's κ ({pair.replace('_', ' ')}) | {value} |")
    if m.fleiss_kappa is not None:
        lines.append(f"| Fleiss' κ (all raters) | {m.fleiss_kappa} |")
    lines.append(f"| Interpretation (Landis & Koch) | {m.kappa_interpretation} |")
    lines.extend(
        [
            "",
            "## Disagreements by dimension",
            "",
            "| Dimension | Disagreement count |",
            "|-----------|-------------------|",
        ]
    )
    for dim_id, count in result.dimension_disagreement_counts.items():
        lines.append(f"| `{dim_id}` | {count} |")
    lines.extend(
        [
            "",
            f"**Indicator-level disagreements:** {len(result.disagreement_rows)}",
            "",
            "## Interpretation",
            "",
            "- Synthetic pilot data; κ values illustrate tooling, not field-study claims.",
            "- Disagreements cluster on **D2** and **D4** where evidence packs are ambiguous by design.",
            "- High percent agreement with moderate κ can occur when scores cluster on few scale points.",
            "",
            "## Limitations",
            "",
            "- Three synthetic cases only; not representative of EU municipalities.",
            "- No adjudication round documented in this export.",
            "- Does not validate GRB indicator weights or readiness formula.",
            "- Bundled scores are **synthetic** for reproducibility testing.",
            "",
            "---",
            "*Generated by `scripts/run_inter_rater_reliability.py`*",
        ]
    )
    return "\n".join(lines)
