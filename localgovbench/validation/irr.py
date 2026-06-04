"""Inter-rater reliability (IRR) study loading and analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from localgovbench.validation.instruments import INSTRUMENT_V01, all_criterion_ids, get_instrument
from localgovbench.validation.reliability import (
    ReliabilityResult,
    cohens_kappa,
    interpret_alpha,
    interpret_kappa,
    krippendorff_alpha,
)
from localgovbench.utils.io import load_yaml


@dataclass(frozen=True, slots=True)
class CaseReliability:
    """Reliability metrics for one benchmark case."""

    case_id: str
    n_criteria: int
    cohens_kappa: float
    krippendorff_alpha: float
    kappa_label: str
    alpha_label: str
    disagreement_count: int


@dataclass
class InterRaterStudyResult:
    """Aggregated IRR study output."""

    study_id: str
    instrument_id: str
    cases: list[CaseReliability] = field(default_factory=list)
    overall_kappa: float = 0.0
    overall_alpha: float = 0.0
    overall_kappa_label: str = ""
    overall_alpha_label: str = ""


def load_rating_files(ratings_dir: Path) -> list[dict[str, Any]]:
    """Load all YAML rating files in a directory."""
    files = sorted(ratings_dir.glob("*.yaml"))
    payloads: list[dict[str, Any]] = []
    for path in files:
        data = load_yaml(path)
        data["_source_path"] = str(path)
        payloads.append(data)
    return payloads


def _validate_rating_payload(payload: dict[str, Any]) -> tuple[str, str, str, dict[str, int]]:
    metadata = payload.get("metadata") or {}
    case_id = str(metadata.get("case_id", ""))
    rater_id = str(metadata.get("rater_id", ""))
    instrument = str(metadata.get("instrument", INSTRUMENT_V01))
    if not case_id or not rater_id:
        raise ValueError(f"Rating file missing case_id or rater_id: {payload.get('_source_path')}")
    if instrument != INSTRUMENT_V01:
        raise ValueError(f"Unsupported instrument {instrument!r}")

    responses = payload.get("responses") or {}
    expected = set(all_criterion_ids())
    provided = set(responses.keys())
    missing = expected - provided
    if missing:
        raise ValueError(f"Case {case_id} rater {rater_id} missing {len(missing)} criteria.")
    scores = {cid: int(round(responses[cid])) for cid in expected}
    return case_id, rater_id, instrument, scores


def run_inter_rater_study(
    ratings_dir: Path,
    *,
    study_id: str = "irr-pilot-synthetic",
) -> InterRaterStudyResult:
    """
    Compute Cohen's Kappa and Krippendorff's Alpha per case and overall.

    Expects exactly two raters per case in *ratings_dir*.
    """
    grouped: dict[str, dict[str, dict[str, int]]] = {}
    for payload in load_rating_files(ratings_dir):
        case_id, rater_id, _, scores = _validate_rating_payload(payload)
        grouped.setdefault(case_id, {})[rater_id] = scores

    instrument = get_instrument()
    result = InterRaterStudyResult(study_id=study_id, instrument_id=instrument.id)

    criterion_ids = list(all_criterion_ids())

    for case_id in sorted(grouped):
        raters = grouped[case_id]
        if len(raters) != 2:
            raise ValueError(f"Case {case_id} must have exactly 2 raters, found {len(raters)}.")
        ids = sorted(raters.keys())
        scores_a = [raters[ids[0]][cid] for cid in criterion_ids]
        scores_b = [raters[ids[1]][cid] for cid in criterion_ids]
        kappa = cohens_kappa(scores_a, scores_b)
        alpha = krippendorff_alpha([scores_a, scores_b])
        disagreements = sum(1 for i in range(len(scores_a)) if scores_a[i] != scores_b[i])
        result.cases.append(
            CaseReliability(
                case_id=case_id,
                n_criteria=len(criterion_ids),
                cohens_kappa=round(kappa, 4),
                krippendorff_alpha=round(alpha, 4),
                kappa_label=interpret_kappa(kappa),
                alpha_label=interpret_alpha(alpha),
                disagreement_count=disagreements,
            )
        )
    # Pooled across all case×criterion units
    pooled_a: list[int] = []
    pooled_b: list[int] = []
    for case_id in sorted(grouped):
        ids = sorted(grouped[case_id].keys())
        for cid in criterion_ids:
            pooled_a.append(grouped[case_id][ids[0]][cid])
            pooled_b.append(grouped[case_id][ids[1]][cid])

    result.overall_kappa = round(cohens_kappa(pooled_a, pooled_b), 4)
    result.overall_alpha = round(krippendorff_alpha([pooled_a, pooled_b]), 4)
    result.overall_kappa_label = interpret_kappa(result.overall_kappa)
    result.overall_alpha_label = interpret_alpha(result.overall_alpha)
    return result
