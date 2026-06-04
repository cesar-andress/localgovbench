#!/usr/bin/env python3
"""Validate repository structure and key metadata for publication readiness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "pyproject.toml",
    ".gitignore",
    "docs/framework.md",
    "docs/benchmark_specification.md",
    "docs/methodology.md",
    "docs/governance_dimensions.md",
    "docs/ai_act_mapping.md",
    "docs/gdpr_mapping.md",
    "docs/zenodo_release.md",
    "docs/manuscript_positioning.md",
    "docs/validation_protocol.md",
    "localgovbench/__init__.py",
    "localgovbench/framework/dimensions.py",
    "localgovbench/framework/scoring.py",
    "localgovbench/framework/checklist.py",
    "localgovbench/evaluation/rubric.py",
    "localgovbench/evaluation/validators.py",
    "localgovbench/utils/io.py",
    "localgovbench/llm/evidence_extraction.py",
    "prompts/evidence_extraction.md",
    "data/synthetic/governance_policy_sample.md",
    "data/synthetic/README.md",
    "scripts/run_ollama_evidence_extraction.py",
    "data/README.md",
    "data/raw/.gitkeep",
    "data/processed/.gitkeep",
    "data/templates/README.md",
    "prompts/README.md",
    "examples/example_assessment.yaml",
    "examples/README.md",
    "examples/grb/low_readiness_municipality.yaml",
    "examples/grb/medium_readiness_municipality.yaml",
    "examples/grb/high_readiness_municipality.yaml",
    "examples/grb/README.md",
    "reports/README.md",
    "results/README.md",
    "tests/test_dimensions.py",
    "tests/test_scoring.py",
    "tests/test_checklist.py",
    "tests/test_evidence_extraction.py",
    "validation/README.md",
    "validation/content_validity/README.md",
    "validation/content_validity/expert_review_questionnaire.yaml",
    "validation/content_validity/indicator_relevance_survey.yaml",
    "validation/content_validity/scoring_rubric.md",
    "validation/content_validity/indicator_relevance_survey_results.example.yaml",
    "validation/inter_rater/assessor_guide.md",
    "validation/inter_rater/scoring_template.yaml",
    "validation/benchmark_cases/municipality_low_readiness.yaml",
    "validation/benchmark_cases/municipality_medium_readiness.yaml",
    "validation/benchmark_cases/municipality_high_readiness.yaml",
    "validation/benchmark_cases/municipality_sovereign_ready.yaml",
    "validation/benchmark_cases/municipality_compliance_gap.yaml",
    "validation/benchmark_cases/README.md",
    "localgovbench/validation/content_validity.py",
    "localgovbench/validation/discriminant.py",
    "scripts/run_content_validity_analysis.py",
    "scripts/run_discriminant_validity.py",
    "tests/test_content_validity_metrics.py",
    "tests/test_discriminant_validity.py",
    "validation/docs/validation_protocol.md",
    "validation/docs/content_validity_guide.md",
    "validation/docs/inter_rater_guide.md",
    "validation/templates/content_validity_study.yaml",
    "validation/templates/expert_review_questionnaire.yaml",
    "validation/templates/inter_rater_codebook.yaml",
    "validation/templates/inter_rater_rating_sheet.yaml",
    "validation/templates/adjudication_record.yaml",
    "validation/cases/case_01_nordvega_internal_llm.yaml",
    "validation/cases/case_02_bayridge_service_bot.yaml",
    "validation/cases/case_03_highland_onprem_scale.yaml",
    "validation/ratings/case_01_nordvega_internal_llm_rater_a.yaml",
    "validation/reports/README.md",
    "localgovbench/validation/reliability.py",
    "localgovbench/validation/irr.py",
    "scripts/run_inter_rater_analysis.py",
    "scripts/generate_validation_report.py",
    "tests/test_reliability.py",
    "tests/test_validation_irr.py",
    "scripts/run_example_assessment.py",
]


def main() -> int:
    missing = [p for p in REQUIRED_PATHS if not (ROOT / p).exists()]
    if missing:
        print("Missing required paths:")
        for path in missing:
            print(f"  - {path}")
        return 1

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if "LocalGovBench" not in citation:
        print("CITATION.cff does not mention LocalGovBench.")
        return 1
    if "cff-version:" not in citation:
        print("CITATION.cff missing cff-version field.")
        return 1
    if "type: software" not in citation:
        print("CITATION.cff should declare type: software.")
        return 1

    example = (ROOT / "examples" / "example_assessment.yaml").read_text(encoding="utf-8")
    if "synthetic: true" not in example:
        print("example_assessment.yaml must declare synthetic: true")
        return 1

    print("Repository structure validation passed.")
    print(f"Checked {len(REQUIRED_PATHS)} required paths under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
