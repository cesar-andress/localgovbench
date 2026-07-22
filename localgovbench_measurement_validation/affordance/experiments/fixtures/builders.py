"""Helpers to synthesize minimal valid completed coding fixtures for tests."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.coding.template import (
    load_corpus_lock,
)
from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    SPECIFICATION_VERSION,
)
from localgovbench_measurement_validation.affordance.paths import (
    OBJECT_LAYER_BY_SOURCE,
    SCHEMA_INVENTORY_VERSION,
)


def make_completed_row(
    source: str,
    function_id: str,
    *,
    coder_id: str,
    support_level: str = "absent",
    applicability_label: str = "universal",
    encoding_type: str = "not_applicable",
    documentary_linkage_layer: str = "none",
    primary_supporting_fields: str = "",
    indirect_supporting_fields: str = "",
    confidence: str = "high",
) -> dict[str, Any]:
    lock = load_corpus_lock()
    unit = f"{source}__{function_id}"
    return {
        "coding_unit_id": unit,
        "coding_record_id": f"{unit}__{coder_id}",
        "coding_round_id": "pilot_v1",
        "source_name": source,
        "schema_object_id": source,
        "schema_object_type": OBJECT_LAYER_BY_SOURCE[source],
        "disclosure_function_id": function_id,
        "coder_id": coder_id,
        "coding_timestamp": "2026-07-23T00:00:00+00:00",
        "specification_version": SPECIFICATION_VERSION,
        "coding_layer_version": CODING_LAYER_VERSION,
        "corpus_lock_reference": lock["sha256"],
        "schema_inventory_reference": "schema_inventory_v1.csv",
        "schema_inventory_version": SCHEMA_INVENTORY_VERSION,
        "applicability_label": applicability_label,
        "applicability_rationale": "fixture",
        "support_level": support_level,
        "encoding_type": encoding_type,
        "documentary_linkage_layer": documentary_linkage_layer,
        "function_specific_link_type": "",
        "candidate_fields_reviewed": "",
        "primary_supporting_fields": primary_supporting_fields,
        "indirect_supporting_fields": indirect_supporting_fields,
        "rejected_fields_reviewed": "",
        "generic_narrative_used": "false",
        "anti_overcredit_check": "ok",
        "coder_confidence": confidence,
        "coder_rationale": "fixture rationale",
        "unresolved_issue": "",
        "adjudication_status": "pending",
        "adjudicated_value": "",
        "adjudicator_id": "",
        "notes": "",
        "scoring_role": "core_scored",
    }


def write_coding_csv(path: Path, rows: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_coding_json(path: Path, rows: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"records": rows}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def write_adjudication_csv(
    path: Path,
    *,
    unit: str,
    source: str,
    function_id: str,
    decision: str,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "coding_unit_id",
        "source_name",
        "disclosure_function_id",
        "coder_a_value",
        "coder_b_value",
        "disagreement_type",
        "relevant_fields",
        "relevant_codebook_rule",
        "adjudicator_decision",
        "adjudicator_rationale",
        "codebook_ambiguity_flag",
        "specification_ambiguity_flag",
        "resolution_status",
        "date",
        "version",
        "adjudicator_id",
    ]
    row = {
        "coding_unit_id": unit,
        "source_name": source,
        "disclosure_function_id": function_id,
        "coder_a_value": "",
        "coder_b_value": "",
        "disagreement_type": "support_level",
        "relevant_fields": "",
        "relevant_codebook_rule": "",
        "adjudicator_decision": decision,
        "adjudicator_rationale": "fixture adjudication",
        "codebook_ambiguity_flag": "false",
        "specification_ambiguity_flag": "false",
        "resolution_status": "resolved",
        "date": "2026-07-23",
        "version": "1.0.0",
        "adjudicator_id": "adj1",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)
    return path
