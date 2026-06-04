"""Unit tests for Ollama evidence extraction (mocked — no network or Ollama required)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from localgovbench.llm.evidence_extraction import (
    OllamaClient,
    build_extraction_prompt,
    extract_evidence,
    get_grb_indicator,
    parse_extraction_response,
)
from tests.conftest import MockOllamaClient

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


def test_extract_evidence_with_mock_client(mock_ollama_client: MockOllamaClient) -> None:
    result = extract_evidence(
        SAMPLE_DOC,
        "d2_oversight_design_01",
        client=mock_ollama_client,
    )
    assert result.model == "mock-model"
    assert mock_ollama_client.last_prompt is not None
    assert "candidate_evidence" in mock_ollama_client.last_prompt
    assert "d2_oversight_design_01" in mock_ollama_client.last_prompt


def test_extract_evidence_requires_client_or_mock() -> None:
    """Default OllamaClient must not be invoked in unit tests."""
    client = MockOllamaClient(VALID_RESPONSE)
    result = extract_evidence(SAMPLE_DOC, "d2_oversight_design_01", client=client)
    assert result.candidate_evidence


def test_ollama_client_generate_uses_mocked_http() -> None:
    """HTTP layer is patched — no live Ollama server or model download."""
    api_body = json.dumps({"response": VALID_RESPONSE}).encode("utf-8")
    mock_response = MagicMock()
    mock_response.read.return_value = api_body
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)

    client = OllamaClient(base_url="http://127.0.0.1:11434", model="test-model", timeout_seconds=1.0)
    with patch("localgovbench.llm.evidence_extraction.urllib.request.urlopen", return_value=mock_response):
        text = client.generate("test prompt", json_format=True)

    assert json.loads(text)["confidence_level"] == "high"
    mock_response.read.assert_called_once()


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
