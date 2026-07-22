"""Validate hand-authored affordance specification artefacts."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import yaml

from localgovbench_measurement_validation.affordance.paths import (
    APPLICABILITY_OVERRIDES_YAML,
    DISCLOSURE_FUNCTIONS_YAML,
    FIELD_FUNCTION_CANDIDATES_CSV,
    FIELD_NORMALIZATION_YAML,
    LINKAGE_FIELD_TYPES_CSV,
    REALIZATION_RULES_YAML,
)

PROHIBITED = {
    "readiness",
    "maturity",
    "shortfall",
    "composite_score",
    "jurisdiction_ranking",
    "compliance_score",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_function_ids() -> dict[str, dict[str, Any]]:
    doc = _load_yaml(DISCLOSURE_FUNCTIONS_YAML)
    functions: dict[str, dict[str, Any]] = {}
    for item in doc.get("core_functions", []):
        functions[item["id"]] = item
    for item in doc.get("modules", []):
        functions[item["id"]] = item
    return functions


def validate_disclosure_functions() -> list[str]:
    errors: list[str] = []
    doc = _load_yaml(DISCLOSURE_FUNCTIONS_YAML)
    if doc.get("meta", {}).get("version") != "1.0.0":
        errors.append("disclosure_functions version must be 1.0.0")

    functions = load_function_ids()
    ids = list(functions)
    if len(ids) != len(set(ids)):
        errors.append("Duplicate function identifiers")

    expected = {
        "cf_system_identity",
        "cf_purpose",
        "cf_operational_status",
        "cf_accountable_body",
        "cf_data_involvement",
        "om_human_oversight",
        "om_risk_or_impact",
        "om_legal_basis",
        "om_supplier",
        "om_technical_method",
        "om_redress_pointer",
    }
    if set(ids) != expected:
        errors.append(f"Unexpected function set: {sorted(set(ids) ^ expected)}")

    identity = functions["cf_system_identity"]
    if identity.get("status") != "core_unscored":
        errors.append("cf_system_identity must be core_unscored / descriptive_only")

    prohibited = set(doc.get("meta", {}).get("prohibited_constructs", []))
    if not PROHIBITED.issubset(prohibited):
        errors.append("Missing prohibited constructs in disclosure_functions meta")

    # No active scoring field may be a prohibited construct name
    for fid, item in functions.items():
        blob = " ".join(str(v) for v in item.values()).lower()
        for bad in ("readiness_score", "maturity_score", "shortfall_level", "compliance_score"):
            if bad in blob:
                errors.append(f"{fid} contains prohibited construct token {bad}")
    return errors


def validate_candidates() -> list[str]:
    errors: list[str] = []
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    allowed = {"PRIMARY", "SECONDARY", "INDIRECT", "REJECTED"}
    function_ids = set(load_function_ids())

    for i, row in enumerate(rows, start=2):
        if row["mapping_label"] not in allowed:
            errors.append(f"line {i}: invalid mapping_label {row['mapping_label']}")
        if row["function_id"] not in function_ids:
            errors.append(f"line {i}: unknown function_id {row['function_id']}")

    def labels(source: str, field: str, function: str) -> set[str]:
        return {
            r["mapping_label"]
            for r in rows
            if r["source"] == source
            and r["raw_field"] == field
            and r["function_id"] == function
        }

    if "PRIMARY" in labels("UK-ATRS", "organisation_title", "cf_accountable_body"):
        errors.append("UK organisation_title must not be PRIMARY accountable body")
    if labels("UK-ATRS", "organisation_title", "cf_accountable_body") != {"INDIRECT"}:
        errors.append("UK organisation_title must be INDIRECT for accountable body")
    if "PRIMARY" in labels("UK-ATRS", "description", "cf_purpose"):
        errors.append("UK description must not be PRIMARY purpose")
    if "INDIRECT" not in labels("UK-ATRS", "description", "cf_purpose"):
        errors.append("UK description must be INDIRECT purpose")

    if labels("US-OMB-2025", "has_pii", "cf_data_involvement") != {"PRIMARY"}:
        errors.append("US has_pii must be PRIMARY data involvement")
    if labels("CA-GC-AI-REG", "involves_personal_information", "cf_data_involvement") != {
        "PRIMARY"
    }:
        errors.append("CA involves_personal_information must be PRIMARY data involvement")
    if labels("NL-ALGO-REG", "source_data", "cf_data_involvement") != {"PRIMARY"}:
        errors.append("NL source_data must be PRIMARY data involvement")
    if labels("NL-ALGO-REG", "publication_category", "om_risk_or_impact") != {"SECONDARY"}:
        errors.append("NL publication_category must be SECONDARY risk")
    if "PRIMARY" in labels("NL-ALGO-REG", "impacttoetsen", "om_risk_or_impact"):
        errors.append("NL impacttoetsen must not be PRIMARY risk")

    # PSTW outcome flags rejected for risk
    for row in rows:
        if (
            row["source"] == "EU-PSTW"
            and row["function_id"] == "om_risk_or_impact"
            and row["raw_field"].startswith("Improved")
            and row["mapping_label"] != "REJECTED"
        ):
            errors.append(f"PSTW outcome flag not REJECTED: {row['raw_field']}")

    prop = [
        r
        for r in rows
        if r["source"] == "NL-ALGO-REG" and r["raw_field"] == "proportionality"
    ]
    if not prop:
        errors.append("NL proportionality mappings missing")
    if any(r["mapping_label"] != "REJECTED" for r in prop):
        errors.append("NL proportionality must be REJECTED for all mapped functions")

    return errors


def validate_applicability() -> list[str]:
    errors: list[str] = []
    doc = _load_yaml(APPLICABILITY_OVERRIDES_YAML)
    objects = doc.get("inventory_objects", {})
    if objects.get("UK-ATRS", {}).get("object_type") != "search_api_slim":
        errors.append("UK-ATRS must be labelled search_api_slim")
    if objects.get("EU-PSTW", {}).get("peer_status") != "contrast":
        errors.append("EU-PSTW must be contrast catalogue")
    defaults = doc.get("function_defaults", {})
    if defaults.get("cf_system_identity", {}).get("profile_role") != "descriptive_only":
        errors.append("identity must be descriptive_only")
    return errors


def validate_normalization() -> list[str]:
    errors: list[str] = []
    doc = _load_yaml(FIELD_NORMALIZATION_YAML)
    forbidden = {(f["source"], f["raw_field"]) for f in doc.get("forbidden_as_observed", [])}
    required_forbidden = {
        ("US-OMB-2025", "human_roles"),
        ("US-OMB-2025", "data_used_for_training"),
        ("US-OMB-2025", "data_used_for_inference"),
        ("US-OMB-2025", "data_used_for_evaluation"),
        ("NL-ALGO-REG", "department"),
    }
    if not required_forbidden.issubset(forbidden):
        errors.append("Missing forbidden_as_observed entries")
    rules = {(r["source"], r["raw_field"]): r for r in doc.get("rules", [])}
    pstw = rules.get(("EU-PSTW", " Status"))
    if not pstw or pstw.get("normalized_field") != "status":
        errors.append("PSTW Status normalization rule missing or incorrect")
    return errors


def validate_linkage() -> list[str]:
    errors: list[str] = []
    with LINKAGE_FIELD_TYPES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    layers = {"generic_url", "record_locator", "function_specific"}
    for row in rows:
        if row["linkage_layer"] not in layers:
            errors.append(f"Invalid linkage_layer: {row['linkage_layer']}")
    return errors


def validate_realization() -> list[str]:
    errors: list[str] = []
    doc = _load_yaml(REALIZATION_RULES_YAML)
    data = doc.get("functions", {}).get("cf_data_involvement", {})
    preferred = data.get("preferred_by_source", {})
    if preferred.get("US-OMB-2025") != "has_pii":
        errors.append("realization preferred US data involvement must be has_pii")
    if preferred.get("CA-GC-AI-REG") != "involves_personal_information":
        errors.append("realization preferred CA data involvement mismatch")
    if preferred.get("NL-ALGO-REG") != "source_data":
        errors.append("realization preferred NL data involvement mismatch")
    return errors


def validate_all_hand_authored() -> list[str]:
    errors: list[str] = []
    for path in [
        DISCLOSURE_FUNCTIONS_YAML,
        FIELD_NORMALIZATION_YAML,
        FIELD_FUNCTION_CANDIDATES_CSV,
        APPLICABILITY_OVERRIDES_YAML,
        REALIZATION_RULES_YAML,
        LINKAGE_FIELD_TYPES_CSV,
    ]:
        if not path.is_file():
            errors.append(f"Missing artefact: {path}")
    errors.extend(validate_disclosure_functions())
    errors.extend(validate_normalization())
    errors.extend(validate_candidates())
    errors.extend(validate_applicability())
    errors.extend(validate_realization())
    errors.extend(validate_linkage())
    return errors
