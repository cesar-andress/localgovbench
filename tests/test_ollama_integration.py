"""Optional integration tests against a local Ollama server.

Run only when explicitly requested:

    pytest -m integration
    OLLAMA_INTEGRATION=1 pytest -m integration

Default ``pytest`` and ``pytest -m "not integration"`` skip these tests.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

import pytest

from localgovbench.llm.evidence_extraction import (
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_MODEL,
    OllamaClient,
    extract_evidence,
)

pytestmark = pytest.mark.integration

SAMPLE_DOC = "Section 4.2 requires review by a named policy officer."


def _ollama_available(base_url: str = DEFAULT_OLLAMA_BASE_URL) -> bool:
    if os.environ.get("OLLAMA_INTEGRATION", "").lower() not in ("1", "true", "yes"):
        return False
    try:
        urllib.request.urlopen(f"{base_url.rstrip('/')}/api/tags", timeout=3)
        return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


@pytest.mark.skipif(
    not _ollama_available(),
    reason="Set OLLAMA_INTEGRATION=1 and start Ollama (ollama serve) to run integration tests",
)
def test_ollama_live_generate_json() -> None:
    client = OllamaClient(timeout_seconds=60.0)
    raw = client.generate(
        'Respond with JSON only: {"status": "ok"}',
        json_format=True,
    )
    payload = json.loads(raw.strip())
    assert payload.get("status") == "ok"


@pytest.mark.skipif(
    not _ollama_available(),
    reason="Set OLLAMA_INTEGRATION=1 and start Ollama (ollama serve) to run integration tests",
)
def test_ollama_live_extract_evidence() -> None:
    result = extract_evidence(
        SAMPLE_DOC,
        "d2_oversight_design_01",
        client=OllamaClient(model=os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)),
    )
    assert result.indicator_id == "d2_oversight_design_01"
    assert result.confidence_level in ("low", "medium", "high")
