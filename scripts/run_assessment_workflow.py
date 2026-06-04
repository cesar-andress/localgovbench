#!/usr/bin/env python3
"""End-to-end GRB assessment: documents → evidence log → human scores → readiness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench.llm.evidence_extraction import DEFAULT_OLLAMA_BASE_URL, DEFAULT_OLLAMA_MODEL
from localgovbench.workflows.assessment_workflow import (
    WorkflowConfig,
    run_compute_phase,
    run_prepare_phase,
)

DEFAULT_DOCS = ROOT / "data" / "synthetic" / "workflow_demo" / "documents"
DEFAULT_OUTPUT = ROOT / "outputs" / "demo_municipality"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="GRB end-to-end assessment workflow (documents → evidence → human scores → readiness)."
    )
    parser.add_argument("--case-id", required=True, help="Assessment case identifier")
    parser.add_argument(
        "--documents",
        type=Path,
        default=DEFAULT_DOCS,
        help="Folder containing governance documents (.md, .txt)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directory for workflow outputs",
    )
    parser.add_argument(
        "--generate-template",
        action="store_true",
        help="Prepare evidence log and human scoring template (default if neither flag set)",
    )
    parser.add_argument(
        "--compute-score",
        action="store_true",
        help="Compute readiness from completed human scores YAML",
    )
    parser.add_argument(
        "--scores",
        type=Path,
        default=None,
        help="Path to completed assessor_scoring_template.yaml (for --compute-score)",
    )
    parser.add_argument(
        "--use-ollama",
        action="store_true",
        help="Extract candidate evidence via local Ollama (optional; never assigns scores)",
    )
    parser.add_argument("--model", default=DEFAULT_OLLAMA_MODEL, help="Ollama model name")
    parser.add_argument("--ollama-base-url", default=DEFAULT_OLLAMA_BASE_URL, help="Ollama API base URL")
    parser.add_argument("--municipality", default=None, help="Display label for reports")
    args = parser.parse_args()

    run_prepare = args.generate_template or not args.compute_score
    run_compute = args.compute_score

    if not run_prepare and not run_compute:
        run_prepare = True

    config = WorkflowConfig(
        case_id=args.case_id,
        documents_dir=args.documents.resolve(),
        output_dir=args.output_dir.resolve(),
        use_ollama=args.use_ollama,
        ollama_model=args.model,
        ollama_base_url=args.ollama_base_url,
        municipality_label=args.municipality,
    )

    exit_code = 0

    if run_prepare:
        result = run_prepare_phase(config)
        print("GRB assessment workflow — prepare phase")
        print("=" * 40)
        print(f"Case: {result.case_id}")
        print(f"Evidence log: {result.evidence_log_path}")
        print(f"Scoring template: {result.scoring_template_path}")
        for warning in result.warnings:
            print(f"WARNING: {warning}")
        print("Next: complete human scores in the template, then run with --compute-score")

    if run_compute:
        scores_path = args.scores or (config.output_dir / "assessor_scoring_template.yaml")
        if not scores_path.exists():
            print(f"Scores file not found: {scores_path}", file=sys.stderr)
            return 1
        result = run_compute_phase(config, scores_path.resolve())
        print("GRB assessment workflow — compute phase")
        print("=" * 40)
        print(f"Case: {result.case_id}")
        if result.assessment_result:
            ar = result.assessment_result
            print(f"Readiness (final): {ar.readiness_final} — {ar.readiness_band}")
        print(f"Report: {result.readiness_report_path}")
        print(f"JSON: {result.results_json_path}")
        for warning in result.warnings:
            print(f"WARNING: {warning}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
