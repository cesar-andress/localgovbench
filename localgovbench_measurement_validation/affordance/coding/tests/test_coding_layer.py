"""Tests for Disclosure Functions v1 schema coding layer."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from localgovbench_measurement_validation.affordance.coding.pilot import (
    PILOT_SELECTION,
    build_pilot_manifest_rows,
    write_pilot_manifest,
)
from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_RECORD_SCHEMA,
    SCHEMA_CODING_TEMPLATE_CSV,
)
from localgovbench_measurement_validation.affordance.coding.render_codebook import (
    write_codebook,
)
from localgovbench_measurement_validation.affordance.coding.template import (
    build_coding_template_rows,
    expected_unit_ids,
    write_coding_template,
)
from localgovbench_measurement_validation.affordance.coding.validate import (
    create_adjudication_input,
    export_disagreements,
    validate_coding_csv,
)
from localgovbench_measurement_validation.affordance.paths import OBJECT_LAYER_BY_SOURCE
from localgovbench_measurement_validation.affordance.validate_specs import (
    validate_all_hand_authored,
)


def test_phase1_specs_still_validate():
    assert validate_all_hand_authored() == []


def test_template_deterministic():
    a = build_coding_template_rows()
    b = build_coding_template_rows()
    assert a == b


def test_template_unit_count_and_coverage():
    rows = build_coding_template_rows()
    assert len(rows) == 5 * 11
    sources = {r["source_name"] for r in rows}
    functions = {r["disclosure_function_id"] for r in rows}
    assert sources == set(OBJECT_LAYER_BY_SOURCE)
    assert len(functions) == 11
    assert len(expected_unit_ids()) == len(set(expected_unit_ids()))


def test_no_duplicate_coding_units():
    ids = [r["coding_unit_id"] for r in build_coding_template_rows()]
    assert len(ids) == len(set(ids))


def test_write_template_and_empty_judgments(tmp_path):
    path = write_coding_template(tmp_path / "template.csv")
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 55
    assert all(r["support_level"] == "" for r in rows)
    assert all(r["coder_id"] == "" for r in rows)


def test_schema_file_exists_and_lists_functions():
    schema = json.loads(CODING_RECORD_SCHEMA.read_text(encoding="utf-8"))
    enums = schema["properties"]["disclosure_function_id"]["enum"]
    assert "cf_purpose" in enums
    assert "om_redress_pointer" in enums
    assert schema["properties"]["support_level"]["enum"] == [
        "dedicated",
        "indirect",
        "absent",
    ]


def test_impossible_catalogue_inapplicable_dedicated(tmp_path):
    rows = build_coding_template_rows()
    row = next(r for r in rows if r["coding_unit_id"] == "EU-PSTW__cf_data_involvement")
    row = dict(row)
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "catalogue_inapplicable",
            "support_level": "dedicated",
            "encoding_type": "free_text",
            "documentary_linkage_layer": "none",
            "primary_supporting_fields": "Description",
            "coder_confidence": "high",
            "adjudication_status": "not_required",
        }
    )
    path = tmp_path / "bad.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("catalogue_inapplicable" in e for e in errors)


def test_uk_restrictions(tmp_path):
    rows = build_coding_template_rows()
    row = dict(next(r for r in rows if r["coding_unit_id"] == "UK-ATRS__cf_purpose"))
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "universal",
            "support_level": "dedicated",
            "encoding_type": "free_text",
            "documentary_linkage_layer": "none",
            "primary_supporting_fields": "description",
            "coder_confidence": "high",
            "adjudication_status": "pending",
        }
    )
    path = tmp_path / "uk.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("UK description" in e for e in errors)

    row2 = dict(
        next(r for r in rows if r["coding_unit_id"] == "UK-ATRS__cf_accountable_body")
    )
    row2.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "object_specific",
            "support_level": "dedicated",
            "encoding_type": "structured",
            "documentary_linkage_layer": "none",
            "primary_supporting_fields": "organisation_title",
            "coder_confidence": "high",
            "adjudication_status": "pending",
        }
    )
    path2 = tmp_path / "uk2.csv"
    with path2.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row2.keys()))
        writer.writeheader()
        writer.writerow(row2)
    errors2 = validate_coding_csv(path2)
    assert any("organisation_title" in e for e in errors2)


def test_pstw_outcome_and_nl_proportionality(tmp_path):
    rows = build_coding_template_rows()
    row = dict(next(r for r in rows if r["coding_unit_id"] == "EU-PSTW__om_risk_or_impact"))
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "catalogue_inapplicable",
            "support_level": "absent",
            "encoding_type": "not_applicable",
            "documentary_linkage_layer": "not_applicable",
            "indirect_supporting_fields": "Improved Public Service",
            "coder_confidence": "medium",
            "adjudication_status": "pending",
        }
    )
    # even with absent, listing outcome as indirect evidence for risk should fail
    row["support_level"] = "indirect"
    path = tmp_path / "pstw.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("outcome flag" in e or "catalogue_inapplicable" in e for e in errors)

    row_nl = dict(next(r for r in rows if r["coding_unit_id"] == "NL-ALGO-REG__cf_purpose"))
    row_nl.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "universal",
            "support_level": "indirect",
            "encoding_type": "free_text",
            "documentary_linkage_layer": "none",
            "indirect_supporting_fields": "proportionality",
            "coder_confidence": "low",
            "adjudication_status": "pending",
        }
    )
    path_nl = tmp_path / "nl.csv"
    with path_nl.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row_nl.keys()))
        writer.writeheader()
        writer.writerow(row_nl)
    errors_nl = validate_coding_csv(path_nl)
    assert any("proportionality" in e for e in errors_nl)


def test_rejected_field_as_primary(tmp_path):
    rows = build_coding_template_rows()
    row = dict(next(r for r in rows if r["coding_unit_id"] == "US-OMB-2025__cf_purpose"))
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "universal",
            "support_level": "dedicated",
            "encoding_type": "free_text",
            "documentary_linkage_layer": "none",
            "primary_supporting_fields": "topic_area",
            "coder_confidence": "high",
            "adjudication_status": "pending",
        }
    )
    path = tmp_path / "rej.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("REJECTED field" in e for e in errors)


def test_adjudicated_value_before_adjudication(tmp_path):
    rows = build_coding_template_rows()
    row = dict(next(r for r in rows if r["coding_unit_id"] == "NL-ALGO-REG__cf_purpose"))
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "universal",
            "support_level": "dedicated",
            "encoding_type": "free_text",
            "documentary_linkage_layer": "none",
            "primary_supporting_fields": "goal",
            "coder_confidence": "high",
            "adjudication_status": "pending",
            "adjudicated_value": "dedicated",
        }
    )
    path = tmp_path / "adj.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("adjudicated_value" in e for e in errors)


def test_unknown_requires_unresolved(tmp_path):
    rows = build_coding_template_rows()
    row = dict(next(r for r in rows if r["coding_unit_id"] == "CA-GC-AI-REG__om_legal_basis"))
    row.update(
        {
            "coder_id": "A",
            "coding_timestamp": "2026-07-23T00:00:00Z",
            "applicability_label": "unknown",
            "support_level": "absent",
            "encoding_type": "not_applicable",
            "documentary_linkage_layer": "not_applicable",
            "coder_confidence": "low",
            "adjudication_status": "pending",
            "unresolved_issue": "",
        }
    )
    path = tmp_path / "unk.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    errors = validate_coding_csv(path)
    assert any("unresolved_issue" in e for e in errors)


def test_identity_descriptive_only():
    row = next(
        r for r in build_coding_template_rows() if r["disclosure_function_id"] == "cf_system_identity"
    )
    assert row["scoring_role"] == "descriptive_only"


def test_disagreement_export_and_adjudication(tmp_path):
    rows = build_coding_template_rows()
    base = dict(next(r for r in rows if r["coding_unit_id"] == "NL-ALGO-REG__cf_purpose"))
    a = dict(base)
    b = dict(base)
    common = {
        "coding_timestamp": "2026-07-23T00:00:00Z",
        "applicability_label": "universal",
        "encoding_type": "free_text",
        "documentary_linkage_layer": "none",
        "primary_supporting_fields": "goal",
        "coder_confidence": "high",
        "adjudication_status": "pending",
    }
    a.update(common, coder_id="A", support_level="dedicated")
    b.update(common, coder_id="B", support_level="indirect", primary_supporting_fields="", indirect_supporting_fields="description_short")
    path_a = tmp_path / "a.csv"
    path_b = tmp_path / "b.csv"
    for path, row in [(path_a, a), (path_b, b)]:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
            writer.writeheader()
            writer.writerow(row)
    disagree = tmp_path / "disagree.csv"
    export_disagreements(path_a, path_b, disagree)
    with disagree.open(encoding="utf-8", newline="") as handle:
        drows = list(csv.DictReader(handle))
    assert len(drows) == 1
    adj = tmp_path / "adj_in.csv"
    create_adjudication_input(disagree, adj)
    with adj.open(encoding="utf-8", newline="") as handle:
        arows = list(csv.DictReader(handle))
    assert len(arows) == 1
    assert arows[0]["resolution_status"] == "pending"


def test_pilot_manifest_balanced():
    rows = build_pilot_manifest_rows()
    assert len(rows) == len(PILOT_SELECTION)
    sources = {r["source_name"] for r in rows}
    functions = {r["disclosure_function_id"] for r in rows}
    assert sources == set(OBJECT_LAYER_BY_SOURCE)
    assert len(functions) >= 8
    assert any("catalogue_inapplicable" in r["selection_rationale"] for r in rows)
    assert any("uk_api_slim" in r["selection_rationale"] for r in rows)
    assert any("conditional" in r["selection_rationale"] for r in rows)


def test_write_codebook_and_pilot(tmp_path):
    cb = write_codebook(tmp_path / "codebook.md")
    text = cb.read_text(encoding="utf-8")
    assert "cf_purpose" in text
    assert "anti-over-credit" in text.lower() or "anti_overcredit" in text or "Anti-over" in text or "anti-over" in text
    write_pilot_manifest(tmp_path / "pilot.csv")
