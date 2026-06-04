"""Metric definitions for LocalGovBench LLM evidence extraction benchmark."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from localgovbench.llm.evidence_extraction import EvidenceExtractionResult

NO_EVIDENCE_PREFIXES = (
    "no explicit evidence",
    "no evidence identified",
    "no relevant evidence",
)


def normalize_text(text: str) -> str:
    """Collapse whitespace for substring checks."""
    return re.sub(r"\s+", " ", text.strip().lower())


def claims_evidence(result: EvidenceExtractionResult) -> bool:
    """True when the model asserts documentary support (non-empty quote)."""
    quote = result.quoted_text_span.strip()
    if not quote:
        return False
    candidate = result.candidate_evidence.strip().lower()
    if any(candidate.startswith(prefix) for prefix in NO_EVIDENCE_PREFIXES):
        return False
    return True


def quote_is_verbatim(quote: str, document_text: str) -> bool:
    """Quote must appear verbatim in the source document (whitespace-normalized)."""
    if not quote.strip():
        return False
    doc = normalize_text(document_text)
    fragment = normalize_text(quote)
    if len(fragment) < 8:
        return fragment in doc
    return fragment in doc


def quote_matches_gold_keywords(quote: str, gold_keywords: list[str]) -> bool:
    if not gold_keywords:
        return True
    normalized = normalize_text(quote)
    return any(normalize_text(keyword) in normalized for keyword in gold_keywords)


def detects_insufficient(result: EvidenceExtractionResult) -> bool:
    if result.insufficient_evidence_warning:
        return True
    if result.confidence_level == "low" and not result.quoted_text_span.strip():
        return True
    return False


@dataclass(frozen=True, slots=True)
class TaskGold:
    task_id: str
    document_path: str
    indicator_id: str
    gold_has_evidence: bool
    gold_keywords: list[str]
    gold_expect_insufficient: bool


@dataclass(frozen=True, slots=True)
class TaskEvaluation:
    task_id: str
    indicator_id: str
    claims_evidence: bool
    quote_valid: bool
    hallucinated: bool
    precision_hit: bool
    insufficient_detected: bool
    gold_expect_insufficient: bool
    latency_seconds: float
    error: str | None = None


def evaluate_task(
    result: EvidenceExtractionResult,
    *,
    gold: TaskGold,
    document_text: str,
) -> TaskEvaluation:
    claims = claims_evidence(result)
    valid = quote_is_verbatim(result.quoted_text_span, document_text) if claims else False
    hallucinated = claims and not valid

    if claims:
        precision_hit = (
            valid
            and gold.gold_has_evidence
            and quote_matches_gold_keywords(result.quoted_text_span, gold.gold_keywords)
        )
    else:
        precision_hit = not gold.gold_has_evidence

    insufficient_detected = detects_insufficient(result)

    return TaskEvaluation(
        task_id=gold.task_id,
        indicator_id=gold.indicator_id,
        claims_evidence=claims,
        quote_valid=valid,
        hallucinated=hallucinated,
        precision_hit=precision_hit,
        insufficient_detected=insufficient_detected,
        gold_expect_insufficient=gold.gold_expect_insufficient,
        latency_seconds=0.0,
    )


def aggregate_metrics(evaluations: list[TaskEvaluation]) -> dict[str, Any]:
    """Aggregate task-level evaluations into benchmark metrics."""
    n = len(evaluations)
    if n == 0:
        return {
            "n_tasks": 0,
            "n_success": 0,
            "evidence_precision": 0.0,
            "quote_validity_rate": 0.0,
            "hallucinated_evidence_rate": 0.0,
            "insufficient_evidence_detection_rate": 0.0,
            "mean_latency_seconds": 0.0,
            "p95_latency_seconds": 0.0,
        }

    claims = [e for e in evaluations if e.claims_evidence]
    quotes_claimed = len(claims)
    precision_hits = sum(1 for e in evaluations if e.precision_hit)
    evidence_precision = precision_hits / n

    valid_quotes = sum(1 for e in claims if e.quote_valid)
    quote_validity_rate = valid_quotes / quotes_claimed if quotes_claimed else 1.0

    hallucinated_evidence_rate = sum(1 for e in evaluations if e.hallucinated) / n

    insufficient_tasks = [e for e in evaluations if e.gold_expect_insufficient]
    if insufficient_tasks:
        insufficient_evidence_detection_rate = sum(
            1 for e in insufficient_tasks if e.insufficient_detected
        ) / len(insufficient_tasks)
    else:
        insufficient_evidence_detection_rate = 1.0

    latencies = sorted(e.latency_seconds for e in evaluations if e.error is None)
    n_success = len(latencies)
    if latencies:
        mean_latency = sum(latencies) / len(latencies)
        p95_index = max(0, int(0.95 * len(latencies)) - 1)
        p95_latency = latencies[p95_index]
    else:
        mean_latency = 0.0
        p95_latency = 0.0

    return {
        "n_tasks": n,
        "n_success": n_success,
        "evidence_precision": round(evidence_precision, 4),
        "quote_validity_rate": round(quote_validity_rate, 4),
        "hallucinated_evidence_rate": round(hallucinated_evidence_rate, 4),
        "insufficient_evidence_detection_rate": round(insufficient_evidence_detection_rate, 4),
        "mean_latency_seconds": round(mean_latency, 3),
        "p95_latency_seconds": round(p95_latency, 3),
    }
