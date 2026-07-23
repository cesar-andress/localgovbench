"""Deterministic adjudication merge for double-coded schema units.

Never overwrites original coder files. Keeps full provenance of A/B/adjudicated.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from localgovbench_measurement_validation.affordance.experiments.import_coding import (
    CodingImportError,
    _unit_id,
    import_coding_file,
    load_coding_records,
)

# Substantive adjudicable judgments per double_coding_protocol_v1.md §8
# (support / applicability / encoding / linkage) and adjudication_protocol_v1.md.
# coder_confidence / coder_rationale are coder metadata only (coder_instructions_v1.md)
# and must NOT force adjudication when they are the sole differences.
JUDGMENT_FIELDS = (
    "applicability_label",
    "support_level",
    "encoding_type",
    "documentary_linkage_layer",
    "function_specific_link_type",
    "primary_supporting_fields",
    "indirect_supporting_fields",
)

CODER_METADATA_FIELDS = (
    "coder_confidence",
    "coder_rationale",
)

def _index_by_unit(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        unit = _unit_id(row)
        if unit in out:
            raise CodingImportError(f"Duplicate unit in merge input: {unit}")
        out[unit] = row
    return out


def load_adjudication_sheet(path: Path) -> dict[str, dict[str, str]]:
    """Load adjudication CSV keyed by coding_unit_id."""
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        unit = row.get("coding_unit_id") or ""
        if not unit:
            continue
        if unit in out:
            raise CodingImportError(f"Duplicate adjudication row for {unit}")
        out[unit] = row
    return out


def _parse_adjudicator_decision(decision: str) -> dict[str, str]:
    """Parse adjudicator_decision as key=value;key=value or bare support label."""
    text = (decision or "").strip()
    if not text:
        return {}
    if "=" not in text and ";" not in text:
        # Bare support level decision
        return {"support_level": text}
    parsed: dict[str, str] = {}
    for part in text.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            parsed[k.strip()] = v.strip()
    return parsed


def merge_double_coding(
    coder_a_path: Path,
    coder_b_path: Path,
    adjudication_path: Path | None,
    *,
    require_complete: bool = True,
    expected_units: set[str] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Merge coder A, coder B, and optional adjudication into finalized rows.

    Merge rules (deterministic):
    1. If A and B agree on JUDGMENT_FIELDS → keep A values; adjudication_status=not_required.
       Differences only in CODER_METADATA_FIELDS (confidence/rationale) do not require
       adjudication; original coder B sheet remains archived for independent metadata.
    2. If they disagree and adjudication resolves the unit → apply adjudicator decision;
       adjudication_status=resolved; adjudicated_from=adjudication.
    3. If they disagree and adjudication missing/pending → raise CodingImportError.
    4. Escalated specification contradictions remain flagged; support taken from A unless
       adjudicator_decision provides overrides.
    """
    a_rows = import_coding_file(
        coder_a_path,
        require_complete=require_complete,
        expected_units=expected_units,
    )
    b_rows = import_coding_file(
        coder_b_path,
        require_complete=require_complete,
        expected_units=expected_units,
    )
    a_idx = _index_by_unit(a_rows)
    b_idx = _index_by_unit(b_rows)

    if set(a_idx) != set(b_idx):
        only_a = sorted(set(a_idx) - set(b_idx))
        only_b = sorted(set(b_idx) - set(a_idx))
        raise CodingImportError(
            f"Coder unit sets differ; only_a={only_a[:5]} only_b={only_b[:5]}"
        )

    adj = load_adjudication_sheet(adjudication_path) if adjudication_path else {}
    orphan = sorted(set(adj) - set(a_idx))
    if orphan:
        raise CodingImportError(f"Orphan adjudications for unknown units: {orphan[:10]}")

    finalized: list[dict[str, Any]] = []
    provenance_rows: list[dict[str, Any]] = []

    for unit in sorted(a_idx):
        a = a_idx[unit]
        b = b_idx[unit]
        disagreements = [
            field
            for field in JUDGMENT_FIELDS
            if str(a.get(field) or "") != str(b.get(field) or "")
        ]
        merged = dict(a)
        if not disagreements:
            merged["adjudication_status"] = "not_required"
            merged["adjudicated_value"] = ""
            merged["adjudicator_id"] = ""
            merged["adjudicated_from"] = "agreement"
            source_choice = "coder_a_agreement"
        else:
            if unit not in adj:
                raise CodingImportError(
                    f"Disagreement on {unit} fields={disagreements} without adjudication row"
                )
            sheet = adj[unit]
            status = (sheet.get("resolution_status") or "").strip()
            if status in {"", "pending"}:
                raise CodingImportError(
                    f"Adjudication for {unit} is unresolved (status={status or 'empty'})"
                )
            if status == "escalated_specification_contradiction":
                merged["adjudication_status"] = status
                merged["adjudicated_from"] = "escalation"
                source_choice = "coder_a_escalation_placeholder"
            else:
                decision = _parse_adjudicator_decision(sheet.get("adjudicator_decision", ""))
                for key, value in decision.items():
                    if key in JUDGMENT_FIELDS or key in merged:
                        merged[key] = value
                # Also accept JSON decision blob in adjudicator_decision
                raw = (sheet.get("adjudicator_decision") or "").strip()
                if raw.startswith("{"):
                    try:
                        blob = json.loads(raw)
                        if isinstance(blob, dict):
                            for key, value in blob.items():
                                merged[key] = value
                    except json.JSONDecodeError as exc:
                        raise CodingImportError(
                            f"Invalid JSON adjudicator_decision for {unit}: {exc}"
                        ) from exc
                merged["adjudication_status"] = "resolved"
                merged["adjudicated_value"] = sheet.get("adjudicator_decision", "")
                merged["adjudicator_id"] = sheet.get("adjudicator_id") or merged.get(
                    "adjudicator_id"
                ) or "adjudicator"
                merged["adjudicated_from"] = "adjudication"
                source_choice = "adjudication"

        finalized.append(merged)
        provenance_rows.append(
            {
                "coding_unit_id": unit,
                "disagreement_fields": "|".join(disagreements),
                "merge_source": source_choice,
                "coder_a_id": a.get("coder_id", ""),
                "coder_b_id": b.get("coder_id", ""),
                "adjudication_status": merged.get("adjudication_status", ""),
            }
        )

    merge_log = {
        "coder_a_path": str(coder_a_path),
        "coder_b_path": str(coder_b_path),
        "adjudication_path": str(adjudication_path) if adjudication_path else None,
        "unit_count": len(finalized),
        "disagreement_count": sum(
            1 for r in provenance_rows if r["disagreement_fields"]
        ),
        "adjudicable_fields": list(JUDGMENT_FIELDS),
        "coder_metadata_fields": list(CODER_METADATA_FIELDS),
        "rows": provenance_rows,
    }
    return finalized, merge_log


def archive_inputs(
    *,
    dest_dir: Path,
    coder_a: Path,
    coder_b: Path,
    adjudication: Path | None,
) -> list[Path]:
    """Copy original coding/adjudication inputs without modification."""
    import shutil

    dest_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for src, name in (
        (coder_a, "coder_a" + coder_a.suffix.lower()),
        (coder_b, "coder_b" + coder_b.suffix.lower()),
    ):
        dest = dest_dir / name
        shutil.copy2(src, dest)
        copied.append(dest)
    if adjudication is not None:
        dest = dest_dir / ("adjudication" + adjudication.suffix.lower())
        shutil.copy2(adjudication, dest)
        copied.append(dest)
    return copied
