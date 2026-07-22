"""Tests for Disclosure Functions v1 pilot launch package."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from localgovbench_measurement_validation.affordance.coding.pilot_launch import (
    BLANK_JUDGMENT_COLUMNS,
    PILOT_ROUND_ROOT,
    build_coder_packet_rows,
    generate_pilot_launch_package,
    validate_blank_packet,
    validate_completed_packet,
    verify_pilot_inputs,
    write_coder_packet,
    write_sha256sums,
    _sha256_file,
)


def test_frozen_inputs_have_no_contradictions():
    assert verify_pilot_inputs() == []


def test_packets_exist_with_33_rows():
    a = PILOT_ROUND_ROOT / "coder_packets" / "pilot_round_01_coder_A.csv"
    b = PILOT_ROUND_ROOT / "coder_packets" / "pilot_round_01_coder_B.csv"
    assert a.is_file() and b.is_file()
    assert validate_blank_packet(a) == []
    assert validate_blank_packet(b) == []


def test_identical_unit_universe_across_packets():
    rows_a = build_coder_packet_rows("coder_A")
    rows_b = build_coder_packet_rows("coder_B")
    assert [r["coding_unit_id"] for r in rows_a] == [r["coding_unit_id"] for r in rows_b]
    assert len(rows_a) == 33


def test_judgment_fields_blank():
    for slot in ("coder_A", "coder_B"):
        for row in build_coder_packet_rows(slot):
            for col in BLANK_JUDGMENT_COLUMNS:
                assert (row.get(col) or "") == ""
            assert (row.get("adjudicated_value") or "") == ""


def test_stable_identifiers_and_slots():
    a = build_coder_packet_rows("coder_A")
    assert all(r["assigned_coder_slot"] == "coder_A" for r in a)
    assert all(r["coding_round_id"] == "pilot_round_01" for r in a)
    assert all(r["coding_record_id"].endswith("__coder_A") for r in a)
    assert all(r["coding_record_id"].startswith("pilot_round_01__") for r in a)


def test_no_duplicate_units():
    ids = [r["coding_unit_id"] for r in build_coder_packet_rows("coder_A")]
    assert len(ids) == len(set(ids)) == 33


def test_all_sources_and_functions_represented():
    rows = build_coder_packet_rows("coder_A")
    sources = {r["source_name"] for r in rows}
    funcs = {r["disclosure_function_id"] for r in rows}
    assert sources == {
        "US-OMB-2025",
        "CA-GC-AI-REG",
        "NL-ALGO-REG",
        "EU-PSTW",
        "UK-ATRS",
    }
    assert len(funcs) == 11


def test_deterministic_packet_generation(tmp_path: Path):
    p1 = write_coder_packet("coder_A", tmp_path / "a1.csv")
    p2 = write_coder_packet("coder_A", tmp_path / "a2.csv")
    assert p1.read_bytes() == p2.read_bytes()


def test_frozen_context_immutability_check(tmp_path: Path):
    blank = write_coder_packet("coder_A", tmp_path / "blank.csv")
    with blank.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    # Simulate completed sheet with judgments but unchanged context
    for r in rows:
        r["coder_id"] = "coder_A"
        r["coding_timestamp"] = "2026-07-23T00:00:00+00:00"
        appl = r["frozen_default_applicability"]
        r["applicability_label"] = appl
        r["applicability_rationale"] = "test"
        if appl == "catalogue_inapplicable":
            r["support_level"] = "absent"
            r["encoding_type"] = "not_applicable"
            r["documentary_linkage_layer"] = "not_applicable"
        else:
            r["support_level"] = "absent"
            r["encoding_type"] = "not_applicable"
            r["documentary_linkage_layer"] = "none"
        r["coder_confidence"] = "low"
        r["coder_rationale"] = "test"
        r["anti_overcredit_check"] = "ok"
        r["adjudication_status"] = "pending"
    done = tmp_path / "done.csv"
    with done.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    # Tamper frozen context
    rows[0]["pilot_selection_rationale"] = "TAMPERED"
    tampered = tmp_path / "tampered.csv"
    with tampered.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    errs = validate_completed_packet(tampered, blank)
    assert any("frozen context changed" in e for e in errs)


def test_checksum_generation(tmp_path: Path):
    p = write_coder_packet("coder_B", tmp_path / "b.csv")
    sums = write_sha256sums([p], tmp_path / "SHA256SUMS")
    text = sums.read_text(encoding="utf-8")
    assert _sha256_file(p) in text


def test_pre_coding_validation_script_paths():
    a = PILOT_ROUND_ROOT / "coder_packets" / "pilot_round_01_coder_A.csv"
    b = PILOT_ROUND_ROOT / "coder_packets" / "pilot_round_01_coder_B.csv"
    assert validate_blank_packet(a) == []
    assert validate_blank_packet(b) == []


def test_no_adjudication_values_in_packets():
    for slot in ("coder_A", "coder_B"):
        for row in build_coder_packet_rows(slot):
            assert not (row.get("adjudicated_value") or "").strip()
            assert not (row.get("adjudicator_id") or "").strip()
            assert (row.get("adjudication_status") or "") == ""


def test_regenerate_package_is_stable():
    out = generate_pilot_launch_package()
    a = out["packet_a"].read_bytes()
    generate_pilot_launch_package()
    assert out["packet_a"].read_bytes() == a
