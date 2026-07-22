"""Pilot coding unit selection for Disclosure Functions v1."""

from __future__ import annotations

import csv
from pathlib import Path

from localgovbench_measurement_validation.affordance.coding.paths import (
    PILOT_MANIFEST_CSV,
)
from localgovbench_measurement_validation.affordance.coding.template import (
    build_coding_template_rows,
)

# Explicit balanced pilot set: all sources × stratified functions.
# Selection rationale is frozen here for auditability.
PILOT_SELECTION: list[tuple[str, str, str]] = [
    # Clear dedicated
    ("NL-ALGO-REG", "cf_purpose", "clear_dedicated: NL goal is dedicated purpose"),
    ("NL-ALGO-REG", "om_human_oversight", "clear_dedicated: NL human_intervention"),
    ("US-OMB-2025", "cf_operational_status", "clear_dedicated: development_stage"),
    ("US-OMB-2025", "om_risk_or_impact", "clear_dedicated: is_high_impact flag"),
    ("CA-GC-AI-REG", "cf_accountable_body", "clear_dedicated: government_organization"),
    # Clear indirect / thin
    ("UK-ATRS", "cf_purpose", "uk_api_slim: description INDIRECT purpose only"),
    ("UK-ATRS", "cf_accountable_body", "uk_api_slim: organisation_title publisher INDIRECT"),
    # Clear absent
    ("UK-ATRS", "cf_operational_status", "clear_absent: no status field on API slim"),
    ("CA-GC-AI-REG", "om_legal_basis", "clear_absent: no lawful_basis field"),
    # Catalogue-inapplicable
    ("EU-PSTW", "cf_data_involvement", "catalogue_inapplicable: PSTW contrast"),
    ("EU-PSTW", "om_risk_or_impact", "catalogue_inapplicable + outcome-flag trap"),
    # Conditional US HI
    ("US-OMB-2025", "om_human_oversight", "conditional: US hi_* high-impact subclass"),
    ("US-OMB-2025", "om_redress_pointer", "conditional: hi_appeal_process only"),
    # Generic description cases
    ("CA-GC-AI-REG", "cf_purpose", "generic_narrative: description_ai_system_en host"),
    ("EU-PSTW", "cf_purpose", "generic_narrative: Description dedicated-once purpose"),
    ("CA-GC-AI-REG", "om_technical_method", "purpose_vs_technical: capabilities vs description"),
    # Accountable vs supplier conflict
    ("US-OMB-2025", "om_supplier", "accountable_vs_supplier: vendor_name not agency"),
    ("NL-ALGO-REG", "om_supplier", "accountable_vs_supplier: provider vs organization"),
    # Linkage cases
    ("US-OMB-2025", "cf_data_involvement", "linkage: has_pii primary + link_to_data linkage"),
    ("NL-ALGO-REG", "om_risk_or_impact", "linkage: risks primary; impacttoetsen not PRIMARY"),
    # Identity descriptive
    ("US-OMB-2025", "cf_system_identity", "descriptive_only identity"),
    ("UK-ATRS", "cf_system_identity", "descriptive_only + record_locator link"),
    # Jurisdiction-specific legal basis
    ("NL-ALGO-REG", "om_legal_basis", "jurisdiction_specific: lawful_basis"),
    # Additional coverage for remaining functions/sources balance
    ("CA-GC-AI-REG", "cf_data_involvement", "data_involvement primary PI flag"),
    ("CA-GC-AI-REG", "cf_operational_status", "clear_dedicated status"),
    ("EU-PSTW", "cf_operational_status", "PSTW Status with leading-space raw field"),
    ("EU-PSTW", "cf_accountable_body", "Responsible organisation peer-like on catalogue"),
    ("NL-ALGO-REG", "cf_data_involvement", "source_data primary"),
    ("NL-ALGO-REG", "cf_operational_status", "clear_dedicated status"),
    ("US-OMB-2025", "cf_purpose", "clear_dedicated problem_solved"),
    ("US-OMB-2025", "cf_accountable_body", "agency_name dedicated"),
    ("UK-ATRS", "om_technical_method", "clear_absent on API slim"),
    ("UK-ATRS", "cf_data_involvement", "clear_absent on API slim"),
]


def build_pilot_manifest_rows() -> list[dict[str, str]]:
    template = {
        r["coding_unit_id"]: r for r in build_coding_template_rows()
    }
    rows: list[dict[str, str]] = []
    for source, fid, reason in PILOT_SELECTION:
        unit_id = f"{source}__{fid}"
        base = template[unit_id]
        rows.append(
            {
                "pilot_unit_id": unit_id,
                "source_name": source,
                "schema_object_id": base["schema_object_id"],
                "schema_object_type": base["schema_object_type"],
                "disclosure_function_id": fid,
                "function_display_name": base["function_display_name"],
                "tier": base["tier"],
                "scoring_role": base["scoring_role"],
                "default_applicability": base["default_applicability"],
                "selection_rationale": reason,
                "candidate_observed_fields": base["candidate_observed_fields"],
                "known_field_mapping_labels": base["known_field_mapping_labels"],
                "specification_version": base["specification_version"],
                "corpus_lock_reference": base["corpus_lock_reference"],
            }
        )
    return rows


def write_pilot_manifest(path: Path | None = None) -> Path:
    path = path or PILOT_MANIFEST_CSV
    rows = build_pilot_manifest_rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
