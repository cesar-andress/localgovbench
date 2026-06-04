"""Tests for Ollama evidence extraction (mocked HTTP)."""

from __future__ import annotations

import json

import pytest

from localgovbench.llm.evidence_extraction import (
    OllamaClient,
    build_extraction_prompt,
    extract_evidence,
    get_grb_indicator,
    parse_extraction_response,
)


class MockOllamaClient(OllamaClient):
    """Ollama client that returns a fixed response without network I/O."""

    def __init__(self, response_text: str) -> None:
        super().__init__(base_url="http://mock", model="mock-model")
        self._response_text = response_text
        self.last_prompt: str | None = None

    def generate(self, prompt: str, *, json_format: bool = True) -> str:
        self.last_prompt = prompt
        return self._response_text


VALID_RESPONSE = json.dumps(
    {
        "candidate_evidence": "Policy requires named policy officer review of LLM drafts.",
        "confidence_level": "high",
        "quoted_text_span": "must be reviewed by a named policy officer",
        "insufficient_evidence_warning": None,
    }
)

SCORING_RESPONSE = json.dumps(
    {
        "candidate_evidence": "Some evidence",
        "confidence_level": "medium",
        "quoted_text_span": "quote",
        "maturity_score": 3,
        "insufficient_evidence_warning": None,
    }
)


SAMPLE_DOC = (
    "Section 4.2 requires review by a named policy officer. "
    "Automated outputs are advisory."
)


def test_get_grb_indicator() -> None:
    ind = get_grb_indicator("d2_oversight_design_01")
    assert ind.dimension_id == "d2"
    assert "oversight" in ind.id


def test_build_prompt_forbids_scoring_instructions() -> None:
    indicator = get_grb_indicator("d2_oversight_design_01")
    prompt = build_extraction_prompt(SAMPLE_DOC, indicator, template="TEMPLATE")
    assert "TEMPLATE" in prompt
    assert "d2_oversight_design_01" in prompt
    assert SAMPLE_DOC in prompt
    assert "candidate_evidence" in prompt


def test_parse_valid_mock_response() -> None:
    result = parse_extraction_response(
        VALID_RESPONSE,
        indicator_id="d2_oversight_design_01",
        model="mock-model",
    )
    assert result.confidence_level == "high"
    assert "policy officer" in result.candidate_evidence
    assert result.insufficient_evidence_warning is None


def test_parse_rejects_scoring_fields() -> None:
    with pytest.raises(ValueError, match="scoring"):
        parse_extraction_response(
            SCORING_RESPONSE,
            indicator_id="d2_oversight_design_01",
            model="mock-model",
        )


def test_extract_evidence_with_mock_client() -> None:
    client = MockOllamaClient(VALID_RESPONSE)
    result = extract_evidence(
        SAMPLE_DOC,
        "d2_oversight_design_01",
        client=client,
    )
    assert result.model == "mock-model"
    assert client.last_prompt is not None
    assert "candidate_evidence" in client.last_prompt
    assert "d2_oversight_design_01" in client.last_prompt


def test_low_confidence_without_quote_sets_warning() -> None:
    raw = json.dumps(
        {
            "candidate_evidence": "",
            "confidence_level": "low",
            "quoted_text_span": "",
            "insufficient_evidence_warning": None,
        }
    )
    result = parse_extraction_response(raw, indicator_id="d1_mandate_01", model="m")
    assert result.insufficient_evidence_warning is not None


def test_prompt_template_loaded_from_repo() -> None:
    from localgovbench.llm.evidence_extraction import load_prompt_template

    text = load_prompt_template()
    assert "must **not** assign maturity scores" in text
