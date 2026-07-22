"""Canonical paths for the affordance specification layer."""

from __future__ import annotations

from pathlib import Path

AFFORDANCE_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = AFFORDANCE_ROOT / "config"
LOCKS_DIR = AFFORDANCE_ROOT / "locks"
OUTPUTS_DIR = AFFORDANCE_ROOT / "outputs"
TESTS_DIR = AFFORDANCE_ROOT / "tests"

REPO_ROOT = AFFORDANCE_ROOT.parents[1]
CORPUS_PATH = (
    REPO_ROOT
    / "localgovbench_measurement_validation"
    / "pilot_public_satisfiability"
    / "data"
    / "pilot_programme_records.csv"
)

CORPUS_LOCK_JSON = LOCKS_DIR / "corpus_lock_v1.json"
CORPUS_LOCK_MD = LOCKS_DIR / "corpus_lock_v1.md"
SCHEMA_INVENTORY_CSV = OUTPUTS_DIR / "schema_inventory_v1.csv"
SCHEMA_INVENTORY_JSON = OUTPUTS_DIR / "schema_inventory_v1.json"

DISCLOSURE_FUNCTIONS_YAML = CONFIG_DIR / "disclosure_functions_v1.yaml"
FIELD_NORMALIZATION_YAML = CONFIG_DIR / "field_normalization_rules_v1.yaml"
FIELD_FUNCTION_CANDIDATES_CSV = CONFIG_DIR / "field_function_candidates_v1.csv"
APPLICABILITY_OVERRIDES_YAML = CONFIG_DIR / "applicability_overrides_v1.yaml"
REALIZATION_RULES_YAML = CONFIG_DIR / "realization_rules_v1.yaml"
LINKAGE_FIELD_TYPES_CSV = CONFIG_DIR / "linkage_field_types_v1.csv"

SCHEMA_INVENTORY_VERSION = "1.0.0"
CORPUS_LOCK_VERSION = "1.0.0"

# Phase 2 coding layer (see affordance/coding/)
CODING_ROOT = AFFORDANCE_ROOT / "coding"

OBJECT_LAYER_BY_SOURCE: dict[str, str] = {
    "US-OMB-2025": "use_case_inventory",
    "CA-GC-AI-REG": "ai_system_register",
    "NL-ALGO-REG": "algorithm_register",
    "EU-PSTW": "case_catalogue",
    "UK-ATRS": "search_api_slim",
}
