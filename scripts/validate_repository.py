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
    "docs/citation.md",
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
    "scripts/run_llm_model_benchmark.py",
    "data/benchmark/evidence_extraction_tasks.json",
    "data/benchmark/README.md",
    "localgovbench/llm/benchmark_metrics.py",
    "localgovbench/llm/model_benchmark.py",
    "tests/test_llm_model_benchmark.py",
    "results/model_benchmark_mock.csv",
    "reports/model_benchmark_mock.md",
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
    "docs/demo_walkthrough.md",
    "docs/llm_benchmark_experiment.md",
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

# Active Disclosure Functions v1 stack (required for current release tip).
DF_REQUIRED_PATHS = [
    "localgovbench_measurement_validation/affordance/README.md",
    "localgovbench_measurement_validation/affordance/config/disclosure_functions_v1.yaml",
    "localgovbench_measurement_validation/affordance/config/field_function_candidates_v1.csv",
    "localgovbench_measurement_validation/affordance/config/applicability_overrides_v1.yaml",
    "localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.json",
    "localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.md",
    "localgovbench_measurement_validation/affordance/outputs/schema_inventory_v1.csv",
    "localgovbench_measurement_validation/affordance/coding/config/codebook_affordance_v1.md",
    "localgovbench_measurement_validation/affordance/coding/config/coder_instructions_v1.md",
    "localgovbench_measurement_validation/affordance/coding/config/coding_labels_v1.yaml",
    "localgovbench_measurement_validation/affordance/coding/config/schema_coding_record_v1.schema.json",
    "localgovbench_measurement_validation/affordance/coding/config/double_coding_protocol_v1.md",
    "localgovbench_measurement_validation/affordance/coding/templates/schema_coding_template_v1.csv",
    "localgovbench_measurement_validation/affordance/coding/templates/pilot_coding_manifest_v1.csv",
    "localgovbench_measurement_validation/affordance/coding/pilot_round_01/README.md",
    "localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv",
    "localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_B.csv",
    "localgovbench_measurement_validation/affordance/experiments/EXPERIMENT_PIPELINE.md",
    "scripts/run_affordance_experiment_pipeline.py",
    "scripts/build_affordance_specification.py",
    "scripts/build_affordance_coding_layer.py",
    "docs/supplements/README.md",
    "paper_assets/paper_asset_manifest.md",
    "docs/releases/public_positioning_v0.2.0.md",
    "docs/releases/NEXT_RELEASE.md",
    "docs/reproducibility/corpus_acquisition.md",
    "docs/reproducibility/clean_room_checklist.md",
    ".zenodo.json",
    ".github/workflows/ci.yml",
]

LEGACY_NOTICE_MARKERS = (
    "Status: LEGACY — v0.1.0",
    "LEGACY — v0.1.0",
    "not Disclosure Functions v1 empirical results",
    "not the active Disclosure Functions",
)


def _read_pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("version"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("version not found in pyproject.toml")


def main() -> int:
    missing = [p for p in REQUIRED_PATHS + DF_REQUIRED_PATHS if not (ROOT / p).exists()]
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
    if "title:" not in citation or "LocalGovBench" not in citation:
        print("CITATION.cff title should include LocalGovBench.")
        return 1
    if "10.5281/zenodo.21701861" not in citation:
        print("CITATION.cff must declare canonical Zenodo DOI 10.5281/zenodo.21701861.")
        return 1
    if "doi: \"10.5281/zenodo.21701861\"" not in citation and "doi: 10.5281/zenodo.21701861" not in citation:
        print("CITATION.cff must set top-level doi to 10.5281/zenodo.21701861.")
        return 1
    if "10.5281/zenodo.21500899" not in citation:
        print("CITATION.cff should retain historical Zenodo DOI 10.5281/zenodo.21500899.")
        return 1
    if "10.5281/zenodo.20543779" not in citation:
        print("CITATION.cff should retain historical Zenodo DOI 10.5281/zenodo.20543779.")
        return 1
    if "zenodo.TBD" in citation or "zenodo.XXXXXXX" in citation or "zenodo.PLACEHOLDER" in citation:
        print("CITATION.cff still contains a placeholder Zenodo DOI.")
        return 1
    if "family-names: Andrés" not in citation or "given-names: César" not in citation:
        print("CITATION.cff should list author César Andrés.")
        return 1
    if "family-names: Martín-Moncunill" not in citation or "given-names: David" not in citation:
        print("CITATION.cff should list author David Martín-Moncunill.")
        return 1
    if "0009-0001-8968-3404" not in citation:
        print("CITATION.cff should include ORCID 0009-0001-8968-3404.")
        return 1
    if "0000-0003-2422-9005" not in citation:
        print("CITATION.cff should include ORCID 0000-0003-2422-9005.")
        return 1
    zenodo = (ROOT / ".zenodo.json").read_text(encoding="utf-8")
    if "Martín-Moncunill, David" not in zenodo and "Martin-Moncunill, David" not in zenodo:
        print(".zenodo.json should list creator Martín-Moncunill, David.")
        return 1

    if "version: 1.0.0" not in citation and 'version: "1.0.0"' not in citation:
        print("CITATION.cff must declare software version 1.0.0.")
        return 1

    py_version = _read_pyproject_version()
    if py_version != "1.0.0":
        print(f"Unexpected pyproject version: {py_version} (expected 1.0.0)")
        return 1

    import localgovbench

    if localgovbench.__version__ != py_version:
        print(
            f"Runtime __version__ ({localgovbench.__version__}) "
            f"!= pyproject.toml ({py_version})"
        )
        return 1

    lock = (ROOT / "localgovbench_measurement_validation/affordance/locks/corpus_lock_v1.json").read_text(
        encoding="utf-8"
    )
    if "canonical_path" not in lock or "portable_path" not in lock:
        print("corpus_lock_v1.json must include canonical_path and portable_path.")
        return 1

    for rel in (
        "reports/README.md",
        "results/README.md",
        "localgovbench_measurement_validation/pilot_public_satisfiability/README.md",
    ):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not any(m in text for m in LEGACY_NOTICE_MARKERS):
            print(f"{rel} missing legacy/non-DF empirical-results notice.")
            return 1

    affordance_readme = (
        ROOT / "localgovbench_measurement_validation/affordance/README.md"
    ).read_text(encoding="utf-8")
    if "](coding/pilot_round_01/README.md)" not in affordance_readme:
        print("affordance/README.md must link to coding/pilot_round_01/README.md")
        return 1

    next_release = (ROOT / "docs/releases/NEXT_RELEASE.md").read_text(encoding="utf-8")
    if "10.5281/zenodo.NEXT_DOI_TBD" not in next_release and "NEXT_DOI_TBD" not in next_release:
        print("NEXT_RELEASE.md must include an explicit NEXT_DOI_TBD placeholder.")
        return 1
    if "v0.2.0" not in next_release or "unchanged" not in next_release.lower():
        print("NEXT_RELEASE.md must state that historical v0.2.0 remains unchanged.")
        return 1
    if "10.5281/zenodo.21701861" not in next_release:
        print("NEXT_RELEASE.md must name canonical DOI 10.5281/zenodo.21701861.")
        return 1
    if "21701861" not in (ROOT / "README.md").read_text(encoding="utf-8"):
        print("README.md must cite canonical DOI 10.5281/zenodo.21701861.")
        return 1
    if "21701861" not in (ROOT / ".zenodo.json").read_text(encoding="utf-8"):
        print(".zenodo.json must reference canonical DOI 10.5281/zenodo.21701861.")
        return 1

    pilot_outputs = ROOT / "localgovbench_measurement_validation/pilot_public_satisfiability/outputs"
    required_pilot = [
        "field_criterion_coverage_matrix.csv",
        "criterion_satisfiability_summary.csv",
        "gate_reachability_summary.csv",
        "minimum_internal_evidence_set.csv",
    ]
    for name in required_pilot:
        if not (pilot_outputs / name).is_file():
            print(f"Missing frozen pilot output: {pilot_outputs / name}")
            return 1

    example = (ROOT / "examples" / "example_assessment.yaml").read_text(encoding="utf-8")
    if "synthetic: true" not in example:
        print("example_assessment.yaml must declare synthetic: true")
        return 1

    print("Repository structure validation passed.")
    print(
        f"Checked {len(REQUIRED_PATHS) + len(DF_REQUIRED_PATHS)} required paths "
        f"(legacy + DF) under {ROOT}"
    )
    print(f"Runtime version={localgovbench.__version__}; stable release=1.0.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
