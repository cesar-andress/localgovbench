"""Render codebook_affordance_v1.md from frozen Phase 1 artefacts plus operational text."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import yaml

from localgovbench_measurement_validation.affordance.coding.paths import CODEBOOK_MD
from localgovbench_measurement_validation.affordance.paths import (
    APPLICABILITY_OVERRIDES_YAML,
    DISCLOSURE_FUNCTIONS_YAML,
    FIELD_FUNCTION_CANDIDATES_CSV,
)


def _load(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def render_codebook() -> str:
    df = _load(DISCLOSURE_FUNCTIONS_YAML)
    overrides = _load(APPLICABILITY_OVERRIDES_YAML)
    cands = list(csv.DictReader(FIELD_FUNCTION_CANDIDATES_CSV.open(encoding="utf-8")))
    by_fn: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in cands:
        by_fn[row["function_id"]].append(row)

    lines: list[str] = []
    lines += [
        "# Codebook — Schema Disclosure Affordance v1",
        "",
        "**Specification version:** 1.0.0  ",
        "**Coding layer version:** 1.0.0  ",
        "**Unit of analysis:** `schema_object × disclosure_function`  ",
        "**Construct:** schema disclosure affordance (not readiness, maturity, shortfall, compliance, or governance quality).",
        "",
        "## Global coding labels",
        "",
        "| Attribute | Allowed values |",
        "|-----------|----------------|",
        "| Support level | `dedicated`, `indirect`, `absent` |",
        "| Applicability | `universal`, `conditional`, `jurisdiction_specific`, `object_specific`, `catalogue_inapplicable`, `unknown` |",
        "| Encoding type | `free_text`, `structured`, `mixed`, `other`, `not_applicable` |",
        "| Documentary linkage layer | `generic_url`, `record_locator`, `function_specific`, `none`, `not_applicable` |",
        "| Confidence | `high`, `medium`, `low` (metadata only; never changes support) |",
        "",
        "## Support level definitions",
        "",
        "- **dedicated:** Schema exposes a field whose native role is to host this disclosure function.",
        "- **indirect:** Schema exposes only a proxy or adjacent field that may carry related information without being dedicated.",
        "- **absent:** No dedicated or acceptable indirect host for this function on this schema object.",
        "",
        "When applicability is `catalogue_inapplicable`, do **not** assign `dedicated` or `indirect`. Use support `absent` with encoding/linkage `not_applicable`, or follow the pilot sheet instruction for N/A marking while keeping support=`absent`.",
        "",
        "## Global anti-over-credit rules",
        "",
    ]
    for rule in df["meta"]["anti_overcredit_rules"]:
        lines.append(f"- **{rule['id']}:** {rule['rule'].strip()}")
    lines += [
        "",
        "## Prohibited coder behaviours",
        "",
        "- Inferring undisclosed content or organisational quality.",
        "- Using record population rates to decide schema support.",
        "- Treating a generic URL as function-specific evidence without an explicit field role.",
        "- Using LocalGovBench, readiness, maturity, shortfall, or compliance concepts.",
        "- Consulting external pages unless the coding round explicitly authorizes documentation review.",
        "",
        "---",
        "",
    ]

    for fn in list(df["core_functions"]) + list(df["modules"]):
        fid = fn["id"]
        tier = fn.get("scope")
        status = fn.get("status")
        scoring = (
            "descriptive_only"
            if status == "core_unscored"
            else ("core_scored" if status == "core_scored" else "module")
        )
        default_app = overrides.get("function_defaults", {}).get(fid, {}).get("label", "")
        lines += [
            f"## {fid} — {fn['display_name']}",
            "",
            f"- **Identifier:** `{fid}`",
            f"- **Display name:** {fn['display_name']}",
            f"- **Tier:** `{tier}`",
            f"- **Scoring role:** `{scoring}`",
            f"- **Normative definition:** {fn['definition'].strip()}",
            f"- **Primary coding question:** {fn['primary_question'].strip()}",
            "- **Unit of analysis:** schema_object × disclosure_function",
            f"- **Default applicability:** `{default_app}`",
            f"- **Generic field policy:** `{fn.get('generic_field_policy')}`",
            f"- **Documentary linkage relevance:** `{fn.get('documentary_linkage_relevance')}`",
            "",
            "### What counts as DEDICATED",
            "",
            "A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.",
            "",
            "### What counts as INDIRECT",
            "",
            "A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.",
            "",
            "### What counts as ABSENT",
            "",
            "No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).",
            "",
            "### Candidate map (frozen)",
            "",
            "| Source | Label | Raw field | Rationale |",
            "|--------|-------|-----------|-----------|",
        ]
        for row in sorted(by_fn[fid], key=lambda r: (r["source"], r["mapping_label"], r["raw_field"])):
            rat = row["rationale"].replace("|", "/")
            lines.append(
                f"| {row['source']} | {row['mapping_label']} | `{row['raw_field']}` | {rat} |"
            )
        lines += [
            "",
            "### Positive examples",
            "",
            _positives(fid),
            "",
            "### Negative examples / non-examples",
            "",
            _negatives(fid),
            "",
            "### Source-specific caveats",
            "",
            _caveats(fid),
            "",
            "### Common coding errors",
            "",
            _errors(fid),
            "",
            "### Adjudication notes",
            "",
            "- Prefer the frozen candidate map over memory.",
            "- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.",
            "",
            "---",
            "",
        ]
    return "\n".join(lines) + "\n"


def _positives(fid: str) -> str:
    mapping = {
        "cf_system_identity": "- US `use_case_name`; NL `name`; UK `title`.",
        "cf_purpose": "- US `problem_solved`; NL `goal`; CA/PSTW description hosts under anti-over-credit.",
        "cf_operational_status": "- US `development_stage`; NL `status`; CA `ai_system_status_en`; PSTW raw ` Status`.",
        "cf_accountable_body": "- US `agency_name`; CA `government_organization`; NL `organization`.",
        "cf_data_involvement": "- US `has_pii`; CA `involves_personal_information`; NL `source_data`.",
        "om_human_oversight": "- NL `human_intervention` (dedicated).",
        "om_risk_or_impact": "- US `is_high_impact`; NL `risks`.",
        "om_legal_basis": "- NL `lawful_basis`.",
        "om_supplier": "- US `vendor_name`; CA `vendor_information`; NL `provider`.",
        "om_technical_method": "- NL `methods_and_models`; CA `ai_system_capabilities_en`; US `classification`.",
        "om_redress_pointer": "- US `hi_appeal_process` only under high-impact conditional applicability.",
    }
    return mapping.get(fid, "- See candidate map.")


def _negatives(fid: str) -> str:
    mapping = {
        "cf_system_identity": "- US `system_name_ato`; NL `source_id`; UK `format`/`index`.",
        "cf_purpose": "- `topic_area`; NL `proportionality`; capabilities fields reserved for technical.",
        "cf_operational_status": "- Any date/year/timestamp field (`operational_date`, `begin_date`, `Start Year`, etc.).",
        "cf_accountable_body": "- Vendor/provider fields; `contact_email`; UK `organisation_title` as dedicated.",
        "cf_data_involvement": "- `demographic_features`; `hi_training_established`; `notification_ai`; `impacttoetsen`.",
        "om_human_oversight": "- `have_ato`; `contact_email`; using description as dedicated.",
        "om_risk_or_impact": "- PSTW outcome `Improved…` flags; NL `proportionality`; `impacttoetsen` as PRIMARY.",
        "om_legal_basis": "- Inferring law from purpose text; using `proportionality`.",
        "om_supplier": "- Agency/organization accountable-body fields.",
        "om_technical_method": "- Purpose primaries (`problem_solved`, `goal`); purpose-dedicated descriptions.",
        "om_redress_pointer": "- `contact_email`; `notification_ai`.",
    }
    return mapping.get(fid, "- Rejected candidates in the map.")


def _caveats(fid: str) -> str:
    mapping = {
        "cf_system_identity": "- Descriptive only; do not use in scored affordance profiles.",
        "cf_purpose": "- UK description is INDIRECT only. Generic description may be dedicated at most once (usually purpose).",
        "cf_operational_status": "- PSTW raw field name is ` Status` (leading space).",
        "cf_accountable_body": "- UK publisher identity is INDIRECT only.",
        "cf_data_involvement": "- PSTW is catalogue_inapplicable. Report primary vs narrative fallback separately later (realization).",
        "om_human_oversight": "- US hi_* fields are conditional on high-impact subclass.",
        "om_risk_or_impact": "- NL `publication_category` is SECONDARY only; `impacttoetsen` not PRIMARY.",
        "om_legal_basis": "- Jurisdiction-specific; dedicated host observed only in NL export.",
        "om_supplier": "- Do not confuse with accountable body.",
        "om_technical_method": "- If description is dedicated for purpose, it cannot also be dedicated technical.",
        "om_redress_pointer": "- Conditional; generic contact is never sufficient.",
    }
    return mapping.get(fid, "- See applicability_overrides_v1.yaml.")


def _errors(fid: str) -> str:
    return (
        "- Upgrading INDIRECT to DEDICATED because a narrative is rich.\n"
        "- Using population rates.\n"
        "- Ignoring REJECTED rows in the candidate map.\n"
        f"- Function-specific: see caveats for `{fid}`."
    )


def write_codebook(path: Path | None = None) -> Path:
    path = path or CODEBOOK_MD
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_codebook(), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write_codebook())
