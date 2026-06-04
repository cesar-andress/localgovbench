"""Pytest configuration for LocalGovBench tests."""

from __future__ import annotations

import json

import pytest

from localgovbench.llm.evidence_extraction import OllamaClient


class MockOllamaClient(OllamaClient):
    """Ollama client that returns a fixed response without network I/O."""

    def __init__(self, response_text: str, *, model: str = "mock-model") -> None:
        super().__init__(base_url="http://mock.test", model=model)
        self._response_text = response_text
        self.last_prompt: str | None = None

    def generate(self, prompt: str, *, json_format: bool = True) -> str:
        self.last_prompt = prompt
        return self._response_text


@pytest.fixture
def mock_ollama_valid_response() -> str:
    return json.dumps(
        {
            "candidate_evidence": "Policy requires named policy officer review of LLM drafts.",
            "confidence_level": "high",
            "quoted_text_span": "must be reviewed by a named policy officer",
            "insufficient_evidence_warning": None,
        }
    )


@pytest.fixture
def mock_ollama_client(mock_ollama_valid_response: str) -> MockOllamaClient:
    return MockOllamaClient(mock_ollama_valid_response)
