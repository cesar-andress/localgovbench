#!/usr/bin/env python3
"""Run experimental Ollama evidence extraction for one GRB indicator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.evidence_extraction import (
    DEFAULT_OLLAMA_BASE_URL,
    DEFAULT_OLLAMA_MODEL,
    OllamaClient,
    extract_evidence,
    get_grb_indicator,
)

DEFAULT_DOCUMENT = ROOT / "data" / "synthetic" / "governance_policy_sample.md"
DEFAULT_INDICATOR = "d2_oversight_design_01"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract candidate GRB evidence from a document using local Ollama."
    )
    parser.add_argument(
        "--document",
        type=Path,
        default=DEFAULT_DOCUMENT,
        help="Path to governance document (markdown or plain text)",
    )
    parser.add_argument(
        "--indicator",
        default=DEFAULT_INDICATOR,
        help="GRB indicator id (default: d2_oversight_design_01)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_OLLAMA_MODEL,
        help=f"Ollama model name (default: {DEFAULT_OLLAMA_MODEL})",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_OLLAMA_BASE_URL,
        help=f"Ollama API base URL (default: {DEFAULT_OLLAMA_BASE_URL})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result as JSON",
    )
    args = parser.parse_args()

    if not args.document.exists():
        print(f"Document not found: {args.document}", file=sys.stderr)
        return 1

    document_text = args.document.read_text(encoding="utf-8")
    indicator = get_grb_indicator(args.indicator)
    client = OllamaClient(base_url=args.base_url, model=args.model)

    print("LocalGovBench — Ollama evidence extraction (prototype)")
    print("=" * 55)
    print("Local setup:")
    print("  ollama serve")
    print(f"  ollama pull {args.model}")
    print()
    print(f"Document: {args.document.name}")
    print(f"Indicator: {indicator.id} — {indicator.name}")
    print(f"Model: {args.model} @ {args.base_url}")
    print()
    print("NOTE: The LLM does not assign GRB scores. Humans must verify evidence.")
    print()

    try:
        result = extract_evidence(
            document_text,
            args.indicator,
            client=client,
        )
    except (ConnectionError, RuntimeError, ValueError) as exc:
        print(f"Extraction failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "indicator_id": result.indicator_id,
                    "candidate_evidence": result.candidate_evidence,
                    "confidence_level": result.confidence_level,
                    "quoted_text_span": result.quoted_text_span,
                    "insufficient_evidence_warning": result.insufficient_evidence_warning,
                    "model": result.model,
                    "note": result.note,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    print(f"Candidate evidence: {result.candidate_evidence}")
    print(f"Confidence: {result.confidence_level}")
    print(f"Quoted span: {result.quoted_text_span!r}")
    if result.insufficient_evidence_warning:
        print(f"Warning: {result.insufficient_evidence_warning}")
    print(f"\n{result.note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
