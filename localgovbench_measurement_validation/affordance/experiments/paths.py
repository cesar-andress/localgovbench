"""Paths for the Phase 3 experiment package."""

from __future__ import annotations

from pathlib import Path

from localgovbench_measurement_validation.affordance.paths import AFFORDANCE_ROOT

EXPERIMENTS_ROOT = AFFORDANCE_ROOT / "experiments"
EXPERIMENT_CONFIG = EXPERIMENTS_ROOT / "config"
EXPERIMENT_INPUTS = EXPERIMENTS_ROOT / "inputs"
EXPERIMENT_OUTPUTS = EXPERIMENTS_ROOT / "outputs"
EXPERIMENT_MANIFESTS = EXPERIMENTS_ROOT / "manifests"
EXPERIMENT_PROVENANCE = EXPERIMENTS_ROOT / "provenance"
EXPERIMENT_VALIDATION = EXPERIMENTS_ROOT / "validation"
EXPERIMENT_TESTS = EXPERIMENTS_ROOT / "tests"
EXPERIMENT_FIXTURES = EXPERIMENTS_ROOT / "fixtures"

PIPELINE_CONFIG_YAML = EXPERIMENT_CONFIG / "experiment_pipeline_v1.yaml"
MATRIX_SCHEMA_JSON = EXPERIMENT_CONFIG / "schema_affordance_matrix_v1.schema.json"

EXPERIMENT_PIPELINE_VERSION = "1.0.0"
CODING_VERSION = "1.0.0"
SPECIFICATION_VERSION = "1.0.0"

MATRIX_COLUMNS = [
    "schema_object_id",
    "source_name",
    "schema_object_type",
    "disclosure_function_id",
    "support_level",
    "applicability_label",
    "encoding_type",
    "documentary_linkage_layer",
    "function_specific_link_type",
    "coder_confidence",
    "adjudication_status",
    "adjudicated_from",
    "coding_round_id",
    "specification_version",
    "coding_version",
    "corpus_lock_sha256",
    "schema_inventory_version",
    "experiment_id",
    "pipeline_version",
]

REALIZATION_TEMPLATE_COLUMNS = [
    "schema_object_id",
    "source_name",
    "disclosure_function_id",
    "support_level",
    "applicability_label",
    "realization_status",
    "realization_notes",
    "corpus_lock_sha256",
    "specification_version",
    "experiment_id",
]
