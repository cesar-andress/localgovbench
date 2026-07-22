"""Import and validate completed schema-coding files (CSV / JSON / Parquet)."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    SPECIFICATION_VERSION,
)
from localgovbench_measurement_validation.affordance.coding.template import (
    expected_unit_ids,
    load_corpus_lock,
    load_functions,
)
from localgovbench_measurement_validation.affordance.coding.validate import (
    validate_coding_csv,
)
from localgovbench_measurement_validation.affordance.paths import OBJECT_LAYER_BY_SOURCE

SUPPORTED_IMPORT_SUFFIXES = {".csv", ".json", ".parquet"}


class CodingImportError(ValueError):
    """Raised when a coding import fails validation."""


def _unit_id(row: dict[str, Any]) -> str:
    if row.get("coding_unit_id"):
        return str(row["coding_unit_id"])
    source = row.get("source_name") or row.get("source") or ""
    fid = row.get("disclosure_function_id") or ""
    return f"{source}__{fid}"


def load_coding_records(path: Path) -> list[dict[str, Any]]:
    """Load coding records from CSV, JSON, or Parquet."""
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMPORT_SUFFIXES:
        raise CodingImportError(
            f"Unsupported import format {suffix}; expected one of "
            f"{sorted(SUPPORTED_IMPORT_SUFFIXES)}"
        )
    if not path.is_file():
        raise CodingImportError(f"Import file not found: {path}")

    if suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]

    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "records" in data:
            data = data["records"]
        if not isinstance(data, list):
            raise CodingImportError("JSON coding import must be a list or {records: [...]}")
        return [dict(row) for row in data]

    # parquet
    try:
        import pandas as pd  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise CodingImportError(
            "Parquet import requires pandas (and a parquet engine); not available"
        ) from exc
    frame = pd.read_parquet(path)
    return frame.where(frame.notna(), None).to_dict(orient="records")


def write_temp_csv(rows: list[dict[str, Any]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    # Union of keys, sorted for determinism except prefer known template order
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for k in row:
            if k not in seen:
                keys.append(k)
                seen.add(k)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in keys})
    return path


def validate_imported_coding(
    path: Path,
    *,
    require_complete: bool = True,
    expected_units: set[str] | None = None,
) -> list[str]:
    """Validate an imported coding file; return error messages (empty = ok)."""
    errors: list[str] = []
    try:
        rows = load_coding_records(path)
    except CodingImportError as exc:
        return [str(exc)]

    if not rows:
        return ["Coding import is empty"]

    # Reuse Phase 2 CSV validator by materializing CSV when needed.
    if path.suffix.lower() == ".csv":
        csv_errors = validate_coding_csv(path)
    else:
        tmp = path.with_suffix(".import_validate.csv")
        write_temp_csv(rows, tmp)
        try:
            csv_errors = validate_coding_csv(tmp)
        finally:
            if tmp.exists():
                tmp.unlink()

    # Coverage is enforced below via expected_units / require_complete.
    # Drop Phase-2 full-template missing-unit messages when we manage coverage here.
    if expected_units is not None or not require_complete:
        csv_errors = [
            e for e in csv_errors if not e.startswith("missing coding unit:")
        ]
    errors.extend(csv_errors)
    lock = load_corpus_lock()
    function_ids = {f["id"] for f in load_functions()}
    expected = expected_units if expected_units is not None else set(expected_unit_ids())

    seen_units: dict[str, int] = {}
    present: set[str] = set()
    for i, row in enumerate(rows, start=1):
        unit = _unit_id(row)
        present.add(unit)
        if unit in seen_units:
            errors.append(f"record {i}: duplicate coding unit {unit}")
        seen_units[unit] = i

        source = str(row.get("source_name") or row.get("source") or "")
        fid = str(row.get("disclosure_function_id") or "")
        if source and source not in OBJECT_LAYER_BY_SOURCE:
            errors.append(f"record {i}: unknown schema object / source {source}")
        if fid and fid not in function_ids:
            errors.append(f"record {i}: unknown function ID {fid}")

        spec_v = str(row.get("specification_version") or "")
        if spec_v and spec_v != SPECIFICATION_VERSION:
            errors.append(f"record {i}: invalid specification version {spec_v}")

        coding_v = str(row.get("coding_layer_version") or row.get("coding_version") or "")
        if coding_v and coding_v != CODING_LAYER_VERSION:
            errors.append(f"record {i}: invalid coding version {coding_v}")

        lock_ref = str(row.get("corpus_lock_reference") or "")
        if lock_ref and lock_ref != lock["sha256"]:
            errors.append(f"record {i}: invalid corpus lock reference")

    if require_complete:
        for unit in sorted(expected - present):
            errors.append(f"missing unit: {unit}")
        for unit in sorted(present - expected):
            # Extra units beyond full template are rejected for full imports.
            errors.append(f"unexpected unit: {unit}")

    # Deduplicate while preserving order
    deduped: list[str] = []
    seen_err: set[str] = set()
    for err in errors:
        if err not in seen_err:
            deduped.append(err)
            seen_err.add(err)
    return deduped


def import_coding_file(
    path: Path,
    *,
    require_complete: bool = True,
    expected_units: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Load and validate a coding file; raise CodingImportError on failure."""
    errors = validate_imported_coding(
        path, require_complete=require_complete, expected_units=expected_units
    )
    if errors:
        raise CodingImportError(
            "Coding import rejected:\n" + "\n".join(f"- {e}" for e in errors)
        )
    return load_coding_records(path)
