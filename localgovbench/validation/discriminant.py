"""Discriminant validity checks for synthetic benchmark cases."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from localgovbench.framework.scoring import compute_maturity_score
from localgovbench.utils.io import load_yaml

READINESS_BANDS: tuple[tuple[float, float, str], ...] = (
    (0.0, 24.0, "Not ready"),
    (25.0, 49.0, "Emerging"),
    (50.0, 74.0, "Substantially ready"),
    (75.0, 100.0, "Advanced readiness"),
)


@dataclass(frozen=True, slots=True)
class BenchmarkCaseResult:
    """Scored synthetic benchmark case."""

    case_id: str
    overall_maturity: float
    readiness_index: float
    readiness_band: str
    by_dimension: dict[str, float]
    expected_band: str
    band_match: bool


def readiness_index(overall_maturity: float) -> float:
    return round(100.0 * overall_maturity / 4.0, 2)


def classify_readiness_band(index: float) -> str:
    for low, high, label in READINESS_BANDS:
        if low <= index <= high:
            return label
    return READINESS_BANDS[-1][2]


def load_benchmark_case(path: Path) -> dict[str, Any]:
    return load_yaml(path)


def score_benchmark_case(payload: dict[str, Any]) -> BenchmarkCaseResult:
    metadata = payload.get("metadata") or {}
    case_id = str(metadata.get("case_id", "unknown"))
    responses = payload.get("responses") or {}
    result = compute_maturity_score(responses)
    index = readiness_index(result.overall)
    band = classify_readiness_band(index)
    expected = (payload.get("expected_outcome") or {}).get("readiness_band", "")
    return BenchmarkCaseResult(
        case_id=case_id,
        overall_maturity=result.overall,
        readiness_index=index,
        readiness_band=band,
        by_dimension=result.by_dimension,
        expected_band=str(expected),
        band_match=band == expected if expected else True,
    )


def run_discriminant_analysis(cases_dir: Path) -> list[BenchmarkCaseResult]:
    """Score all municipality_*.yaml benchmark cases in *cases_dir*."""
    results: list[BenchmarkCaseResult] = []
    for path in sorted(cases_dir.glob("municipality_*.yaml")):
        payload = load_benchmark_case(path)
        results.append(score_benchmark_case(payload))
    if not results:
        raise ValueError(f"No benchmark cases found in {cases_dir}")
    return results


def verify_discriminant_ordering(results: list[BenchmarkCaseResult]) -> list[str]:
    """
    Verify expected ordering: low < medium < high <= sovereign_ready.

    compliance_gap should score below high (documentation-heavy, weak oversight).
    """
    by_id = {r.case_id: r for r in results}
    errors: list[str] = []

    def _get(suffix: str) -> BenchmarkCaseResult:
        key = f"municipality_{suffix}"
        if key not in by_id:
            raise KeyError(key)
        return by_id[key]

    low = _get("low_readiness")
    medium = _get("medium_readiness")
    high = _get("high_readiness")
    sovereign = _get("sovereign_ready")
    gap = _get("compliance_gap")

    if not low.overall_maturity < medium.overall_maturity < high.overall_maturity:
        errors.append(
            f"Ordering failed: low={low.overall_maturity}, "
            f"medium={medium.overall_maturity}, high={high.overall_maturity}"
        )
    if sovereign.overall_maturity < high.overall_maturity:
        errors.append(
            f"Sovereign ready should be >= high: sovereign={sovereign.overall_maturity}, "
            f"high={high.overall_maturity}"
        )
    if gap.overall_maturity >= high.overall_maturity:
        errors.append(
            f"Compliance gap should be below high: gap={gap.overall_maturity}, "
            f"high={high.overall_maturity}"
        )
    if gap.by_dimension.get("operational", 4) >= high.by_dimension.get("operational", 0):
        errors.append("Compliance gap should have weaker operational dimension than high profile.")

    for result in results:
        if not result.band_match:
            errors.append(
                f"{result.case_id}: expected band {result.expected_band!r}, "
                f"got {result.readiness_band!r}"
            )

    return errors
