"""Tests for Disclosure Functions v1 specification layer."""

from __future__ import annotations

import csv
import json

import pytest

from localgovbench_measurement_validation.affordance.corpus_lock import (
    build_corpus_lock,
    write_corpus_lock,
)
from localgovbench_measurement_validation.affordance.nonempty import (
    classify_value,
    is_nonempty_for_population,
)
from localgovbench_measurement_validation.affordance.paths import (
    APPLICABILITY_OVERRIDES_YAML,
    CORPUS_LOCK_JSON,
    CORPUS_PATH,
    DISCLOSURE_FUNCTIONS_YAML,
    FIELD_FUNCTION_CANDIDATES_CSV,
    OBJECT_LAYER_BY_SOURCE,
    SCHEMA_INVENTORY_CSV,
)
from localgovbench_measurement_validation.affordance.schema_inventory import (
    build_schema_inventory,
    write_schema_inventory,
)
from localgovbench_measurement_validation.affordance.validate_specs import (
    load_function_ids,
    validate_all_hand_authored,
)

import yaml

# Aggregate corpus is intentionally gitignored; CI validates frozen lock/inventory.
_CORPUS_AVAILABLE = CORPUS_PATH.is_file()
requires_corpus = pytest.mark.skipif(
    not _CORPUS_AVAILABLE,
    reason="pilot_programme_records.csv absent (gitignored; rebuild locally to run)",
)


@pytest.fixture(scope="module")
def corpus_lock():
    """Prefer live rebuild when corpus bytes exist; else use frozen lock artefact."""
    if _CORPUS_AVAILABLE:
        return build_corpus_lock()
    assert CORPUS_LOCK_JSON.is_file(), f"Frozen corpus lock missing: {CORPUS_LOCK_JSON}"
    return json.loads(CORPUS_LOCK_JSON.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def inventory(corpus_lock):
    if _CORPUS_AVAILABLE:
        return build_schema_inventory(corpus_lock=corpus_lock)
    assert SCHEMA_INVENTORY_CSV.is_file(), f"Frozen inventory missing: {SCHEMA_INVENTORY_CSV}"
    with SCHEMA_INVENTORY_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_hand_authored_specs_validate():
    errors = validate_all_hand_authored()
    assert errors == [], errors


def test_source_counts_sum_to_total(corpus_lock):
    total = corpus_lock["total_record_count"]
    assert total == 7434
    assert sum(corpus_lock["record_count_per_source"].values()) == total


def test_raw_fields_json_confirmed(corpus_lock):
    assert corpus_lock["raw_fields_json_column_confirmed"] is True
    assert "raw_fields_json" in corpus_lock["columns"]


@requires_corpus
def test_every_observed_field_in_inventory(inventory):
    # Rebuild observed keys independently
    observed: dict[str, set[str]] = {}
    with CORPUS_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            source = row["source_name"]
            raw = json.loads(row["raw_fields_json"])
            observed.setdefault(source, set()).update(raw.keys())
    inventory_keys = {
        (r["source_name"], r["raw_field_name"]) for r in inventory
    }
    for source, keys in observed.items():
        for key in keys:
            assert (source, key) in inventory_keys


def test_no_unobserved_forbidden_fields(inventory):
    present = {(r["source_name"], r["raw_field_name"]) for r in inventory}
    forbidden = [
        ("US-OMB-2025", "human_roles"),
        ("US-OMB-2025", "data_used_for_training"),
        ("US-OMB-2025", "data_used_for_inference"),
        ("US-OMB-2025", "data_used_for_evaluation"),
        ("NL-ALGO-REG", "department"),
    ]
    for item in forbidden:
        assert item not in present


def test_pstw_status_raw_preserved_and_normalized(inventory):
    rows = [r for r in inventory if r["source_name"] == "EU-PSTW" and r["raw_field_name"] == " Status"]
    assert len(rows) == 1
    assert rows[0]["normalized_field_name"] == "status"
    assert rows[0]["raw_field_name"] == " Status"


def test_canadian_en_fr_traceable(inventory):
    ca = [r for r in inventory if r["source_name"] == "CA-GC-AI-REG"]
    names = {r["raw_field_name"] for r in ca}
    assert "description_ai_system_en" in names
    assert "description_ai_system_fr" in names
    assert "name_ai_system_en" in names
    assert "name_ai_system_fr" in names


def test_uk_labelled_search_api_slim(corpus_lock):
    assert corpus_lock["object_layer_per_source"]["UK-ATRS"] == "search_api_slim"
    assert OBJECT_LAYER_BY_SOURCE["UK-ATRS"] == "search_api_slim"
    with APPLICABILITY_OVERRIDES_YAML.open(encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    assert doc["inventory_objects"]["UK-ATRS"]["object_type"] == "search_api_slim"


def test_uk_organisation_title_not_primary_accountable():
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    hits = [
        r
        for r in rows
        if r["source"] == "UK-ATRS"
        and r["raw_field"] == "organisation_title"
        and r["function_id"] == "cf_accountable_body"
    ]
    assert hits and all(r["mapping_label"] == "INDIRECT" for r in hits)


def test_uk_description_not_primary_purpose():
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    hits = [
        r
        for r in rows
        if r["source"] == "UK-ATRS"
        and r["raw_field"] == "description"
        and r["function_id"] == "cf_purpose"
    ]
    assert hits and all(r["mapping_label"] == "INDIRECT" for r in hits)


def test_pstw_outcome_flags_rejected_for_risk():
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    flags = [
        r
        for r in rows
        if r["source"] == "EU-PSTW"
        and r["function_id"] == "om_risk_or_impact"
        and r["raw_field"].startswith("Improved")
    ]
    assert flags
    assert all(r["mapping_label"] == "REJECTED" for r in flags)


def test_nl_proportionality_rejected():
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    props = [
        r
        for r in rows
        if r["source"] == "NL-ALGO-REG" and r["raw_field"] == "proportionality"
    ]
    assert props
    assert all(r["mapping_label"] == "REJECTED" for r in props)


def test_unique_function_identifiers():
    ids = list(load_function_ids())
    assert len(ids) == len(set(ids))


def test_identity_descriptive_only():
    functions = load_function_ids()
    assert functions["cf_system_identity"]["status"] == "core_unscored"
    with APPLICABILITY_OVERRIDES_YAML.open(encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    assert (
        doc["function_defaults"]["cf_system_identity"]["profile_role"]
        == "descriptive_only"
    )


def test_no_prohibited_active_scoring_fields():
    with DISCLOSURE_FUNCTIONS_YAML.open(encoding="utf-8") as handle:
        doc = yaml.safe_load(handle)
    prohibited = set(doc["meta"]["prohibited_constructs"])
    for token in (
        "readiness",
        "maturity",
        "shortfall",
        "composite_score",
        "jurisdiction_ranking",
        "compliance_score",
    ):
        assert token in prohibited
    # Active function ids must not be prohibited construct names
    for fid in load_function_ids():
        assert fid not in prohibited


def test_nonempty_treats_no_as_populated():
    assert is_nonempty_for_population("No") is True
    assert is_nonempty_for_population("N") is True
    assert classify_value("No") == "valid_negative_categorical"
    assert is_nonempty_for_population("") is False
    assert is_nonempty_for_population([]) is False
    assert is_nonempty_for_population("n/a") is False
    assert classify_value("Not available") == "invalid_url_placeholder"
    assert is_nonempty_for_population("Not available") is True


@requires_corpus
def test_inventory_deterministic(corpus_lock, tmp_path):
    inv1 = build_schema_inventory(corpus_lock=corpus_lock)
    inv2 = build_schema_inventory(corpus_lock=corpus_lock)
    assert inv1 == inv2


@requires_corpus
def test_write_lock_and_inventory_roundtrip(corpus_lock, inventory, tmp_path, monkeypatch):
    """Write roundtrip must not mutate frozen on-disk lock/inventory artefacts."""
    import localgovbench_measurement_validation.affordance.corpus_lock as corpus_lock_mod
    import localgovbench_measurement_validation.affordance.schema_inventory as inventory_mod

    lock_json = tmp_path / "corpus_lock_v1.json"
    lock_md = tmp_path / "corpus_lock_v1.md"
    inv_csv = tmp_path / "schema_inventory_v1.csv"
    inv_json = tmp_path / "schema_inventory_v1.json"

    monkeypatch.setattr(corpus_lock_mod, "CORPUS_LOCK_JSON", lock_json)
    monkeypatch.setattr(corpus_lock_mod, "CORPUS_LOCK_MD", lock_md)
    monkeypatch.setattr(inventory_mod, "SCHEMA_INVENTORY_CSV", inv_csv)
    monkeypatch.setattr(inventory_mod, "SCHEMA_INVENTORY_JSON", inv_json)

    write_corpus_lock(corpus_lock)
    write_schema_inventory(inventory)
    assert lock_json.is_file()
    assert lock_md.is_file()
    assert inv_csv.is_file()
    with inv_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == len(inventory)
    assert sum(int(r["source_record_count"]) for r in rows) >= 7434


def test_frozen_lock_and_inventory_present_for_ci():
    """CI-safe: tracked lock/inventory artefacts exist without aggregate corpus bytes."""
    assert CORPUS_LOCK_JSON.is_file()
    assert SCHEMA_INVENTORY_CSV.is_file()
    lock = json.loads(CORPUS_LOCK_JSON.read_text(encoding="utf-8"))
    assert lock["total_record_count"] == 7434
    assert lock["sha256"]
    with SCHEMA_INVENTORY_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) > 100
    refs = {r["corpus_lock_reference"] for r in rows}
    assert lock["sha256"] in refs
