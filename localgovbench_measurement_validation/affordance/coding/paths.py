"""Schema coding layer paths and frozen enumerations (Disclosure Functions v1)."""

from __future__ import annotations

from pathlib import Path

from localgovbench_measurement_validation.affordance.paths import AFFORDANCE_ROOT

CODING_ROOT = AFFORDANCE_ROOT / "coding"
CODING_CONFIG = CODING_ROOT / "config"
CODING_TEMPLATES = CODING_ROOT / "templates"
CODING_EXAMPLES = CODING_ROOT / "examples"
CODING_ADJUDICATION = CODING_ROOT / "adjudication"
CODING_OUTPUTS = CODING_ROOT / "outputs"
CODING_TESTS = CODING_ROOT / "tests"

CODING_LABELS_YAML = CODING_CONFIG / "coding_labels_v1.yaml"
CODING_RECORD_SCHEMA = CODING_CONFIG / "schema_coding_record_v1.schema.json"
CODEBOOK_MD = CODING_CONFIG / "codebook_affordance_v1.md"
CODER_INSTRUCTIONS_MD = CODING_CONFIG / "coder_instructions_v1.md"
DOUBLE_CODING_PROTOCOL_MD = CODING_CONFIG / "double_coding_protocol_v1.md"
IRR_PLAN_MD = CODING_CONFIG / "irr_analysis_plan_v1.md"
ADJUDICATION_PROTOCOL_MD = CODING_ADJUDICATION / "adjudication_protocol_v1.md"
ADJUDICATION_TEMPLATE_CSV = CODING_ADJUDICATION / "adjudication_template_v1.csv"
WORKED_EXAMPLES_MD = CODING_EXAMPLES / "worked_examples_v1.md"
PILOT_MANIFEST_CSV = CODING_TEMPLATES / "pilot_coding_manifest_v1.csv"
SCHEMA_CODING_TEMPLATE_CSV = CODING_TEMPLATES / "schema_coding_template_v1.csv"

SPECIFICATION_VERSION = "1.0.0"
CODING_LAYER_VERSION = "1.0.0"

SUPPORT_LEVELS = ("dedicated", "indirect", "absent")
APPLICABILITY_LABELS = (
    "universal",
    "conditional",
    "jurisdiction_specific",
    "object_specific",
    "catalogue_inapplicable",
    "unknown",
)
ENCODING_TYPES = ("free_text", "structured", "mixed", "other", "not_applicable")
LINKAGE_LAYERS = (
    "generic_url",
    "record_locator",
    "function_specific",
    "none",
    "not_applicable",
)
CONFIDENCE_LEVELS = ("high", "medium", "low")
FUNCTION_SPECIFIC_LINK_TYPES = (
    "impact_assessment",
    "dataset_documentation",
    "source_code",
    "legal_or_policy_document",
    "procurement_document",
    "appeal_process",
    "",
    "null",
)

# Columns left empty for human judgment in the coding template.
JUDGMENT_COLUMNS = [
    "coder_id",
    "coding_timestamp",
    "applicability_label",
    "applicability_rationale",
    "support_level",
    "encoding_type",
    "documentary_linkage_layer",
    "function_specific_link_type",
    "candidate_fields_reviewed",
    "primary_supporting_fields",
    "indirect_supporting_fields",
    "rejected_fields_reviewed",
    "generic_narrative_used",
    "anti_overcredit_check",
    "coder_confidence",
    "coder_rationale",
    "unresolved_issue",
    "adjudication_status",
    "adjudicated_value",
    "adjudicator_id",
    "notes",
]

GENERIC_NARRATIVE_FIELDS = frozenset(
    {
        "description",
        "Description",
        "description_short",
        "description_ai_system_en",
        "description_ai_system_fr",
        "additional information",
        "notes",
        "summary",
    }
)
