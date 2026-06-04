"""Experimental Ollama-based evidence extraction for GRB indicators.

The local LLM proposes candidate evidence only. It must **not** assign maturity
scores or readiness values — those remain with human assessors.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from localgovbench.grb.specification import GRB_DIMENSIONS, GRBIndicator

ConfidenceLevel = Literal["low", "medium", "high"]

FORBIDDEN_RESPONSE_KEYS = frozenset({
    "score",
    "maturity",
    "maturity_score",
    "readiness",
    "readiness_score",
    "rating",
    "overall",
    "dimension_score",
})

DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "evidence_extraction.md"

EXTRACTION_SCHEMA_HINT = {
    "candidate_evidence": "Brief summary of governance evidence found (or none).",
    "confidence_level": "One of: low, medium, high.",
    "quoted_text_span": "Exact quote from the document supporting the evidence, or empty string.",
    "insufficient_evidence_warning": "Warning message if evidence is weak or absent, else null.",
}


@dataclass(frozen=True, slots=True)
class IndicatorDefinition:
    """GRB indicator metadata passed to the extraction prompt."""

    id: str
    dimension_id: str
    subdimension_id: str
    name: str
    prompt: str


@dataclass(frozen=True, slots=True)
class EvidenceExtractionResult:
    """Structured evidence proposal from the LLM (not a scored assessment)."""

    indicator_id: str
    candidate_evidence: str
    confidence_level: ConfidenceLevel
    quoted_text_span: str
    insufficient_evidence_warning: str | None
    model: str
    note: str = (
        "Candidate evidence only — human assessors must verify and assign maturity scores."
    )


def get_grb_indicator(indicator_id: str) -> IndicatorDefinition:
    """Load a GRB indicator definition by id."""
    for dimension in GRB_DIMENSIONS:
        for subdimension in dimension.subdimensions:
            for indicator in subdimension.indicators:
                if indicator.id == indicator_id:
                    return _to_definition(indicator)
    raise KeyError(f"Unknown GRB indicator: {indicator_id!r}")


def _to_definition(indicator: GRBIndicator) -> IndicatorDefinition:
    return IndicatorDefinition(
        id=indicator.id,
        dimension_id=indicator.dimension_id,
        subdimension_id=indicator.subdimension_id,
        name=indicator.name,
        prompt=indicator.prompt,
    )


def load_prompt_template(path: Path | None = None) -> str:
    """Load the evidence extraction prompt template markdown."""
    prompt_path = path or PROMPT_PATH
    return prompt_path.read_text(encoding="utf-8")


def build_extraction_prompt(
    document_text: str,
    indicator: IndicatorDefinition,
    *,
    template: str | None = None,
) -> str:
    """Compose the user prompt sent to Ollama."""
    template = template or load_prompt_template()
    return (
        f"{template}\n\n"
        "---\n\n"
        "## Indicator\n\n"
        f"- **ID:** `{indicator.id}`\n"
        f"- **Dimension:** `{indicator.dimension_id}`\n"
        f"- **Subdimension:** `{indicator.subdimension_id}`\n"
        f"- **Name:** {indicator.name}\n"
        f"- **Assessment focus:** {indicator.prompt}\n\n"
        "---\n\n"
        "## Governance document (verbatim)\n\n"
        f"{document_text.strip()}\n\n"
        "---\n\n"
        "## Required JSON output\n\n"
        "Return **only** a JSON object with these keys:\n"
        f"{json.dumps(EXTRACTION_SCHEMA_HINT, indent=2)}\n"
    )


class OllamaClient:
    """Minimal HTTP client for Ollama's local API."""

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        model: str = DEFAULT_OLLAMA_MODEL,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, *, json_format: bool = True) -> str:
        """Call ``POST /api/generate`` and return the response text."""
        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if json_format:
            payload["format"] = "json"

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise ConnectionError(
                f"Could not reach Ollama at {self.base_url}. "
                "Start the server with: ollama serve"
            ) from exc

        if "error" in body:
            raise RuntimeError(f"Ollama error: {body['error']}")
        return str(body.get("response", ""))


def _reject_scoring_content(payload: dict[str, Any], raw_text: str) -> None:
    """Raise if the model attempted to emit maturity or readiness scores."""
    for key in payload:
        if key.lower() in FORBIDDEN_RESPONSE_KEYS:
            raise ValueError(
                f"Model output must not contain scoring field {key!r}. "
                "Evidence extraction only."
            )
    if re.search(r"\b(maturity|readiness)\s*[:=]\s*[0-4]", raw_text, re.I):
        raise ValueError("Model output appears to contain a maturity/readiness score.")


def _normalize_confidence(value: str) -> ConfidenceLevel:
    normalized = value.strip().lower()
    if normalized not in ("low", "medium", "high"):
        raise ValueError(f"Invalid confidence_level: {value!r}")
    return normalized  # type: ignore[return-value]


def parse_extraction_response(
    raw_response: str,
    *,
    indicator_id: str,
    model: str,
) -> EvidenceExtractionResult:
    """Parse and validate JSON returned by Ollama."""
    text = raw_response.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ollama response is not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("Ollama response must be a JSON object.")

    _reject_scoring_content(payload, raw_response)

    candidate = str(payload.get("candidate_evidence", "")).strip()
    quoted = str(payload.get("quoted_text_span", "")).strip()
    confidence = _normalize_confidence(str(payload.get("confidence_level", "low")))
    warning_raw = payload.get("insufficient_evidence_warning")
    warning = None if warning_raw in (None, "", "null") else str(warning_raw).strip()

    if not warning and (not candidate or not quoted or confidence == "low"):
        warning = (
            "Insufficient documentary evidence: add primary sources or "
            "clarify governance controls before scoring."
        )

    return EvidenceExtractionResult(
        indicator_id=indicator_id,
        candidate_evidence=candidate or "No explicit evidence identified.",
        confidence_level=confidence,
        quoted_text_span=quoted,
        insufficient_evidence_warning=warning,
        model=model,
    )


def extract_evidence(
    document_text: str,
    indicator_id: str,
    *,
    client: OllamaClient | None = None,
    prompt_template: str | None = None,
) -> EvidenceExtractionResult:
    """
    Extract candidate evidence for one GRB indicator using a local Ollama model.

    This function never assigns benchmark scores.
    """
    indicator = get_grb_indicator(indicator_id)
    ollama = client or OllamaClient()
    prompt = build_extraction_prompt(
        document_text,
        indicator,
        template=prompt_template,
    )
    raw = ollama.generate(prompt, json_format=True)
    return parse_extraction_response(
        raw,
        indicator_id=indicator_id,
        model=ollama.model,
    )
