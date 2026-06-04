"""Tests for GRB sensitivity analysis package."""

from __future__ import annotations

import csv
from pathlib import Path

from localgovbench.grb.profiles import build_responses
from localgovbench.grb.scoring import SAFEGUARD_CAP, compute_grb_assessment
from localgovbench.grb.sensitivity import (
    CSV_FIELDNAMES,
    MIN_PROFILE_COUNT,
    ProfileSpec,
    generate_profile_specs,
    run_sensitivity_study,
    score_profile_spec,
)


def test_profile_count_at_least_150() -> None:
    specs = generate_profile_specs()
    assert len(specs) >= 150
    assert len(specs) == MIN_PROFILE_COUNT


def test_deterministic_profile_generation() -> None:
    a = [s.profile_id for s in generate_profile_specs()]
    b = [s.profile_id for s in generate_profile_specs()]
    assert a == b
    groups_a = {s.profile_group for s in generate_profile_specs()}
    assert groups_a == {"baseline", "low_d2", "low_d4", "high_d6", "mixed"}


def test_baseline_higher_than_low_d2_at_zero() -> None:
    rows = run_sensitivity_study()
    baseline = [r for r in rows if r["profile_group"] == "baseline"]
    low_d2_0 = [r for r in rows if r["profile_group"] == "low_d2" and r["d2_input_level"] == 0]
    assert baseline
    assert low_d2_0
    mean_baseline = sum(float(r["readiness_final"]) for r in baseline) / len(baseline)
    mean_low = sum(float(r["readiness_final"]) for r in low_d2_0) / len(low_d2_0)
    assert mean_baseline > mean_low


def test_low_d4_at_zero_lower_than_baseline() -> None:
    rows = run_sensitivity_study()
    baseline_mean = sum(
        float(r["readiness_final"]) for r in rows if r["profile_group"] == "baseline"
    ) / sum(1 for r in rows if r["profile_group"] == "baseline")
    low_d4_0 = [
        r for r in rows if r["profile_group"] == "low_d4" and r["d4_input_level"] == 0
    ]
    mean_low = sum(float(r["readiness_final"]) for r in low_d4_0) / len(low_d4_0)
    assert mean_low < baseline_mean


def test_high_d6_at_four_higher_than_baseline() -> None:
    rows = run_sensitivity_study()
    baseline_mean = sum(
        float(r["readiness_final"]) for r in rows if r["profile_group"] == "baseline"
    ) / sum(1 for r in rows if r["profile_group"] == "baseline")
    high_d6_4 = [
        r for r in rows if r["profile_group"] == "high_d6" and r["d6_input_level"] == 4
    ]
    mean_high = sum(float(r["readiness_final"]) for r in high_d6_4) / len(high_d6_4)
    assert mean_high > baseline_mean


def test_safeguard_activation_when_d2_low_and_raw_high() -> None:
    result = compute_grb_assessment(
        {
            "metadata": {"municipality": "safeguard_d2"},
            "responses": build_responses(dimension_levels={"d2": 1}, default_level=4),
        }
    )
    assert result.readiness_raw > SAFEGUARD_CAP
    assert result.safeguard_applied is True
    assert result.readiness_final == SAFEGUARD_CAP


def test_safeguard_on_low_d4_input_zero_in_study() -> None:
    rows = run_sensitivity_study()
    low_d4_0 = [r for r in rows if r["profile_group"] == "low_d4" and r["d4_input_level"] == 0]
    assert low_d4_0
    assert any(r["safeguard_applied"] for r in low_d4_0)


def test_safeguard_not_on_baseline() -> None:
    rows = run_sensitivity_study()
    for r in rows:
        if r["profile_group"] == "baseline":
            assert r["safeguard_applied"] is False


def test_score_profile_spec_matches_study_row() -> None:
    spec = generate_profile_specs()[0]
    row = score_profile_spec(spec)
    study_row = next(r for r in run_sensitivity_study() if r["profile_id"] == spec.profile_id)
    assert row == study_row


def test_csv_output_schema(tmp_path: Path) -> None:
    rows = run_sensitivity_study()
    path = tmp_path / "out.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_FIELDNAMES))
        writer.writeheader()
        for row in rows[:5]:
            writer.writerow({k: row[k] for k in CSV_FIELDNAMES})
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == list(CSV_FIELDNAMES)
        assert len(list(reader)) == 5
