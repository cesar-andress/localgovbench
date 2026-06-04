"""Tests for validation IRR package."""

from __future__ import annotations

from pathlib import Path

import pytest

from localgovbench.validation.instruments import INSTRUMENT_V01, all_criterion_ids
from localgovbench.validation.irr import run_inter_rater_study
from localgovbench.validation.reports import render_validation_report

ROOT = Path(__file__).resolve().parents[1]
RATINGS_DIR = ROOT / "validation" / "ratings"


def test_instrument_has_25_criteria() -> None:
    assert len(all_criterion_ids()) == 25


def test_synthetic_irr_study_runs() -> None:
    result = run_inter_rater_study(RATINGS_DIR)
    assert result.instrument_id == INSTRUMENT_V01
    assert len(result.cases) == 3
    assert -1.0 <= result.overall_kappa <= 1.0
    assert 0.0 <= result.overall_alpha <= 1.0


def test_validation_report_renders() -> None:
    text = render_validation_report(validation_root=ROOT / "validation")
    assert "Cohen's Kappa" in text
    assert "Krippendorff's Alpha" in text
    assert "synthetic" in text.lower()


def test_ratings_missing_criterion_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "metadata:\n  case_id: c1\n  rater_id: a\n  instrument: localgovbench-v0.1\n"
        "responses:\n  legal_regulatory_gdpr_readiness: 2\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="missing"):
        run_inter_rater_study(tmp_path)
