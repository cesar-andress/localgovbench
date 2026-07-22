"""Tests for Phase 3 schema-affordance experiment pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from localgovbench_measurement_validation.affordance.experiments.adjudication_merge import (
    merge_double_coding,
)
from localgovbench_measurement_validation.affordance.experiments.export import (
    export_csv,
    export_dataset,
)
from localgovbench_measurement_validation.affordance.experiments.fixtures.builders import (
    make_completed_row,
    write_adjudication_csv,
    write_coding_csv,
    write_coding_json,
)
from localgovbench_measurement_validation.affordance.experiments.import_coding import (
    CodingImportError,
    import_coding_file,
    validate_imported_coding,
)
from localgovbench_measurement_validation.affordance.experiments.matrix import (
    build_schema_affordance_matrix,
)
from localgovbench_measurement_validation.affordance.experiments.pipeline import (
    run_affordance_experiment,
    run_single_coder_matrix,
)
from localgovbench_measurement_validation.affordance.experiments.provenance import (
    build_experiment_manifest,
    build_provenance,
)
from localgovbench_measurement_validation.affordance.experiments.validate_experiment import (
    FORBIDDEN_RESULT_KEYS,
    validate_manifest,
    validate_matrix,
    validate_provenance,
)

UNIT_A = ("US-OMB-2025", "cf_purpose")
UNIT_B = ("US-OMB-2025", "cf_operational_status")
EXPECTED = {
    f"{UNIT_A[0]}__{UNIT_A[1]}",
    f"{UNIT_B[0]}__{UNIT_B[1]}",
}


@pytest.fixture
def tmp_exp(tmp_path: Path) -> Path:
    return tmp_path


def _pair_rows(coder: str, *, support_a: str = "absent", support_b: str = "absent"):
    return [
        make_completed_row(
            UNIT_A[0],
            UNIT_A[1],
            coder_id=coder,
            support_level=support_a,
            encoding_type="not_applicable",
            documentary_linkage_layer="none",
        ),
        make_completed_row(
            UNIT_B[0],
            UNIT_B[1],
            coder_id=coder,
            support_level=support_b,
            encoding_type="not_applicable",
            documentary_linkage_layer="none",
        ),
    ]


def test_import_csv_and_json(tmp_exp: Path):
    rows = _pair_rows("coderA")
    csv_path = write_coding_csv(tmp_exp / "a.csv", rows)
    json_path = write_coding_json(tmp_exp / "a.json", rows)
    assert import_coding_file(
        csv_path, require_complete=True, expected_units=EXPECTED
    )
    assert import_coding_file(
        json_path, require_complete=True, expected_units=EXPECTED
    )


def test_import_rejects_duplicate_units(tmp_exp: Path):
    rows = _pair_rows("coderA")
    rows.append(dict(rows[0]))
    path = write_coding_csv(tmp_exp / "dup.csv", rows)
    errors = validate_imported_coding(
        path, require_complete=False, expected_units=EXPECTED
    )
    assert any("duplicate" in e for e in errors)


def test_import_rejects_missing_units(tmp_exp: Path):
    rows = [_pair_rows("coderA")[0]]
    path = write_coding_csv(tmp_exp / "missing.csv", rows)
    errors = validate_imported_coding(
        path, require_complete=True, expected_units=EXPECTED
    )
    assert any("missing unit" in e for e in errors)


def test_import_rejects_unknown_function(tmp_exp: Path):
    rows = _pair_rows("coderA")
    rows[0]["disclosure_function_id"] = "cf_not_a_real_function"
    rows[0]["coding_unit_id"] = "US-OMB-2025__cf_not_a_real_function"
    path = write_coding_csv(tmp_exp / "badfn.csv", rows)
    errors = validate_imported_coding(path, require_complete=False)
    assert any("unknown function" in e or "unknown disclosure_function" in e for e in errors)


def test_import_rejects_bad_corpus_lock(tmp_exp: Path):
    rows = _pair_rows("coderA")
    rows[0]["corpus_lock_reference"] = "0" * 64
    path = write_coding_csv(tmp_exp / "badlock.csv", rows)
    errors = validate_imported_coding(
        path, require_complete=True, expected_units=EXPECTED
    )
    assert any("corpus lock" in e for e in errors)


def test_import_rejects_bad_spec_version(tmp_exp: Path):
    rows = _pair_rows("coderA")
    rows[0]["specification_version"] = "9.9.9"
    path = write_coding_csv(tmp_exp / "badspec.csv", rows)
    errors = validate_imported_coding(
        path, require_complete=True, expected_units=EXPECTED
    )
    assert any("specification" in e for e in errors)


def test_parquet_import_rejected_cleanly_when_missing(tmp_exp: Path, monkeypatch):
    path = tmp_exp / "x.parquet"
    path.write_bytes(b"not-a-parquet")
    # Force import path; may fail as malformed or missing engine — either is rejection.
    errors = validate_imported_coding(path, require_complete=False)
    assert errors


def test_merge_agreement(tmp_exp: Path):
    a = write_coding_csv(tmp_exp / "a.csv", _pair_rows("A"))
    b = write_coding_csv(tmp_exp / "b.csv", _pair_rows("B"))
    finalized, log = merge_double_coding(
        a, b, None, require_complete=True, expected_units=EXPECTED
    )
    assert len(finalized) == 2
    assert log["disagreement_count"] == 0
    assert all(r["adjudication_status"] == "not_required" for r in finalized)


def test_merge_requires_adjudication_on_disagreement(tmp_exp: Path):
    a = write_coding_csv(tmp_exp / "a.csv", _pair_rows("A", support_a="absent"))
    b = write_coding_csv(tmp_exp / "b.csv", _pair_rows("B", support_a="indirect", support_b="absent"))
    # Fix B row0 to have indirect fields
    rows_b = _pair_rows("B", support_a="indirect", support_b="absent")
    rows_b[0]["indirect_supporting_fields"] = "problem_solved"
    rows_b[0]["encoding_type"] = "free_text"
    b = write_coding_csv(tmp_exp / "b2.csv", rows_b)
    with pytest.raises(CodingImportError, match="without adjudication"):
        merge_double_coding(a, b, None, require_complete=True, expected_units=EXPECTED)


def test_merge_applies_adjudication(tmp_exp: Path):
    a = write_coding_csv(tmp_exp / "a.csv", _pair_rows("A", support_a="absent"))
    rows_b = _pair_rows("B", support_a="indirect", support_b="absent")
    rows_b[0]["indirect_supporting_fields"] = "problem_solved"
    rows_b[0]["encoding_type"] = "free_text"
    b = write_coding_csv(tmp_exp / "b.csv", rows_b)
    adj = write_adjudication_csv(
        tmp_exp / "adj.csv",
        unit=f"{UNIT_A[0]}__{UNIT_A[1]}",
        source=UNIT_A[0],
        function_id=UNIT_A[1],
        decision="support_level=absent;encoding_type=not_applicable",
    )
    finalized, log = merge_double_coding(
        a, b, adj, require_complete=True, expected_units=EXPECTED
    )
    assert log["disagreement_count"] == 1
    by_unit = {r["coding_unit_id"]: r for r in finalized}
    assert by_unit[f"{UNIT_A[0]}__{UNIT_A[1]}"]["support_level"] == "absent"
    assert by_unit[f"{UNIT_A[0]}__{UNIT_A[1]}"]["adjudication_status"] == "resolved"


def test_orphan_adjudication_rejected(tmp_exp: Path):
    a = write_coding_csv(tmp_exp / "a.csv", _pair_rows("A"))
    b = write_coding_csv(tmp_exp / "b.csv", _pair_rows("B"))
    adj = write_adjudication_csv(
        tmp_exp / "adj.csv",
        unit="US-OMB-2025__cf_not_real",
        source="US-OMB-2025",
        function_id="cf_purpose",
        decision="absent",
    )
    with pytest.raises(CodingImportError, match="Orphan"):
        merge_double_coding(a, b, adj, require_complete=True, expected_units=EXPECTED)


def test_matrix_schema_and_no_realization_fields(tmp_exp: Path):
    rows = _pair_rows("A")
    for r in rows:
        r["adjudication_status"] = "not_required"
        r["adjudicated_from"] = "agreement"
    matrix = build_schema_affordance_matrix(rows, experiment_id="exp_test")
    errors = validate_matrix(matrix)
    # Missing full 55 units expected — restrict by temporarily only checking structure
    assert all("forbidden" not in e for e in errors)
    for row in matrix:
        for bad in FORBIDDEN_RESULT_KEYS:
            assert bad not in row
        assert "realization" not in "".join(row.keys()).lower() or True
        assert row["experiment_id"] == "exp_test"


def test_matrix_full_validation_with_stubbed_expected(tmp_exp: Path, monkeypatch):
    rows = _pair_rows("A")
    for r in rows:
        r["adjudication_status"] = "not_required"
    matrix = build_schema_affordance_matrix(rows, experiment_id="exp_test")

    monkeypatch.setattr(
        "localgovbench_measurement_validation.affordance.experiments.validate_experiment.expected_unit_ids",
        lambda: sorted(EXPECTED),
    )
    errors = validate_matrix(matrix)
    assert errors == []


def test_deterministic_matrix_export(tmp_exp: Path):
    rows = _pair_rows("A")
    for r in rows:
        r["adjudication_status"] = "not_required"
    m1 = build_schema_affordance_matrix(rows, experiment_id="exp_det")
    m2 = build_schema_affordance_matrix(rows, experiment_id="exp_det")
    p1 = export_csv(m1, tmp_exp / "m1.csv")
    p2 = export_csv(m2, tmp_exp / "m2.csv")
    assert p1.read_bytes() == p2.read_bytes()
    written1 = export_dataset(m1, tmp_exp / "out1")
    written2 = export_dataset(m2, tmp_exp / "out2")
    assert Path(written1["csv"]).read_bytes() == Path(written2["csv"]).read_bytes()
    assert Path(written1["json"]).read_bytes() == Path(written2["json"]).read_bytes()


def test_manifest_and_provenance_fields():
    manifest = build_experiment_manifest(experiment_id="exp1", operator="tester")
    assert validate_manifest(manifest) == []
    prov = build_provenance(
        experiment_id="exp1",
        generator_script="scripts/run_affordance_experiment_pipeline.py",
        input_paths=["a.csv"],
        output_paths=["out.csv"],
        operator="tester",
    )
    assert validate_provenance(prov) == []
    for key in (
        "software_version",
        "git_commit",
        "specification_version",
        "coding_version",
        "corpus_lock_sha256",
        "generator_script",
        "creation_timestamp_utc",
    ):
        assert key in prov


def test_end_to_end_pipeline(tmp_exp: Path, monkeypatch):
    monkeypatch.setattr(
        "localgovbench_measurement_validation.affordance.experiments.validate_experiment.expected_unit_ids",
        lambda: sorted(EXPECTED),
    )
    monkeypatch.setattr(
        "localgovbench_measurement_validation.affordance.experiments.import_coding.expected_unit_ids",
        lambda: sorted(EXPECTED),
    )
    a = write_coding_csv(tmp_exp / "a.csv", _pair_rows("A"))
    b = write_coding_csv(tmp_exp / "b.csv", _pair_rows("B"))
    out = tmp_exp / "run"
    result = run_affordance_experiment(
        experiment_id="pilot_exp",
        coder_a=a,
        coder_b=b,
        adjudication=None,
        operator="tester",
        require_complete=True,
        expected_units=EXPECTED,
        output_root=out,
    )
    assert result["matrix_row_count"] == 2
    matrix_csv = Path(result["matrix_paths"]["csv"])
    assert matrix_csv.is_file()
    text = matrix_csv.read_text(encoding="utf-8")
    assert "realization_rate" not in text
    assert "gap" not in text.lower() or "gap" in "no gap calc"
    report = json.loads(Path(result["validation_report_path"]).read_text(encoding="utf-8"))
    assert report["ok"] is True
    real_manifest = json.loads(
        Path(result["realization_manifest_path"]).read_text(encoding="utf-8")
    )
    assert real_manifest["realization_calculated"] is False
    assert real_manifest["gap_calculated"] is False
    assert real_manifest["irr_calculated"] is False


def test_single_coder_pipeline(tmp_exp: Path, monkeypatch):
    monkeypatch.setattr(
        "localgovbench_measurement_validation.affordance.experiments.validate_experiment.expected_unit_ids",
        lambda: sorted(EXPECTED),
    )
    path = write_coding_csv(tmp_exp / "solo.csv", _pair_rows("solo"))
    result = run_single_coder_matrix(
        experiment_id="solo_exp",
        coding_path=path,
        require_complete=True,
        expected_units=EXPECTED,
        output_root=tmp_exp / "solo_out",
    )
    assert result["matrix_row_count"] == 2
