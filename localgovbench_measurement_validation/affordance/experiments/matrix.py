"""Build the canonical schema-affordance matrix (no realization fields)."""

from __future__ import annotations

from typing import Any

from localgovbench_measurement_validation.affordance.coding.paths import (
    CODING_LAYER_VERSION,
    SPECIFICATION_VERSION,
)
from localgovbench_measurement_validation.affordance.coding.template import load_corpus_lock
from localgovbench_measurement_validation.affordance.experiments.import_coding import (
    _unit_id,
)
from localgovbench_measurement_validation.affordance.experiments.paths import (
    EXPERIMENT_PIPELINE_VERSION,
    MATRIX_COLUMNS,
)
from localgovbench_measurement_validation.affordance.paths import (
    OBJECT_LAYER_BY_SOURCE,
    SCHEMA_INVENTORY_VERSION,
)


def build_schema_affordance_matrix(
    finalized_rows: list[dict[str, Any]],
    *,
    experiment_id: str,
) -> list[dict[str, str]]:
    """One row per schema_object × disclosure_function from finalized coding."""
    lock = load_corpus_lock()
    matrix: list[dict[str, str]] = []
    for row in finalized_rows:
        source = str(row.get("source_name") or "")
        obj_id = str(row.get("schema_object_id") or source)
        obj_type = str(
            row.get("schema_object_type") or OBJECT_LAYER_BY_SOURCE.get(source, "")
        )
        matrix.append(
            {
                "schema_object_id": obj_id,
                "source_name": source,
                "schema_object_type": obj_type,
                "disclosure_function_id": str(row.get("disclosure_function_id") or ""),
                "support_level": str(row.get("support_level") or ""),
                "applicability_label": str(row.get("applicability_label") or ""),
                "encoding_type": str(row.get("encoding_type") or ""),
                "documentary_linkage_layer": str(
                    row.get("documentary_linkage_layer") or ""
                ),
                "function_specific_link_type": str(
                    row.get("function_specific_link_type") or ""
                ),
                "coder_confidence": str(row.get("coder_confidence") or ""),
                "adjudication_status": str(row.get("adjudication_status") or ""),
                "adjudicated_from": str(row.get("adjudicated_from") or ""),
                "coding_round_id": str(
                    row.get("coding_round_id") or row.get("coder_id") or ""
                ),
                "specification_version": str(
                    row.get("specification_version") or SPECIFICATION_VERSION
                ),
                "coding_version": str(
                    row.get("coding_layer_version")
                    or row.get("coding_version")
                    or CODING_LAYER_VERSION
                ),
                "corpus_lock_sha256": str(
                    row.get("corpus_lock_reference") or lock["sha256"]
                ),
                "schema_inventory_version": str(
                    row.get("schema_inventory_version") or SCHEMA_INVENTORY_VERSION
                ),
                "experiment_id": experiment_id,
                "pipeline_version": EXPERIMENT_PIPELINE_VERSION,
            }
        )

    matrix.sort(
        key=lambda r: (
            r["source_name"],
            r["disclosure_function_id"],
            r["schema_object_id"],
        )
    )
    # Ensure column order
    return [{col: row.get(col, "") for col in MATRIX_COLUMNS} for row in matrix]


def matrix_unit_ids(matrix: list[dict[str, str]]) -> list[str]:
    return [
        f"{row['source_name']}__{row['disclosure_function_id']}"
        if not row.get("schema_object_id")
        else f"{row['schema_object_id']}__{row['disclosure_function_id']}"
        for row in matrix
    ]
