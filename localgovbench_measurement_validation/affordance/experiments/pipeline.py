"""Orchestrate the Phase 3 schema-affordance experiment pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.experiments.adjudication_merge import (
    archive_inputs,
    merge_double_coding,
)
from localgovbench_measurement_validation.affordance.experiments.export import export_dataset
from localgovbench_measurement_validation.affordance.experiments.import_coding import (
    CodingImportError,
    import_coding_file,
)
from localgovbench_measurement_validation.affordance.experiments.matrix import (
    build_schema_affordance_matrix,
)
from localgovbench_measurement_validation.affordance.experiments.paths import (
    EXPERIMENT_INPUTS,
    EXPERIMENT_MANIFESTS,
    EXPERIMENT_OUTPUTS,
    EXPERIMENT_PROVENANCE,
    EXPERIMENT_VALIDATION,
    MATRIX_COLUMNS,
    REALIZATION_TEMPLATE_COLUMNS,
)
from localgovbench_measurement_validation.affordance.experiments.provenance import (
    build_experiment_manifest,
    build_provenance,
    write_json,
)
from localgovbench_measurement_validation.affordance.experiments.realization_placeholders import (
    build_realization_input_template,
    build_realization_manifest,
)
from localgovbench_measurement_validation.affordance.experiments.validate_experiment import (
    validate_manifest,
    validate_matrix,
    validate_merge_log,
    validate_provenance,
    write_validation_report,
)


def run_affordance_experiment(
    *,
    experiment_id: str,
    coder_a: Path,
    coder_b: Path,
    adjudication: Path | None = None,
    operator: str = "local",
    require_complete: bool = True,
    expected_units: set[str] | None = None,
    output_root: Path | None = None,
) -> dict[str, Any]:
    """Run import → merge → matrix → exports → provenance → validation.

    Does not calculate realization, gaps, or IRR.
    """
    outputs = output_root or EXPERIMENT_OUTPUTS
    manifests = (output_root / "manifests") if output_root else EXPERIMENT_MANIFESTS
    provenance_dir = (
        (output_root / "provenance") if output_root else EXPERIMENT_PROVENANCE
    )
    validation_dir = (
        (output_root / "validation") if output_root else EXPERIMENT_VALIDATION
    )
    inputs_archive = (
        (output_root / "inputs_archive" / experiment_id)
        if output_root
        else (EXPERIMENT_INPUTS / "archive" / experiment_id)
    )

    for d in (outputs, manifests, provenance_dir, validation_dir, inputs_archive):
        d.mkdir(parents=True, exist_ok=True)

    archived = archive_inputs(
        dest_dir=inputs_archive,
        coder_a=coder_a,
        coder_b=coder_b,
        adjudication=adjudication,
    )

    finalized, merge_log = merge_double_coding(
        coder_a,
        coder_b,
        adjudication,
        require_complete=require_complete,
        expected_units=expected_units,
    )

    matrix = build_schema_affordance_matrix(finalized, experiment_id=experiment_id)
    matrix_errors = validate_matrix(matrix)
    matrix_units = {f"{r['source_name']}__{r['disclosure_function_id']}" for r in matrix}
    matrix_errors.extend(validate_merge_log(merge_log, matrix_units))

    stem = outputs / f"{experiment_id}_schema_affordance_matrix"
    written = export_dataset(matrix, stem, columns=MATRIX_COLUMNS)

    finalized_stem = outputs / f"{experiment_id}_finalized_coding"
    finalized_written = export_dataset(finalized, finalized_stem)

    realization_rows = build_realization_input_template(
        matrix, experiment_id=experiment_id
    )
    realization_stem = outputs / f"{experiment_id}_realization_input_template"
    realization_written = export_dataset(
        realization_rows, realization_stem, columns=REALIZATION_TEMPLATE_COLUMNS
    )

    realization_manifest = build_realization_manifest(
        experiment_id=experiment_id,
        matrix_path=written["csv"],
        template_path=realization_written["csv"],
    )
    realization_manifest_path = manifests / f"{experiment_id}_realization_manifest.json"
    write_json(realization_manifest_path, realization_manifest)

    merge_log_path = provenance_dir / f"{experiment_id}_merge_log.json"
    write_json(merge_log_path, merge_log)

    experiment_manifest = build_experiment_manifest(
        experiment_id=experiment_id,
        operator=operator,
        notes="Phase 3 schema-affordance pipeline; no realization/gap/IRR results.",
    )
    manifest_path = manifests / f"{experiment_id}_experiment_manifest.json"
    write_json(manifest_path, experiment_manifest)
    manifest_errors = validate_manifest(experiment_manifest)

    output_paths = (
        list(written.values())
        + list(finalized_written.values())
        + list(realization_written.values())
        + [str(realization_manifest_path), str(manifest_path), str(merge_log_path)]
        + [str(p) for p in archived]
    )
    provenance = build_provenance(
        experiment_id=experiment_id,
        generator_script="scripts/run_affordance_experiment_pipeline.py",
        input_paths=[str(coder_a), str(coder_b)]
        + ([str(adjudication)] if adjudication else []),
        output_paths=output_paths,
        operator=operator,
        extra={"formats_written": sorted(set(written) | set(finalized_written))},
    )
    provenance_path = provenance_dir / f"{experiment_id}_provenance.json"
    write_json(provenance_path, provenance)
    provenance_errors = validate_provenance(provenance)

    all_errors = matrix_errors + manifest_errors + provenance_errors
    report_path = validation_dir / f"{experiment_id}_validation_report.json"
    write_validation_report(report_path, all_errors, ok=not all_errors)

    if all_errors:
        raise CodingImportError(
            "Experiment validation failed:\n" + "\n".join(f"- {e}" for e in all_errors)
        )

    return {
        "experiment_id": experiment_id,
        "matrix_paths": written,
        "finalized_paths": finalized_written,
        "realization_template_paths": realization_written,
        "manifest_path": str(manifest_path),
        "realization_manifest_path": str(realization_manifest_path),
        "provenance_path": str(provenance_path),
        "merge_log_path": str(merge_log_path),
        "validation_report_path": str(report_path),
        "matrix_row_count": len(matrix),
    }


def run_single_coder_matrix(
    *,
    experiment_id: str,
    coding_path: Path,
    operator: str = "local",
    require_complete: bool = True,
    expected_units: set[str] | None = None,
    output_root: Path | None = None,
) -> dict[str, Any]:
    """Build matrix from a single already-adjudicated / single-coder sheet."""
    rows = import_coding_file(
        coding_path,
        require_complete=require_complete,
        expected_units=expected_units,
    )
    for row in rows:
        row.setdefault("adjudicated_from", "single_coder")
        if not row.get("adjudication_status"):
            row["adjudication_status"] = "not_required"

    outputs = output_root or EXPERIMENT_OUTPUTS
    manifests = (output_root / "manifests") if output_root else EXPERIMENT_MANIFESTS
    provenance_dir = (
        (output_root / "provenance") if output_root else EXPERIMENT_PROVENANCE
    )
    validation_dir = (
        (output_root / "validation") if output_root else EXPERIMENT_VALIDATION
    )
    for d in (outputs, manifests, provenance_dir, validation_dir):
        d.mkdir(parents=True, exist_ok=True)

    matrix = build_schema_affordance_matrix(rows, experiment_id=experiment_id)
    errors = validate_matrix(matrix)
    written = export_dataset(
        matrix, outputs / f"{experiment_id}_schema_affordance_matrix", columns=MATRIX_COLUMNS
    )
    manifest = build_experiment_manifest(experiment_id=experiment_id, operator=operator)
    manifest_path = manifests / f"{experiment_id}_experiment_manifest.json"
    write_json(manifest_path, manifest)
    errors.extend(validate_manifest(manifest))
    provenance = build_provenance(
        experiment_id=experiment_id,
        generator_script="scripts/run_affordance_experiment_pipeline.py",
        input_paths=[str(coding_path)],
        output_paths=list(written.values()) + [str(manifest_path)],
        operator=operator,
    )
    provenance_path = provenance_dir / f"{experiment_id}_provenance.json"
    write_json(provenance_path, provenance)
    errors.extend(validate_provenance(provenance))
    report_path = validation_dir / f"{experiment_id}_validation_report.json"
    write_validation_report(report_path, errors, ok=not errors)
    if errors:
        raise CodingImportError(
            "Experiment validation failed:\n" + "\n".join(f"- {e}" for e in errors)
        )
    return {
        "experiment_id": experiment_id,
        "matrix_paths": written,
        "manifest_path": str(manifest_path),
        "provenance_path": str(provenance_path),
        "validation_report_path": str(report_path),
        "matrix_row_count": len(matrix),
    }
