"""Tests for synthetic demo score filler."""

from __future__ import annotations

from pathlib import Path

import pytest

from localgovbench.grb.specification import all_indicator_ids
from localgovbench.utils.io import load_yaml
from localgovbench.workflows.demo_scores import (
    SYNTHETIC_DEMO_BANNER,
    deterministic_demo_score,
    fill_demo_scores_file,
    fill_synthetic_demo_scores,
)
from localgovbench.workflows.scoring_template import build_scoring_template


def test_deterministic_demo_score_stable() -> None:
    a = deterministic_demo_score("d2_oversight_design_01")
    b = deterministic_demo_score("d2_oversight_design_01")
    assert a == b
    assert 0 <= a <= 4


def test_fill_all_indicators_around_level_three() -> None:
    template = build_scoring_template("demo")
    completed = fill_synthetic_demo_scores(template)
    assert completed["metadata"]["synthetic_demo_scores"] is True
    assert SYNTHETIC_DEMO_BANNER in completed["notes"]
    assert all(v is not None for v in completed["responses"].values())
    assert len(completed["responses"]) == len(all_indicator_ids())
    assert all(2 <= int(v) <= 4 for v in completed["responses"].values())


def test_evidence_refs_for_scores_at_least_three() -> None:
    template = build_scoring_template("demo")
    completed = fill_synthetic_demo_scores(template)
    refs = completed.get("evidence_refs") or {}
    for ind_id, score in completed["responses"].items():
        if int(score) >= 3:
            assert ind_id in refs
            assert len(refs[ind_id]) >= 1
        if int(score) >= 4:
            assert len(refs[ind_id]) >= 2


def test_fill_demo_scores_file_roundtrip(tmp_path: Path) -> None:
    inp = tmp_path / "assessor_scoring_template.yaml"
    out = tmp_path / "assessor_scoring_completed.yaml"
    template = build_scoring_template("x")
    from localgovbench.utils.io import save_yaml

    save_yaml(inp, template)
    fill_demo_scores_file(inp, out)
    loaded = load_yaml(out)
    assert loaded["metadata"]["synthetic_demo_scores"] is True
    assert all(v is not None for v in loaded["responses"].values())
