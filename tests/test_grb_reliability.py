"""Tests for GRB inter-rater reliability package."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
import yaml

from localgovbench.grb.reliability import (
    CSV_FIELDNAMES,
    build_disagreement_table,
    compute_reliability_metrics,
    fleiss_kappa,
    load_assessor_scores,
    percent_agreement,
    run_grb_irr_study,
    validate_indicator_id,
)
from localgovbench.grb.specification import all_indicator_ids
from localgovbench.grb.profiles import build_responses


def test_percent_agreement_perfect() -> None:
    matrix = [[2, 2, 2], [3, 3, 3], [4, 4, 4]]
    assert percent_agreement(matrix) == 1.0
    assert fleiss_kappa(matrix) == pytest.approx(1.0, abs=0.001)


def test_percent_agreement_partial() -> None:
    matrix = [[2, 2, 2], [3, 3, 4], [1, 2, 1]]
    assert 0.0 < percent_agreement(matrix) < 1.0
    assert fleiss_kappa(matrix) < 1.0


def test_compute_reliability_metrics_perfect() -> None:
    units = [
        ("c", "d1_mandate_01", {"a": 2, "b": 2}),
        ("c", "d1_mandate_02", {"a": 3, "b": 3}),
    ]
    metrics = compute_reliability_metrics(units, study_id="t")
    assert metrics.percent_agreement == 1.0
    assert metrics.cohens_kappa_pairs["a_vs_b"] == pytest.approx(1.0)


def test_invalid_indicator_id_raises() -> None:
    with pytest.raises(ValueError, match="Unknown GRB indicator"):
        validate_indicator_id("d99_fake_01")


def test_disagreement_table_generation() -> None:
    units = [
        ("case_alpha", "d1_mandate_01", {"assessor_1": 2, "assessor_2": 2, "assessor_3": 2}),
        ("case_alpha", "d2_oversight_design_01", {"assessor_1": 1, "assessor_2": 2, "assessor_3": 1}),
    ]
    rows, dim_counts = build_disagreement_table(units)
    assert len(rows) == 1
    assert rows[0].indicator_id == "d2_oversight_design_01"
    assert rows[0].dimension_id == "d2"
    assert dim_counts["d2"] == 1


def test_load_assessor_invalid_indicator(tmp_path: Path) -> None:
    responses = build_responses(dimension_levels={"d1": 2})
    responses["not_a_real_indicator"] = 1
    payload = {
        "metadata": {"rater_id": "x", "study_id": "t"},
        "cases": {"case_alpha": {"responses": responses}},
    }
    path = tmp_path / "assessor_1_scores.yaml"
    path.write_text(yaml.dump(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="Unknown GRB indicator"):
        load_assessor_scores(path)


def test_run_grb_irr_study_on_bundled_examples() -> None:
    root = Path(__file__).resolve().parents[1]
    ratings = root / "examples" / "grb" / "inter_rater"
    result = run_grb_irr_study(ratings)
    assert result.metrics.n_units == 54 * 3
    assert result.metrics.n_raters == 3
    assert 0.0 <= result.metrics.percent_agreement <= 1.0
    assert result.metrics.fleiss_kappa is not None
    assert len(result.disagreement_rows) > 0


def test_csv_schema_from_bundled_study() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_grb_irr_study(root / "examples" / "grb" / "inter_rater")
    from localgovbench.grb.reliability import csv_rows_from_result

    rows = csv_rows_from_result(result)
    metric_rows = [r for r in rows if r["record_type"] == "metric"]
    assert metric_rows
    assert any(r["metric_name"] == "percent_agreement" for r in metric_rows)
    assert any(r["metric_name"] == "fleiss_kappa" for r in metric_rows)
