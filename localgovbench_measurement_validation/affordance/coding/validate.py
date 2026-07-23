"""Validate completed schema-coding CSVs and export disagreements."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from localgovbench_measurement_validation.affordance.coding.paths import (
    APPLICABILITY_LABELS,
    CODING_RECORD_SCHEMA,
    CONFIDENCE_LEVELS,
    ENCODING_TYPES,
    GENERIC_NARRATIVE_FIELDS,
    LINKAGE_LAYERS,
    SPECIFICATION_VERSION,
    SUPPORT_LEVELS,
)
from localgovbench_measurement_validation.affordance.coding.template import (
    expected_unit_ids,
    load_corpus_lock,
    load_functions,
)
from localgovbench_measurement_validation.affordance.paths import (
    FIELD_FUNCTION_CANDIDATES_CSV,
    OBJECT_LAYER_BY_SOURCE,
)


def _split_fields(value: str | None) -> list[str]:
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [p.strip() for p in text.replace(";", "|").split("|") if p.strip()]


def _load_rejected_fields() -> dict[tuple[str, str], set[str]]:
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    with FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["mapping_label"] == "REJECTED":
                out[(row["source"], row["function_id"])].add(row["raw_field"])
    return out


def _load_json_schema() -> dict[str, Any]:
    return json.loads(CODING_RECORD_SCHEMA.read_text(encoding="utf-8"))


def validate_coding_csv(path: Path) -> list[str]:
    """Return a list of validation errors for a completed (or partial) coding CSV."""
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return ["Coding CSV is empty"]

    lock = load_corpus_lock()
    function_ids = {f["id"] for f in load_functions()}
    rejected = _load_rejected_fields()
    schema = _load_json_schema()
    enum_functions = set(schema["properties"]["disclosure_function_id"]["enum"])

    seen_units: dict[tuple[str, str, str], int] = {}
    present_units: set[str] = set()

    for i, row in enumerate(rows, start=2):
        source = row.get("source_name") or row.get("source") or ""
        fid = row.get("disclosure_function_id") or ""
        coder = row.get("coder_id") or ""
        unit = row.get("coding_unit_id") or f"{source}__{fid}"
        present_units.add(f"{source}__{fid}")

        key = (source, fid, coder)
        if key in seen_units:
            errors.append(
                f"line {i}: duplicate coding unit for coder ({source}, {fid}, {coder})"
            )
        seen_units[key] = i

        if source not in OBJECT_LAYER_BY_SOURCE:
            errors.append(f"line {i}: unknown source_name {source}")
        if fid not in function_ids or fid not in enum_functions:
            errors.append(f"line {i}: unknown disclosure_function_id {fid}")

        obj_type = row.get("schema_object_type") or ""
        if source in OBJECT_LAYER_BY_SOURCE and obj_type:
            if obj_type != OBJECT_LAYER_BY_SOURCE[source]:
                errors.append(
                    f"line {i}: schema_object_type {obj_type} mismatches frozen object layer"
                )

        spec_v = row.get("specification_version") or ""
        if spec_v and spec_v != SPECIFICATION_VERSION:
            errors.append(f"line {i}: specification_version mismatch ({spec_v})")

        lock_ref = row.get("corpus_lock_reference") or ""
        if lock_ref and lock_ref != lock["sha256"]:
            errors.append(f"line {i}: corpus_lock_reference mismatch")

        # Skip deep judgment checks if row is still a blank template.
        support = (row.get("support_level") or "").strip()
        applicability = (row.get("applicability_label") or "").strip()
        if not support and not applicability and not coder:
            continue

        errors.extend(_validate_judgments(i, row, rejected))

    expected = set(expected_unit_ids())
    missing = sorted(expected - present_units)
    if missing and any((r.get("coder_id") or "").strip() for r in rows):
        # Only require full coverage for completed coder sheets.
        for unit in missing:
            errors.append(f"missing coding unit: {unit}")

    return errors


def _validate_judgments(
    line: int,
    row: dict[str, str],
    rejected: dict[tuple[str, str], set[str]],
) -> list[str]:
    errors: list[str] = []
    source = row.get("source_name") or ""
    fid = row.get("disclosure_function_id") or ""
    support = (row.get("support_level") or "").strip()
    applicability = (row.get("applicability_label") or "").strip()
    encoding = (row.get("encoding_type") or "").strip()
    linkage = (row.get("documentary_linkage_layer") or "").strip()
    confidence = (row.get("coder_confidence") or "").strip()
    primary = _split_fields(row.get("primary_supporting_fields"))
    indirect = _split_fields(row.get("indirect_supporting_fields"))
    unresolved = (row.get("unresolved_issue") or "").strip()
    adjudicated = (row.get("adjudicated_value") or "").strip()
    adj_status = (row.get("adjudication_status") or "").strip()

    if applicability and applicability not in APPLICABILITY_LABELS:
        errors.append(f"line {line}: invalid applicability_label {applicability}")
    if support and support not in SUPPORT_LEVELS:
        errors.append(f"line {line}: invalid support_level {support}")
    if encoding and encoding not in ENCODING_TYPES:
        errors.append(f"line {line}: invalid encoding_type {encoding}")
    if linkage and linkage not in LINKAGE_LAYERS:
        errors.append(f"line {line}: invalid documentary_linkage_layer {linkage}")
    if confidence and confidence not in CONFIDENCE_LEVELS:
        errors.append(f"line {line}: invalid coder_confidence {confidence}")

    # 1. catalogue_inapplicable cannot have dedicated/indirect
    if applicability == "catalogue_inapplicable" and support in {"dedicated", "indirect"}:
        errors.append(
            f"line {line}: catalogue_inapplicable cannot have dedicated/indirect support"
        )

    # 2. unknown requires unresolved issue
    if applicability == "unknown" and not unresolved:
        errors.append(f"line {line}: unknown applicability requires unresolved_issue")

    # 3. absent cannot list primary supporting fields
    if support == "absent" and primary:
        errors.append(f"line {line}: absent support cannot list primary_supporting_fields")

    # 4. dedicated requires at least one supporting field
    if support == "dedicated" and not primary:
        errors.append(f"line {line}: dedicated support requires primary_supporting_fields")

    # 5. indirect requires indirect supporting fields
    if support == "indirect" and not indirect:
        errors.append(
            f"line {line}: indirect support requires indirect_supporting_fields"
        )

    # 6. REJECTED field cannot be primary
    rej = rejected.get((source, fid), set())
    for field in primary:
        if field in rej:
            errors.append(
                f"line {line}: REJECTED field listed as primary supporting evidence: {field}"
            )

    # 7. generic narrative anti-over-credit
    if support == "dedicated":
        generic_primaries = [f for f in primary if f in GENERIC_NARRATIVE_FIELDS]
        if generic_primaries and fid != "cf_purpose":
            errors.append(
                f"line {line}: generic narrative cannot be dedicated for {fid}: {generic_primaries}"
            )
        if source == "UK-ATRS" and "description" in primary and fid == "cf_purpose":
            errors.append(
                f"line {line}: UK description cannot support dedicated purpose"
            )

    # 8. UK organisation_title cannot support dedicated accountable body
    if (
        source == "UK-ATRS"
        and fid == "cf_accountable_body"
        and support == "dedicated"
        and "organisation_title" in primary
    ):
        errors.append(
            f"line {line}: UK organisation_title cannot support dedicated accountable body"
        )

    # 9 already covered for UK description dedicated purpose

    # 10. PSTW outcome flags cannot support risk
    if source == "EU-PSTW" and fid == "om_risk_or_impact":
        for field in primary + indirect:
            if field.startswith("Improved") or field.startswith("Enabled") or field.startswith(
                "Increased"
            ) or field.startswith("Reduced") or field in {
                "Cost-reduction",
                "Better collaboration and better communication",
                "New services or channels",
                "Open government capabilities",
                "Personalized Services",
                "Public (citizen)-centered services",
                "Responsiveness of government operation",
            }:
                errors.append(
                    f"line {line}: PSTW outcome flag cannot support risk designation: {field}"
                )

    # 11. NL proportionality cannot support any active function
    if source == "NL-ALGO-REG" and (
        "proportionality" in primary or "proportionality" in indirect
    ):
        errors.append(
            f"line {line}: NL proportionality cannot support any active function"
        )

    # 12. Identity descriptive_only — informational; scoring_role checked in template
    if fid == "cf_system_identity" and row.get("scoring_role") not in {
        "",
        "descriptive_only",
    }:
        errors.append(f"line {line}: identity must remain descriptive_only")

    # 13. confidence cannot replace support — structural: both fields independent; no auto rule beyond presence
    # (ensured by separate columns; no code path merges them)

    # 14. adjudicated values empty before adjudication
    if adj_status in {"", "pending", "not_required"} and adjudicated:
        errors.append(
            f"line {line}: adjudicated_value must remain empty before adjudication"
        )

    return errors


def export_disagreements(
    coder_a_csv: Path,
    coder_b_csv: Path,
    output_csv: Path,
) -> Path:
    """Export units where coder A and B differ on key labels."""
    def load(path: Path) -> dict[str, dict[str, str]]:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        out = {}
        for row in rows:
            unit = row.get("coding_unit_id") or (
                f"{row.get('source_name')}__{row.get('disclosure_function_id')}"
            )
            out[unit] = row
        return out

    a_rows = load(coder_a_csv)
    b_rows = load(coder_b_csv)
    # Align with adjudicable JUDGMENT_FIELDS (exclude coder_confidence / rationale).
    compare_fields = [
        "applicability_label",
        "support_level",
        "encoding_type",
        "documentary_linkage_layer",
        "function_specific_link_type",
        "primary_supporting_fields",
        "indirect_supporting_fields",
    ]
    out_rows: list[dict[str, str]] = []
    for unit in sorted(set(a_rows) & set(b_rows)):
        a = a_rows[unit]
        b = b_rows[unit]
        diffs = [f for f in compare_fields if (a.get(f) or "") != (b.get(f) or "")]
        if not diffs:
            continue
        out_rows.append(
            {
                "coding_unit_id": unit,
                "source_name": a.get("source_name", ""),
                "disclosure_function_id": a.get("disclosure_function_id", ""),
                "disagreement_fields": "|".join(diffs),
                "coder_a_support_level": a.get("support_level", ""),
                "coder_b_support_level": b.get("support_level", ""),
                "coder_a_applicability_label": a.get("applicability_label", ""),
                "coder_b_applicability_label": b.get("applicability_label", ""),
                "coder_a_encoding_type": a.get("encoding_type", ""),
                "coder_b_encoding_type": b.get("encoding_type", ""),
                "coder_a_documentary_linkage_layer": a.get(
                    "documentary_linkage_layer", ""
                ),
                "coder_b_documentary_linkage_layer": b.get(
                    "documentary_linkage_layer", ""
                ),
                "coder_a_primary_supporting_fields": a.get(
                    "primary_supporting_fields", ""
                ),
                "coder_b_primary_supporting_fields": b.get(
                    "primary_supporting_fields", ""
                ),
                "coder_a_rationale": a.get("coder_rationale", ""),
                "coder_b_rationale": b.get("coder_rationale", ""),
            }
        )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(out_rows[0].keys()) if out_rows else [
        "coding_unit_id",
        "disagreement_fields",
    ]
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)
    return output_csv


def create_adjudication_input(
    disagreement_csv: Path,
    output_csv: Path,
) -> Path:
    """Create an adjudication worksheet from a disagreement export."""
    with disagreement_csv.open(encoding="utf-8", newline="") as handle:
        disagreements = list(csv.DictReader(handle))

    fieldnames = [
        "coding_unit_id",
        "source_name",
        "disclosure_function_id",
        "coder_a_value",
        "coder_b_value",
        "disagreement_type",
        "relevant_fields",
        "relevant_codebook_rule",
        "adjudicator_decision",
        "adjudicator_rationale",
        "codebook_ambiguity_flag",
        "specification_ambiguity_flag",
        "resolution_status",
        "date",
        "version",
    ]
    rows = []
    for d in disagreements:
        rows.append(
            {
                "coding_unit_id": d.get("coding_unit_id", ""),
                "source_name": d.get("source_name", ""),
                "disclosure_function_id": d.get("disclosure_function_id", ""),
                "coder_a_value": (
                    f"support={d.get('coder_a_support_level','')};"
                    f"applicability={d.get('coder_a_applicability_label','')};"
                    f"encoding={d.get('coder_a_encoding_type','')};"
                    f"linkage={d.get('coder_a_documentary_linkage_layer','')}"
                ),
                "coder_b_value": (
                    f"support={d.get('coder_b_support_level','')};"
                    f"applicability={d.get('coder_b_applicability_label','')};"
                    f"encoding={d.get('coder_b_encoding_type','')};"
                    f"linkage={d.get('coder_b_documentary_linkage_layer','')}"
                ),
                "disagreement_type": d.get("disagreement_fields", ""),
                "relevant_fields": (
                    f"A:{d.get('coder_a_primary_supporting_fields','')}|"
                    f"B:{d.get('coder_b_primary_supporting_fields','')}"
                ),
                "relevant_codebook_rule": "",
                "adjudicator_decision": "",
                "adjudicator_rationale": "",
                "codebook_ambiguity_flag": "",
                "specification_ambiguity_flag": "",
                "resolution_status": "pending",
                "date": "",
                "version": "1.0.0",
            }
        )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_csv
