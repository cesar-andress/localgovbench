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
    "localgovbench/grb/specification.py",
    "localgovbench/grb/scoring.py",
    "localgovbench/grb/profiles.py",
    "localgovbench/grb/sensitivity.py",
    "scripts/run_grb_assessment.py",
    "scripts/run_grb_sensitivity_analysis.py",
    "scripts/run_sensitivity_analysis.py",
    "tests/test_grb_scoring.py",
    "tests/test_grb_sensitivity.py",
    "tests/test_grb_sensitivity_analysis.py",
    "results/grb_sensitivity_analysis.csv",
    "reports/grb_sensitivity_analysis.md",
    "docs/inter_rater_reliability_protocol.md",
    "examples/grb/inter_rater/case_alpha_evidence_pack.md",
    "examples/grb/inter_rater/case_beta_evidence_pack.md",
    "examples/grb/inter_rater/case_gamma_evidence_pack.md",
    "examples/grb/inter_rater/assessor_1_scores.yaml",
    "examples/grb/inter_rater/assessor_2_scores.yaml",
    "examples/grb/inter_rater/assessor_3_scores.yaml",
    "localgovbench/grb/reliability.py",
    "scripts/run_inter_rater_reliability.py",
    "tests/test_grb_reliability.py",
    "results/inter_rater_reliability.csv",
    "reports/inter_rater_reliability.md",
    "CHANGELOG.md",
    "docs/artifact_description.md",
    "docs/reproducibility.md",
    "docs/release_v0_1_checklist.md",
    "docs/construct_traceability.md",
    "docs/author_identity.md",
    "data/traceability/indicator_mapping.csv",
    "data/traceability/README.md",
    "localgovbench/traceability.py",
    "scripts/validate_traceability.py",
    "reports/traceability_report.md",
    "tests/test_traceability.py",
    "localgovbench/workflows/__init__.py",
    "localgovbench/workflows/assessment_workflow.py",
    "localgovbench/workflows/evidence_log.py",
    "localgovbench/workflows/scoring_template.py",
    "scripts/run_assessment_workflow.py",
    "scripts/fill_demo_scores.py",
    "localgovbench/workflows/demo_scores.py",
    "tests/test_demo_scores.py",
    "data/synthetic/workflow_demo/README.md",
    "data/synthetic/workflow_demo/documents/governance_policy.md",
    "data/synthetic/workflow_demo/documents/technical_architecture.md",
    "data/synthetic/workflow_demo/documents/incident_response.md",
    "data/synthetic/workflow_demo/documents/data_governance.md",
    "data/synthetic/workflow_demo/documents/procurement_note.md",
    "tests/test_assessment_workflow.py",
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
    if 'title: LocalGovBench' not in citation:
        print("CITATION.cff title should be LocalGovBench.")
        return 1
    if "10.5281/zenodo.TBD" not in citation:
        print("CITATION.cff should include placeholder DOI 10.5281/zenodo.TBD.")
        return 1
    if "family-names: Andrés" not in citation or "given-names: César" not in citation:
        print("CITATION.cff should list author César Andrés.")
        return 1
    if "0009-0001-8968-3404" not in citation:
        print("CITATION.cff should include ORCID 0009-0001-8968-3404.")
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
