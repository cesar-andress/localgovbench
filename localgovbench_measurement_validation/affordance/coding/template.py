"""Deterministic generation of schema coding templates from Phase 1 artefacts."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    JUDGMENT_COLUMNS,
    SCHEMA_CODING_TEMPLATE_CSV,
    SPECIFICATION_VERSION,
)
from localgovbench_measurement_validation.affordance.paths import (
    APPLICABILITY_OVERRIDES_YAML,
    CORPUS_LOCK_JSON,
    DISCLOSURE_FUNCTIONS_YAML,
    FIELD_FUNCTION_CANDIDATES_CSV,
    OBJECT_LAYER_BY_SOURCE,
    SCHEMA_INVENTORY_CSV,
    SCHEMA_INVENTORY_VERSION,
)

TEMPLATE_PREPOP_COLUMNS = [
    "coding_unit_id",
    "source_name",
    "schema_object_id",
    "schema_object_type",
    "disclosure_function_id",
    "function_display_name",
    "tier",
    "scoring_role",
    "default_applicability",
    "candidate_observed_fields",
    "known_field_mapping_labels",
    "source_specific_caveats",
    "specification_version",
    "coding_layer_version",
    "corpus_lock_reference",
    "schema_inventory_version",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_functions() -> list[dict[str, Any]]:
    doc = _load_yaml(DISCLOSURE_FUNCTIONS_YAML)
    return list(doc.get("core_functions", [])) + list(doc.get("modules", []))


def load_corpus_lock() -> dict[str, Any]:
    return json.loads(CORPUS_LOCK_JSON.read_text(encoding="utf-8"))


def _default_applicability(
    source: str,
    function_id: str,
    overrides: dict[str, Any],
) -> str:
    defaults = overrides.get("function_defaults", {})
    label = defaults.get(function_id, {}).get("label", "universal")
    for item in overrides.get("overrides", []):
        if "function" in item and item["function"] != function_id:
            continue
        if "functions" in item and function_id not in item["functions"]:
            continue
        if "source" in item and item["source"] != source:
            continue
        if "sources" in item and source not in item["sources"]:
            continue
        return item.get("label", label)
    return label


def _caveats(source: str, function_id: str, overrides: dict[str, Any]) -> str:
    notes: list[str] = []
    obj = overrides.get("inventory_objects", {}).get(source, {})
    if obj.get("notes"):
        notes.append(str(obj["notes"]).strip())
    if function_id == "cf_system_identity":
        notes.append("scoring_role=descriptive_only; not profiled as scored affordance.")
    if source == "UK-ATRS" and function_id == "cf_accountable_body":
        notes.append("organisation_title is never PRIMARY; publisher identity only.")
    if source == "UK-ATRS" and function_id == "cf_purpose":
        notes.append("description is INDIRECT purpose only; never dedicated.")
    if source == "EU-PSTW" and function_id in {
        "cf_data_involvement",
        "om_human_oversight",
        "om_risk_or_impact",
        "om_legal_basis",
        "om_redress_pointer",
    }:
        notes.append("catalogue_inapplicable for register-native disclosure functions.")
    if source == "US-OMB-2025" and function_id in {
        "om_human_oversight",
        "om_redress_pointer",
    }:
        notes.append("conditional high-impact subclass for hi_* fields.")
    if function_id == "om_legal_basis" and source != "NL-ALGO-REG":
        notes.append("jurisdiction_specific; dedicated field absent outside NL export.")
    return " | ".join(notes)


def _candidates_for(source: str, function_id: str) -> list[dict[str, str]]:
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = [
            r
            for r in csv.DictReader(handle)
            if r["source"] == source and r["function_id"] == function_id
        ]
    rows.sort(key=lambda r: (r["mapping_label"], r["raw_field"]))
    return rows


def build_coding_template_rows() -> list[dict[str, str]]:
    lock = load_corpus_lock()
    overrides = _load_yaml(APPLICABILITY_OVERRIDES_YAML)
    functions = load_functions()
    sources = sorted(lock["source_names"])
    rows: list[dict[str, str]] = []

    for source in sources:
        object_type = OBJECT_LAYER_BY_SOURCE[source]
        for fn in functions:
            fid = fn["id"]
            cands = _candidates_for(source, fid)
            observed = [c["raw_field"] for c in cands]
            labels = [f"{c['raw_field']}={c['mapping_label']}" for c in cands]
            unit = {
                "coding_unit_id": f"{source}__{fid}",
                "source_name": source,
                "schema_object_id": source,
                "schema_object_type": object_type,
                "disclosure_function_id": fid,
                "function_display_name": fn["display_name"],
                "tier": fn.get("scope", ""),
                "scoring_role": (
                    "descriptive_only"
                    if fn.get("status") == "core_unscored"
                    else ("core_scored" if fn.get("status") == "core_scored" else "module")
                ),
                "default_applicability": _default_applicability(source, fid, overrides),
                "candidate_observed_fields": "|".join(observed),
                "known_field_mapping_labels": "|".join(labels),
                "source_specific_caveats": _caveats(source, fid, overrides),
                "specification_version": SPECIFICATION_VERSION,
                "coding_layer_version": CODING_LAYER_VERSION,
                "corpus_lock_reference": lock["sha256"],
                "schema_inventory_version": SCHEMA_INVENTORY_VERSION,
            }
            for col in JUDGMENT_COLUMNS:
                unit[col] = ""
            rows.append(unit)

    rows.sort(key=lambda r: (r["source_name"], r["disclosure_function_id"]))
    return rows


def write_coding_template(path: Path | None = None) -> Path:
    path = path or SCHEMA_CODING_TEMPLATE_CSV
    rows = build_coding_template_rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = TEMPLATE_PREPOP_COLUMNS + JUDGMENT_COLUMNS
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def expected_unit_ids() -> list[str]:
    return [r["coding_unit_id"] for r in build_coding_template_rows()]
