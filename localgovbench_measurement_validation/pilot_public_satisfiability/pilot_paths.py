"""Paths for the public-satisfiability pilot (Paper 1 rescue)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PILOT = Path(__file__).resolve().parent

CONFIG_CRITERIA = PILOT / "config" / "localgovbench_criteria_v0.yaml"
DATA_RECORDS = PILOT / "data" / "pilot_programme_records.csv"
SOURCE_REGISTRY = PILOT / "data" / "source_registry_expanded.csv"
OUTPUTS = PILOT / "outputs"
FIGURES = PILOT / "figures"
REPORT = PILOT / "reports" / "pilot_public_satisfiability_report.md"
UPGRADE_REPORT = PILOT / "reports" / "validation_upgrade_report.md"

FIELD_COVERAGE_MATRIX = OUTPUTS / "field_criterion_coverage_matrix.csv"
CRITERION_SUMMARY = OUTPUTS / "criterion_satisfiability_summary.csv"
DIMENSION_SUMMARY = OUTPUTS / "dimension_satisfiability_summary.csv"
GATE_SUMMARY = OUTPUTS / "gate_reachability_summary.csv"
PILOT_GO_JSON = OUTPUTS / "pilot_go_decision.json"

PARTITION_AGREEMENT = OUTPUTS / "partition_validation_agreement.csv"
PARTITION_SENSITIVITY = OUTPUTS / "partition_sensitivity_summary.csv"
SENSITIVITY_SCENARIOS = OUTPUTS / "sensitivity_scenarios.csv"
SENSITIVITY_MAIN = OUTPUTS / "sensitivity_main_results.csv"
MINIMUM_INTERNAL = OUTPUTS / "minimum_internal_evidence_set.csv"

FIG_SHORTFALL_HEATMAP = FIGURES / "evidence_shortfall_gradient_heatmap.png"
FIG_SENSITIVITY = FIGURES / "sensitivity_public_satisfiability.png"
FIG_MIN_INTERNAL = FIGURES / "minimum_internal_evidence_set_by_dimension.png"
FIG_CROSS_JURIS = FIGURES / "cross_jurisdiction_ceiling_comparison.png"

DETECTOR_SUMMARY = OUTPUTS / "detector_reliability_summary.csv"
DETECTOR_BY_SOURCE = OUTPUTS / "detector_reliability_by_source.csv"
DETECTOR_REPORT = OUTPUTS / "detector_reliability_report.md"
FIG_DETECTOR = FIGURES / "detector_reliability_by_source.png"

UNIT_SUMMARY = OUTPUTS / "unit_commensurability_summary.csv"
UNIT_SENSITIVITY = OUTPUTS / "unit_commensurability_sensitivity.csv"
UNIT_REPORT = PILOT / "reports" / "unit_commensurability_report.md"
FIG_UNIT_STABILITY = FIGURES / "unit_commensurability_stability.png"
FIG_UNIT_PARTITION = FIGURES / "unit_commensurability_partition_comparison.png"
