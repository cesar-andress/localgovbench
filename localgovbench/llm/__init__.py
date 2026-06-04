"""Experimental LLM helpers (evidence extraction only — no automated scoring)."""

from localgovbench.llm.evidence_extraction import (
    EvidenceExtractionResult,
    OllamaClient,
    extract_evidence,
    get_grb_indicator,
    load_prompt_template,
)
from localgovbench.llm.model_benchmark import (
    BENCHMARK_MODELS,
    benchmark_output_paths,
    legacy_benchmark_output_paths,
    remove_legacy_benchmark_outputs,
    run_full_benchmark,
    write_benchmark_outputs,
)

__all__ = [
    "BENCHMARK_MODELS",
    "benchmark_output_paths",
    "legacy_benchmark_output_paths",
    "remove_legacy_benchmark_outputs",
    "EvidenceExtractionResult",
    "OllamaClient",
    "extract_evidence",
    "get_grb_indicator",
    "load_prompt_template",
    "run_full_benchmark",
    "write_benchmark_outputs",
]
