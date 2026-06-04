"""Tests for discriminant validity on synthetic benchmark cases."""

from __future__ import annotations

from pathlib import Path

from localgovbench.validation.discriminant import (
    run_discriminant_analysis,
    verify_discriminant_ordering,
)

CASES_DIR = Path("validation/benchmark_cases")


def test_five_benchmark_cases_exist() -> None:
    cases = list(CASES_DIR.glob("municipality_*.yaml"))
    assert len(cases) == 5


def test_discriminant_ordering_passes() -> None:
    results = run_discriminant_analysis(CASES_DIR)
    errors = verify_discriminant_ordering(results)
    assert errors == []


def test_low_readiness_not_ready_band() -> None:
    results = run_discriminant_analysis(CASES_DIR)
    low = next(r for r in results if r.case_id == "municipality_low_readiness")
    assert low.readiness_band == "Not ready"
    assert low.readiness_index < 25.0


def test_sovereign_scores_at_least_high() -> None:
    results = run_discriminant_analysis(CASES_DIR)
    sovereign = next(r for r in results if r.case_id == "municipality_sovereign_ready")
    high = next(r for r in results if r.case_id == "municipality_high_readiness")
    assert sovereign.overall_maturity >= high.overall_maturity
