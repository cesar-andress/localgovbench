"""Deterministic generation of Disclosure Functions v1 pilot coder packets.

Does NOT assign human coding judgments (support, encoding, linkage, confidence, etc.).
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.coding.paths import (
    ADJUDICATION_PROTOCOL_MD,
    CODEBOOK_MD,
    CODER_INSTRUCTIONS_MD,
    CODING_LABELS_YAML,
    CODING_LAYER_VERSION,
    CODING_RECORD_SCHEMA,
    DOUBLE_CODING_PROTOCOL_MD,
    IRR_PLAN_MD,
    JUDGMENT_COLUMNS,
    PILOT_MANIFEST_CSV,
    SCHEMA_CODING_TEMPLATE_CSV,
    SPECIFICATION_VERSION,
    WORKED_EXAMPLES_MD,
)
from localgovbench_measurement_validation.affordance.paths import (
    CORPUS_LOCK_JSON,
    DISCLOSURE_FUNCTIONS_YAML,
    REPO_ROOT,
)

PILOT_ROUND_ID = "pilot_round_01"
PILOT_ROUND_ROOT = (
    Path(__file__).resolve().parent / "pilot_round_01"
)

# Human judgment columns that must remain empty in blank packets.
# coder_id is left empty; assignment uses assigned_coder_slot instead.
BLANK_JUDGMENT_COLUMNS = list(JUDGMENT_COLUMNS)

ANTI_OVERCREDIT_REMINDER = (
    "Apply codebook anti-over-credit rules. "
    "Do not treat generic narrative as dedicated support except where the codebook explicitly allows. "
    "Do not treat generic URLs as function-specific documentary linkage. "
    "Do not use record-population rates. "
    "Do not insert adjudicated values."
)

CONTEXT_COLUMNS = [
    "coding_record_id",
    "coding_unit_id",
    "coding_round_id",
    "assigned_coder_slot",
    "specification_version",
    "coding_layer_version",
    "corpus_lock_reference",
    "schema_inventory_reference",
    "schema_inventory_version",
    "source_name",
    "schema_object_id",
    "schema_object_type",
    "disclosure_function_id",
    "function_display_name",
    "tier",
    "scoring_role",
    "frozen_default_applicability",
    "pilot_selection_rationale",
    "candidate_observed_fields",
    "mapping_PRIMARY",
    "mapping_SECONDARY",
    "mapping_INDIRECT",
    "mapping_REJECTED",
    "known_field_mapping_labels",
    "source_specific_caveats",
    "anti_overcredit_reminder",
]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "UNKNOWN"


def _parse_mappings(label_blob: str) -> dict[str, str]:
    buckets = {
        "PRIMARY": [],
        "SECONDARY": [],
        "INDIRECT": [],
        "REJECTED": [],
    }
    text = (label_blob or "").strip()
    if not text:
        return {k: "" for k in buckets}
    for part in text.split("|"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        field, label = part.rsplit("=", 1)
        field = field.strip()
        label = label.strip().upper()
        if label in buckets:
            buckets[label].append(field)
    return {k: "|".join(v) for k, v in buckets.items()}


def load_pilot_units() -> list[dict[str, str]]:
    with PILOT_MANIFEST_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_full_template_index() -> dict[str, dict[str, str]]:
    with SCHEMA_CODING_TEMPLATE_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {r["coding_unit_id"]: r for r in rows}


def build_coder_packet_rows(coder_slot: str) -> list[dict[str, str]]:
    if coder_slot not in {"coder_A", "coder_B"}:
        raise ValueError(f"Unknown coder slot: {coder_slot}")
    pilot = load_pilot_units()
    template = load_full_template_index()
    rows: list[dict[str, str]] = []
    for p in pilot:
        unit = p["pilot_unit_id"]
        base = template[unit]
        maps = _parse_mappings(base.get("known_field_mapping_labels", ""))
        row: dict[str, str] = {
            "coding_record_id": f"{PILOT_ROUND_ID}__{unit}__{coder_slot}",
            "coding_unit_id": unit,
            "coding_round_id": PILOT_ROUND_ID,
            "assigned_coder_slot": coder_slot,
            "specification_version": base["specification_version"],
            "coding_layer_version": base.get("coding_layer_version", CODING_LAYER_VERSION),
            "corpus_lock_reference": base["corpus_lock_reference"],
            "schema_inventory_reference": "schema_inventory_v1.csv",
            "schema_inventory_version": base.get("schema_inventory_version", "1.0.0"),
            "source_name": base["source_name"],
            "schema_object_id": base["schema_object_id"],
            "schema_object_type": base["schema_object_type"],
            "disclosure_function_id": base["disclosure_function_id"],
            "function_display_name": base["function_display_name"],
            "tier": base["tier"],
            "scoring_role": base["scoring_role"],
            "frozen_default_applicability": base.get("default_applicability", ""),
            "pilot_selection_rationale": p.get("selection_rationale", ""),
            "candidate_observed_fields": base.get("candidate_observed_fields", ""),
            "mapping_PRIMARY": maps["PRIMARY"],
            "mapping_SECONDARY": maps["SECONDARY"],
            "mapping_INDIRECT": maps["INDIRECT"],
            "mapping_REJECTED": maps["REJECTED"],
            "known_field_mapping_labels": base.get("known_field_mapping_labels", ""),
            "source_specific_caveats": base.get("source_specific_caveats", ""),
            "anti_overcredit_reminder": ANTI_OVERCREDIT_REMINDER,
        }
        for col in BLANK_JUDGMENT_COLUMNS:
            row[col] = ""
        rows.append(row)
    # Deterministic order by coding_unit_id
    rows.sort(key=lambda r: r["coding_unit_id"])
    return rows


def packet_fieldnames() -> list[str]:
    return CONTEXT_COLUMNS + BLANK_JUDGMENT_COLUMNS


def write_coder_packet(coder_slot: str, path: Path) -> Path:
    rows = build_coder_packet_rows(coder_slot)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = packet_fieldnames()
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def verify_pilot_inputs() -> list[str]:
    """Return contradictions; empty list means OK."""
    errors: list[str] = []
    pilot = load_pilot_units()
    template = load_full_template_index()
    ids = [p["pilot_unit_id"] for p in pilot]
    if len(ids) != 33:
        errors.append(f"expected 33 pilot units, found {len(ids)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate pilot units")
    missing = sorted(set(ids) - set(template))
    if missing:
        errors.append(f"pilot units missing from full template: {missing}")
    sources = {p["source_name"] for p in pilot}
    if sources != {
        "US-OMB-2025",
        "CA-GC-AI-REG",
        "NL-ALGO-REG",
        "EU-PSTW",
        "UK-ATRS",
    }:
        errors.append(f"unexpected source coverage: {sorted(sources)}")
    funcs = {p["disclosure_function_id"] for p in pilot}
    if len(funcs) != 11:
        errors.append(f"expected 11 functions, found {len(funcs)}: {sorted(funcs)}")
    for p in pilot:
        if not (p.get("selection_rationale") or "").strip():
            errors.append(f"missing selection_rationale for {p['pilot_unit_id']}")
        base = template.get(p["pilot_unit_id"])
        if not base:
            continue
        for col in BLANK_JUDGMENT_COLUMNS:
            if (base.get(col) or "").strip():
                errors.append(
                    f"frozen template has non-empty judgment field {col} on {p['pilot_unit_id']}"
                )
        if base.get("specification_version") != SPECIFICATION_VERSION:
            errors.append(f"spec version mismatch on {p['pilot_unit_id']}")
        lock = json.loads(CORPUS_LOCK_JSON.read_text(encoding="utf-8"))
        if base.get("corpus_lock_reference") != lock["sha256"]:
            errors.append(f"corpus lock mismatch on {p['pilot_unit_id']}")
    return errors


def build_reference_manifest() -> dict[str, Any]:
    refs = [
        ("codebook", CODEBOOK_MD),
        ("coder_instructions", CODER_INSTRUCTIONS_MD),
        ("worked_examples", WORKED_EXAMPLES_MD),
        ("coding_record_schema", CODING_RECORD_SCHEMA),
        ("coding_labels", CODING_LABELS_YAML),
        ("double_coding_protocol", DOUBLE_CODING_PROTOCOL_MD),
        ("adjudication_protocol", ADJUDICATION_PROTOCOL_MD),
        ("irr_analysis_plan", IRR_PLAN_MD),
        ("pilot_manifest", PILOT_MANIFEST_CSV),
        ("schema_coding_template", SCHEMA_CODING_TEMPLATE_CSV),
        ("corpus_lock", CORPUS_LOCK_JSON),
        ("disclosure_functions", DISCLOSURE_FUNCTIONS_YAML),
    ]
    files = []
    for name, path in refs:
        rel = str(path.relative_to(REPO_ROOT))
        files.append(
            {
                "name": name,
                "path": rel,
                "sha256": _sha256_file(path),
            }
        )
    return {
        "pilot_round_id": PILOT_ROUND_ID,
        "specification_version": SPECIFICATION_VERSION,
        "coding_version": CODING_LAYER_VERSION,
        "corpus_lock_sha256": json.loads(CORPUS_LOCK_JSON.read_text(encoding="utf-8"))[
            "sha256"
        ],
        "git_commit": _git_commit(),
        "generation_timestamp_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "generator_command": (
            "python3.12 -m localgovbench_measurement_validation.affordance.coding."
            "pilot_launch generate"
        ),
        "files": files,
    }


def write_sha256sums(paths: list[Path], output: Path) -> Path:
    lines = []
    for path in sorted(paths, key=lambda p: str(p)):
        digest = _sha256_file(path)
        # Use path relative to pilot_round_01 when possible
        try:
            rel = path.relative_to(PILOT_ROUND_ROOT)
        except ValueError:
            rel = path
        lines.append(f"{digest}  {rel.as_posix()}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def validate_blank_packet(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 33:
        errors.append(f"{path.name}: expected 33 rows, found {len(rows)}")
    ids = [r.get("coding_unit_id", "") for r in rows]
    if len(set(ids)) != len(ids):
        errors.append(f"{path.name}: duplicate coding_unit_id")
    expected = {p["pilot_unit_id"] for p in load_pilot_units()}
    if set(ids) != expected:
        errors.append(f"{path.name}: unit universe mismatch")
    for i, row in enumerate(rows, start=2):
        for col in BLANK_JUDGMENT_COLUMNS:
            if (row.get(col) or "").strip():
                errors.append(f"{path.name}:{i}: judgment field not empty: {col}")
        if not (row.get("frozen_default_applicability") or "").strip():
            errors.append(f"{path.name}:{i}: missing frozen_default_applicability")
        if not (row.get("pilot_selection_rationale") or "").strip():
            errors.append(f"{path.name}:{i}: missing pilot_selection_rationale")
        if not (row.get("assigned_coder_slot") or "").strip():
            errors.append(f"{path.name}:{i}: missing assigned_coder_slot")
        if (row.get("adjudicated_value") or "").strip():
            errors.append(f"{path.name}:{i}: adjudicated_value must be empty")
    return errors


def validate_completed_packet(path: Path, blank_packet: Path) -> list[str]:
    """Post-coding validation for one coder; does not compare to the other coder."""
    from localgovbench_measurement_validation.affordance.experiments.import_coding import (
        validate_imported_coding,
    )

    errors: list[str] = []
    with blank_packet.open(encoding="utf-8", newline="") as handle:
        blank_rows = list(csv.DictReader(handle))
    with path.open(encoding="utf-8", newline="") as handle:
        done_rows = list(csv.DictReader(handle))

    blank_by = {r["coding_unit_id"]: r for r in blank_rows}
    done_by = {r["coding_unit_id"]: r for r in done_rows}
    if set(blank_by) != set(done_by):
        errors.append("completed packet unit universe differs from blank packet")
    if len(done_rows) != 33:
        errors.append(f"expected 33 completed rows, found {len(done_rows)}")

    context_immutable = [
        "coding_record_id",
        "coding_unit_id",
        "coding_round_id",
        "assigned_coder_slot",
        "specification_version",
        "coding_layer_version",
        "corpus_lock_reference",
        "schema_inventory_reference",
        "source_name",
        "schema_object_id",
        "schema_object_type",
        "disclosure_function_id",
        "function_display_name",
        "tier",
        "scoring_role",
        "frozen_default_applicability",
        "pilot_selection_rationale",
        "candidate_observed_fields",
        "mapping_PRIMARY",
        "mapping_SECONDARY",
        "mapping_INDIRECT",
        "mapping_REJECTED",
        "known_field_mapping_labels",
        "source_specific_caveats",
        "anti_overcredit_reminder",
    ]
    for unit, blank in blank_by.items():
        done = done_by.get(unit)
        if not done:
            continue
        for col in context_immutable:
            if (blank.get(col) or "") != (done.get(col) or ""):
                errors.append(f"{unit}: frozen context changed: {col}")
        if (done.get("adjudicated_value") or "").strip():
            errors.append(f"{unit}: adjudicated_value must remain empty for coder sheet")
        if (done.get("adjudicator_id") or "").strip():
            errors.append(f"{unit}: adjudicator_id must remain empty for coder sheet")

    expected = set(blank_by)
    # Map completed sheet into importable shape for Phase-2/3 validators
    # Completed sheets may still use blank packet columns; ensure coding fields present.
    import_errors = validate_imported_coding(
        path, require_complete=True, expected_units=expected
    )
    # Filter noise about missing units already checked
    errors.extend(import_errors)
    return errors


def generate_pilot_launch_package(root: Path | None = None) -> dict[str, Path]:
    contradictions = verify_pilot_inputs()
    if contradictions:
        raise RuntimeError(
            "Frozen artefact contradiction:\n" + "\n".join(f"- {e}" for e in contradictions)
        )

    root = root or PILOT_ROUND_ROOT
    dirs = [
        root,
        root / "administration",
        root / "coder_packets",
        root / "checksums",
        root / "validation",
        root / "import_commands",
        root / "completed_inputs",
        root / "locked_reference",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    packet_a = write_coder_packet("coder_A", root / "coder_packets" / "pilot_round_01_coder_A.csv")
    packet_b = write_coder_packet("coder_B", root / "coder_packets" / "pilot_round_01_coder_B.csv")

    ref = build_reference_manifest()
    ref_path = root / "locked_reference" / "pilot_reference_manifest_v1.json"
    ref_path.write_text(
        json.dumps(ref, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    checksum_targets = [
        packet_a,
        packet_b,
        PILOT_MANIFEST_CSV,
        CODEBOOK_MD,
        CODER_INSTRUCTIONS_MD,
        CODING_RECORD_SCHEMA,
        ref_path,
    ]
    sums = write_sha256sums(checksum_targets, root / "checksums" / "SHA256SUMS")

    return {
        "root": root,
        "packet_a": packet_a,
        "packet_b": packet_b,
        "reference_manifest": ref_path,
        "checksums": sums,
    }


if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    if cmd == "generate":
        out = generate_pilot_launch_package()
        print(json.dumps({k: str(v) for k, v in out.items()}, indent=2, sort_keys=True))
    elif cmd == "verify":
        errs = verify_pilot_inputs()
        print("\n".join(errs) if errs else "OK")
        raise SystemExit(1 if errs else 0)
    else:
        raise SystemExit(f"Unknown command: {cmd}")
