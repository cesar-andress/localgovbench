"""Tests for construct traceability package."""

from __future__ import annotations

from pathlib import Path

import pytest

from localgovbench.traceability import (
    CSV_COLUMNS,
    build_traceability_rows,
    expected_indicator_ids,
    load_mapping_csv,
    sync_traceability_artifacts,
    validate_traceability,
    write_mapping_csv,
)


def test_build_traceability_covers_all_indicators() -> None:
    rows = build_traceability_rows()
    mapped = {r.indicator_id for r in rows}
    expected = expected_indicator_ids()
    assert mapped == expected
    assert len(rows) >= len(expected)


def test_validate_perfect_coverage(tmp_path: Path) -> None:
    csv_path = tmp_path / "mapping.csv"
    write_mapping_csv(csv_path)
    loaded = load_mapping_csv(csv_path)
    result = validate_traceability(loaded)
    assert result.ok
    assert result.missing_indicator_ids == ()
    assert result.orphan_indicator_ids == ()


def test_partial_agreement_detects_missing_indicator(tmp_path: Path) -> None:
    rows = [r.as_dict() for r in build_traceability_rows()]
    rows = [r for r in rows if not r["indicator_id"].startswith("operational_human")]
    result = validate_traceability(rows)
    assert not result.ok
    assert "operational_human_oversight" in result.missing_indicator_ids


def test_orphan_indicator_rejected(tmp_path: Path) -> None:
    rows = [r.as_dict() for r in build_traceability_rows()]
    rows.append(
        {
            "indicator_id": "fake_dimension_fake_criterion",
            "dimension": "Legal and Regulatory Compliance",
            "governance_requirement": "Test",
            "source_framework": "ART",
            "source_concept": "Accountability",
            "rationale": "Orphan test row.",
        }
    )
    result = validate_traceability(rows)
    assert not result.ok
    assert "fake_dimension_fake_criterion" in result.orphan_indicator_ids


def test_all_dimensions_represented() -> None:
    rows = [r.as_dict() for r in build_traceability_rows()]
    result = validate_traceability(rows)
    assert result.missing_dimension_ids == ()


def test_csv_columns_schema(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    write_mapping_csv(path)
    loaded = load_mapping_csv(path)
    assert loaded
    assert set(loaded[0].keys()) == set(CSV_COLUMNS)


def test_sync_artifacts_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    csv_path = root / "data" / "traceability" / "indicator_mapping.csv"
    report_path = root / "reports" / "traceability_report.md"
    result = sync_traceability_artifacts(csv_path=csv_path, report_path=report_path)
    assert result.ok
    assert csv_path.exists()
    assert report_path.exists()
