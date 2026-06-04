"""Tests for end-to-end GRB assessment workflow."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from localgovbench.grb.profiles import build_responses
from localgovbench.grb.specification import all_indicator_ids
from localgovbench.utils.io import load_yaml, save_yaml
from localgovbench.workflows.assessment_workflow import (
    WorkflowConfig,
    run_compute_phase,
    run_prepare_phase,
)
from localgovbench.workflows.evidence_log import (
    EvidenceEntry,
    append_evidence_entry,
    load_evidence_log,
    new_evidence_log,
    validate_evidence_log,
)
from localgovbench.workflows.scoring_template import (
    assert_no_llm_scores,
    build_scoring_template,
    load_human_scores,
    save_scoring_template,
)

DEMO_DOCS = Path(__file__).resolve().parents[1] / "data" / "synthetic" / "workflow_demo" / "documents"


def test_workflow_runs_without_ollama(tmp_path: Path) -> None:
    config = WorkflowConfig(
        case_id="test_case",
        documents_dir=DEMO_DOCS,
        output_dir=tmp_path / "out",
        use_ollama=False,
    )
    result = run_prepare_phase(config)
    assert result.evidence_log_path and result.evidence_log_path.exists()
    assert result.scoring_template_path and result.scoring_template_path.exists()
    log = load_evidence_log(result.evidence_log_path)
    assert validate_evidence_log(log) == []
    template = load_yaml(result.scoring_template_path)
    assert_no_llm_scores(template)


def test_scoring_template_contains_all_indicators(tmp_path: Path) -> None:
    template = build_scoring_template("demo")
    assert len(template["responses"]) == len(all_indicator_ids())
    assert all(v is None for v in template["responses"].values())


def test_evidence_log_supports_multiple_entries() -> None:
    log = new_evidence_log("x", documents_reviewed=["a.md"])
    ind = list(all_indicator_ids())[0]
    append_evidence_entry(
        log,
        ind,
        EvidenceEntry("e1", "a.md", "first", extracted_by="human"),
    )
    append_evidence_entry(
        log,
        ind,
        EvidenceEntry("e2", "b.md", "second", extracted_by="human"),
    )
    assert len(log["indicators"][ind]["entries"]) == 2
    assert validate_evidence_log(log) == []


def test_readiness_report_generated(tmp_path: Path) -> None:
    config = WorkflowConfig(
        case_id="scored_case",
        documents_dir=DEMO_DOCS,
        output_dir=tmp_path / "scored",
        use_ollama=False,
    )
    run_prepare_phase(config)
    scores_path = config.output_dir / "assessor_scoring_template.yaml"
    template = load_yaml(scores_path)
    template["responses"] = build_responses(dimension_levels={"d1": 3, "d2": 3, "d3": 3, "d4": 3, "d5": 3, "d6": 3})
    save_scoring_template(scores_path, template, allow_prescore=True)

    result = run_compute_phase(config, scores_path)
    assert result.readiness_report_path
    assert result.readiness_report_path.exists()
    text = result.readiness_report_path.read_text(encoding="utf-8")
    assert "Candidate evidence" in text
    assert "Human-assigned scores" in text
    assert "Computed readiness" in text
    assert result.results_json_path
    payload = __import__("json").loads(result.results_json_path.read_text(encoding="utf-8"))
    assert payload["computed_readiness"] is not None


def test_ollama_unavailable_does_not_crash_workflow(tmp_path: Path) -> None:
    config = WorkflowConfig(
        case_id="ollama_fail",
        documents_dir=DEMO_DOCS,
        output_dir=tmp_path / "ollama",
        use_ollama=True,
    )
    with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
        result = run_prepare_phase(config)
    assert result.evidence_log_path
    assert any("Ollama unavailable" in w for w in result.warnings)
    template = load_yaml(result.scoring_template_path)
    assert_no_llm_scores(template)


def test_scores_never_auto_filled_by_llm(tmp_path: Path) -> None:
    config = WorkflowConfig(
        case_id="no_llm_scores",
        documents_dir=DEMO_DOCS,
        output_dir=tmp_path / "nollm",
        use_ollama=False,
    )
    result = run_prepare_phase(config)
    template = load_yaml(result.scoring_template_path)
    assert_no_llm_scores(template)
    filled = [k for k, v in template["responses"].items() if v is not None]
    assert filled == []


def test_compute_requires_complete_scores(tmp_path: Path) -> None:
    config = WorkflowConfig(
        case_id="incomplete",
        documents_dir=DEMO_DOCS,
        output_dir=tmp_path / "inc",
        use_ollama=False,
    )
    run_prepare_phase(config)
    scores_path = config.output_dir / "assessor_scoring_template.yaml"
    with pytest.raises(ValueError, match="template is for human entry only"):
        load_human_scores(scores_path)
