"""Placeholders preparing future realization analysis (no calculations)."""

from __future__ import annotations

from typing import Any

from localgovbench_measurement_validation.affordance.coding.template import load_corpus_lock
from localgovbench_measurement_validation.affordance.experiments.paths import (
    REALIZATION_TEMPLATE_COLUMNS,
)
from localgovbench_measurement_validation.affordance.coding.paths import SPECIFICATION_VERSION


def build_realization_input_template(
    matrix_rows: list[dict[str, Any]],
    *,
    experiment_id: str,
) -> list[dict[str, str]]:
    """Create empty realization template rows from the affordance matrix.

    realization_status remains blank — Phase 3 does not calculate realization.
    """
    lock = load_corpus_lock()
    rows: list[dict[str, str]] = []
    for row in matrix_rows:
        rows.append(
            {
                "schema_object_id": str(row.get("schema_object_id") or ""),
                "source_name": str(row.get("source_name") or ""),
                "disclosure_function_id": str(row.get("disclosure_function_id") or ""),
                "support_level": str(row.get("support_level") or ""),
                "applicability_label": str(row.get("applicability_label") or ""),
                "realization_status": "",  # placeholder only
                "realization_notes": "",
                "corpus_lock_sha256": str(
                    row.get("corpus_lock_sha256") or lock["sha256"]
                ),
                "specification_version": str(
                    row.get("specification_version") or SPECIFICATION_VERSION
                ),
                "experiment_id": experiment_id,
            }
        )
    return [{c: r.get(c, "") for c in REALIZATION_TEMPLATE_COLUMNS} for r in rows]


def build_realization_manifest(
    *,
    experiment_id: str,
    matrix_path: str,
    template_path: str,
) -> dict[str, Any]:
    """Manifest declaring that realization calculation is deferred."""
    return {
        "experiment_id": experiment_id,
        "status": "placeholder_only",
        "realization_calculated": False,
        "gap_calculated": False,
        "irr_calculated": False,
        "affordance_matrix_path": matrix_path,
        "realization_input_template_path": template_path,
        "notes": (
            "Phase 3 prepares realization inputs only. "
            "Do not interpret blank realization_status as study results."
        ),
    }
