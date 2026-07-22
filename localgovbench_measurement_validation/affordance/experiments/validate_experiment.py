"""Validation for experiment datasets, manifests, and provenance."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    SPECIFICATION_VERSION,
    SUPPORT_LEVELS,
    APPLICABILITY_LABELS,
)
from localgovbench_measurement_validation.affordance.coding.template import (
    expected_unit_ids,
    load_corpus_lock,
    load_functions,
)
from localgovbench_measurement_validation.affordance.experiments.paths import (
    EXPERIMENT_PIPELINE_VERSION,
    MATRIX_COLUMNS,
)
from localgovbench_measurement_validation.affordance.paths import OBJECT_LAYER_BY_SOURCE

FORBIDDEN_RESULT_KEYS = {
    "realization_rate",
    "realization_score",
    "affordance_realization_gap",
    "gap_score",
    "irr",
    "cohen_kappa",
    "krippendorff_alpha",
    "fleiss_kappa",
}


def validate_matrix(
    rows: list[dict[str, Any]],
    *,
    expected_units: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["matrix is empty"]

    lock = load_corpus_lock()
    functions = {f["id"] for f in load_functions()}
    expected = set(expected_units) if expected_units is not None else set(expected_unit_ids())
    seen: list[str] = []

    for i, row in enumerate(rows, start=1):
        for col in MATRIX_COLUMNS:
            if col not in row:
                errors.append(f"row {i}: missing column {col}")
        for bad in FORBIDDEN_RESULT_KEYS:
            if bad in row:
                errors.append(f"row {i}: forbidden result field present: {bad}")

        source = str(row.get("source_name") or "")
        fid = str(row.get("disclosure_function_id") or "")
        unit = f"{source}__{fid}"
        seen.append(unit)

        if source not in OBJECT_LAYER_BY_SOURCE:
            errors.append(f"row {i}: unknown schema object / source {source}")
        if fid not in functions:
            errors.append(f"row {i}: unknown function {fid}")
        support = str(row.get("support_level") or "")
        if support not in SUPPORT_LEVELS:
            errors.append(f"row {i}: unexpected support_level {support}")
        applicability = str(row.get("applicability_label") or "")
        if applicability and applicability not in APPLICABILITY_LABELS:
            errors.append(f"row {i}: unexpected applicability_label {applicability}")
        if str(row.get("specification_version") or "") != SPECIFICATION_VERSION:
            errors.append(f"row {i}: broken specification_version reference")
        if str(row.get("coding_version") or "") != CODING_LAYER_VERSION:
            errors.append(f"row {i}: broken coding_version reference")
        if str(row.get("corpus_lock_sha256") or "") != lock["sha256"]:
            errors.append(f"row {i}: corpus lock mismatch")
        if str(row.get("pipeline_version") or "") != EXPERIMENT_PIPELINE_VERSION:
            errors.append(f"row {i}: unexpected pipeline_version")

    counts = Counter(seen)
    for unit, n in counts.items():
        if n > 1:
            errors.append(f"duplicate matrix row for unit {unit}")

    missing = sorted(expected - set(seen))
    for unit in missing:
        errors.append(f"missing schema object×function unit: {unit}")

    return errors


def validate_manifest(payload: dict[str, Any]) -> list[str]:
    required = [
        "experiment_id",
        "creation_timestamp_utc",
        "git_commit",
        "specification_version",
        "coding_version",
        "corpus_hash",
        "software_version",
        "operator",
        "pipeline_version",
    ]
    errors = [f"manifest missing {k}" for k in required if k not in payload or payload[k] in (None, "")]
    for bad in FORBIDDEN_RESULT_KEYS:
        if bad in payload:
            errors.append(f"manifest contains forbidden result field: {bad}")
    return errors


def validate_provenance(payload: dict[str, Any]) -> list[str]:
    required = [
        "experiment_id",
        "creation_timestamp_utc",
        "generator_script",
        "software_version",
        "git_commit",
        "specification_version",
        "coding_version",
        "corpus_lock_sha256",
        "pipeline_version",
        "input_paths",
        "output_paths",
    ]
    errors = [f"provenance missing {k}" for k in required if k not in payload]
    if "input_paths" in payload and not isinstance(payload["input_paths"], list):
        errors.append("provenance input_paths must be a list")
    if "output_paths" in payload and not isinstance(payload["output_paths"], list):
        errors.append("provenance output_paths must be a list")
    for bad in FORBIDDEN_RESULT_KEYS:
        if bad in payload:
            errors.append(f"provenance contains forbidden result field: {bad}")
    return errors


def validate_merge_log(merge_log: dict[str, Any], matrix_units: set[str]) -> list[str]:
    errors: list[str] = []
    rows = merge_log.get("rows") or []
    for row in rows:
        unit = row.get("coding_unit_id")
        if unit and unit not in matrix_units and f"{unit}" not in matrix_units:
            # unit format source__function
            errors.append(f"orphan adjudication/merge row for {unit}")
    return errors


def write_validation_report(path: Path, errors: list[str], *, ok: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "ok": ok,
        "error_count": len(errors),
        "errors": errors,
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path
