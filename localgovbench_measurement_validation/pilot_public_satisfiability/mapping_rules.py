"""Source schemas and criterion mapping rules for public-satisfiability pilot."""

from __future__ import annotations

SHORTFALL_LABELS: dict[int, str] = {
    0: "no_public_field",
    1: "weak_metadata_proxy",
    2: "partial_programme_level_signal",
    3: "named_public_artefact_possible",
    4: "full_evidence_gate_reachable",
}

COVERAGE_TO_SHORTFALL: dict[str, int] = {
    "no_public_field": 0,
    "weak_proxy": 1,
    "direct_field": 2,
    "named_artifact_possible": 3,
}

# source_name -> native field names in that inventory schema
SOURCE_SCHEMAS: dict[str, list[str]] = {
    "US-OMB-2025": [
        "agency",
        "agency_name",
        "id",
        "use_case_name",
        "agency_bureau",
        "contact_email",
        "development_stage",
        "is_high_impact",
        "HI_justification",
        "topic_area",
        "classification",
        "problem_solved",
        "benefits",
        "system_outputs",
        "operational_date",
        "contracting_usage",
        "vendor_name",
        "have_ato",
        "human_roles",
        "data_used_for_training",
        "data_used_for_inference",
        "data_used_for_evaluation",
    ],
    "CA-GC-AI-REG": [
        "ai_register_id",
        "name_ai_system_en",
        "government_organization",
        "description_ai_system_en",
        "vendor_information",
        "ai_system_status_en",
        "status_date",
        "ai_system_capabilities_en",
        "data_sources_en",
        "involves_personal_information",
        "developed_by_en",
        "ai_system_primary_users_en",
        "ai_system_results_en",
        "notification_ai",
    ],
    "NL-ALGO-REG": [
        "name",
        "organization",
        "department",
        "description_short",
        "category",
        "website",
        "status",
        "goal",
        "proportionality",
        "lawful_basis",
        "contact_email",
        "methods_and_models",
        "human_intervention",
        "risks",
        "provider",
        "source_data",
        "impacttoetsen",
        "begin_date",
        "end_date",
        "tags",
        "url",
        "source_id",
    ],
    "EU-PSTW": [
        "PSTW ID",
        "Name",
        "Description",
        "Geographical coverage (country)",
        "Responsible organisation",
        "Responsible organisation category",
        "Status",
        "Primary Technology",
        "Secondary Technology",
        "Application type",
        "Process type",
        "Start Year",
        "End Year",
    ],
    "UK-ATRS": [
        "title",
        "description",
        "link",
        "organisation_title",
        "format",
        "index",
        "public_timestamp",
    ],
}

# criterion_id -> {source_name: (coverage_class, fields, rationale, can_gate)}
MAPPING_RULES: dict[str, dict[str, tuple[str, list[str], str, bool]]] = {
    "legal_regulatory_gdpr_readiness": {
        "US-OMB-2025": ("no_public_field", [], "No RoPA/DPIA fields in OMB schema.", False),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["involves_personal_information", "data_sources_en"],
            "Personal-information flag is not GDPR readiness documentation.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["source_data", "impacttoetsen"],
            "Dataset and impact-assessment references are not RoPA/DPIA records.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No GDPR accountability fields in PSTW schema.", False),
        "UK-ATRS": ("no_public_field", [], "ATRS search metadata lacks GDPR artefact fields.", False),
    },
    "legal_regulatory_ai_act_alignment": {
        "US-OMB-2025": (
            "direct_field",
            ["is_high_impact", "HI_justification", "development_stage"],
            "High-impact designation and justification are direct inventory disclosures.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["description_ai_system_en", "notification_ai"],
            "Narrative may mention risk but not deployer classification memo.",
            False,
        ),
        "NL-ALGO-REG": (
            "direct_field",
            ["risks", "impacttoetsen", "proportionality"],
            "Dutch register publishes risk and impact-assessment narratives.",
            False,
        ),
        "EU-PSTW": (
            "weak_proxy",
            ["Description", "Application type"],
            "Case description may mention AI use but not formal classification memo.",
            False,
        ),
        "UK-ATRS": (
            "weak_proxy",
            ["description"],
            "ATRS record summary may reference risk context without classification memo.",
            False,
        ),
    },
    "legal_regulatory_data_retention": {
        "US-OMB-2025": ("no_public_field", [], "No retention schedule fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No retention schedule fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No retention schedule fields.", False),
        "EU-PSTW": ("no_public_field", [], "No retention schedule fields.", False),
        "UK-ATRS": ("no_public_field", [], "No retention schedule fields.", False),
    },
    "legal_regulatory_lawful_basis": {
        "US-OMB-2025": ("no_public_field", [], "No lawful-basis register fields.", False),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["involves_personal_information"],
            "PI flag does not document lawful basis.",
            False,
        ),
        "NL-ALGO-REG": (
            "direct_field",
            ["lawful_basis"],
            "Dutch Algorithm Register includes explicit lawful-basis field.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No lawful-basis fields.", False),
        "UK-ATRS": ("no_public_field", [], "No lawful-basis fields.", False),
    },
    "legal_regulatory_cross_border_avoidance": {
        "US-OMB-2025": ("no_public_field", [], "No hosting/egress architecture fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No residency/egress fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No hosting/egress architecture fields.", False),
        "EU-PSTW": (
            "weak_proxy",
            ["Geographical coverage (country)"],
            "Geographic coverage is not egress/residency architecture proof.",
            False,
        ),
        "UK-ATRS": ("no_public_field", [], "No residency/egress fields.", False),
    },
    "technical_security_local_architecture": {
        "US-OMB-2025": ("no_public_field", [], "No architecture diagram fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No architecture fields.", False),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["methods_and_models", "website"],
            "Methods/models narrative is not deployment architecture diagram.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No architecture fields.", False),
        "UK-ATRS": ("no_public_field", [], "No architecture fields in search metadata.", False),
    },
    "technical_security_access_control": {
        "US-OMB-2025": ("no_public_field", [], "No IAM/access-control fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No IAM/access-control fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No IAM/access-control fields.", False),
        "EU-PSTW": ("no_public_field", [], "No IAM/access-control fields.", False),
        "UK-ATRS": ("no_public_field", [], "No IAM/access-control fields.", False),
    },
    "technical_security_logging": {
        "US-OMB-2025": ("no_public_field", [], "No logging policy fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No logging policy fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No logging policy fields.", False),
        "EU-PSTW": ("no_public_field", [], "No logging policy fields.", False),
        "UK-ATRS": ("no_public_field", [], "No logging policy fields.", False),
    },
    "technical_security_auditability": {
        "US-OMB-2025": (
            "weak_proxy",
            ["have_ato"],
            "ATO flag implies authorization process, not audit trail artefacts.",
            False,
        ),
        "CA-GC-AI-REG": ("no_public_field", [], "No audit trail fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No audit trail fields.", False),
        "EU-PSTW": ("no_public_field", [], "No audit trail fields.", False),
        "UK-ATRS": ("no_public_field", [], "No audit trail fields.", False),
    },
    "technical_security_model_updates": {
        "US-OMB-2025": ("no_public_field", [], "No model change-management fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No model lifecycle fields.", False),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["methods_and_models"],
            "Model/method description is not change-control procedure.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No model lifecycle fields.", False),
        "UK-ATRS": ("no_public_field", [], "No model lifecycle fields.", False),
    },
    "organizational_accountability": {
        "US-OMB-2025": (
            "weak_proxy",
            ["agency_name", "agency_bureau", "HI_justification"],
            "Organizational attribution without governance charter.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["government_organization"],
            "Owning organization only.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["organization", "goal", "proportionality"],
            "Organisation and purpose fields are not governance charter.",
            False,
        ),
        "EU-PSTW": (
            "weak_proxy",
            ["Responsible organisation", "Description"],
            "Responsible organisation attribution only.",
            False,
        ),
        "UK-ATRS": (
            "weak_proxy",
            ["organisation_title", "description"],
            "Publishing organisation and summary only.",
            False,
        ),
    },
    "organizational_ownership": {
        "US-OMB-2025": (
            "weak_proxy",
            ["contact_email", "agency_bureau"],
            "Contact/bureau are weak ownership proxies.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["government_organization"],
            "Organization name only; no RACI.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["organization", "contact_email", "department"],
            "Organisation/contact are weak ownership proxies.",
            False,
        ),
        "EU-PSTW": (
            "weak_proxy",
            ["Responsible organisation"],
            "Organisation name only.",
            False,
        ),
        "UK-ATRS": (
            "weak_proxy",
            ["organisation_title"],
            "Organisation title only.",
            False,
        ),
    },
    "organizational_role_definition": {
        "US-OMB-2025": (
            "weak_proxy",
            ["human_roles"],
            "Human roles narrative may partially describe functions.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["ai_system_primary_users_en"],
            "Primary users field is not full role definition.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["human_intervention"],
            "Human intervention field is not full role matrix.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No role-definition fields.", False),
        "UK-ATRS": ("no_public_field", [], "No role-definition fields in search metadata.", False),
    },
    "organizational_procurement_governance": {
        "US-OMB-2025": (
            "weak_proxy",
            ["vendor_name", "contracting_usage"],
            "Supplier/contracting metadata only; not contract clauses.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["vendor_information", "developed_by_en"],
            "Vendor/developer disclosure without contract governance text.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["provider"],
            "Provider field indicates supplier presence only.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No procurement clause fields.", False),
        "UK-ATRS": ("no_public_field", [], "No procurement clause fields.", False),
    },
    "organizational_risk_ownership": {
        "US-OMB-2025": ("no_public_field", [], "No risk register fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No risk register fields.", False),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["risks"],
            "Risk narrative is not institutional risk register.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No risk register fields.", False),
        "UK-ATRS": (
            "weak_proxy",
            ["description"],
            "Description may mention risks without risk register.",
            False,
        ),
    },
    "operational_monitoring": {
        "US-OMB-2025": (
            "weak_proxy",
            ["system_outputs", "benefits"],
            "Intended outputs/benefits are not monitoring dashboards.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["ai_system_results_en", "ai_system_capabilities_en"],
            "Results/capabilities narrative only.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["goal", "description_short"],
            "Goal/description are not monitoring dashboards.",
            False,
        ),
        "EU-PSTW": (
            "weak_proxy",
            ["Description"],
            "Case description may mention outcomes but not dashboards.",
            False,
        ),
        "UK-ATRS": (
            "weak_proxy",
            ["description"],
            "Summary may reference outputs but not monitoring artefacts.",
            False,
        ),
    },
    "operational_incident_response": {
        "US-OMB-2025": ("no_public_field", [], "No IR plan fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No IR plan fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No IR plan fields.", False),
        "EU-PSTW": ("no_public_field", [], "No IR plan fields.", False),
        "UK-ATRS": ("no_public_field", [], "No IR plan fields.", False),
    },
    "operational_human_oversight": {
        "US-OMB-2025": (
            "direct_field",
            ["human_roles"],
            "OMB schema includes explicit human roles field.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["description_ai_system_en"],
            "Oversight may appear only in free text.",
            False,
        ),
        "NL-ALGO-REG": (
            "direct_field",
            ["human_intervention"],
            "Dutch register includes explicit human intervention field.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No human oversight fields.", False),
        "UK-ATRS": (
            "weak_proxy",
            ["description"],
            "Oversight may appear only in record summary text.",
            False,
        ),
    },
    "operational_documentation": {
        "US-OMB-2025": ("no_public_field", [], "No prompt/runbook documentation fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No operator documentation fields.", False),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["url", "website"],
            "External links may point to docs but are not operator handbooks.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No operator documentation fields.", False),
        "UK-ATRS": (
            "weak_proxy",
            ["link"],
            "Record URL is transparency page, not operator handbook.",
            False,
        ),
    },
    "operational_lifecycle_management": {
        "US-OMB-2025": (
            "direct_field",
            ["development_stage", "operational_date"],
            "Lifecycle stage and operational date are direct inventory fields.",
            False,
        ),
        "CA-GC-AI-REG": (
            "direct_field",
            ["ai_system_status_en", "status_date"],
            "System status and status date map to lifecycle metadata.",
            False,
        ),
        "NL-ALGO-REG": (
            "direct_field",
            ["status", "begin_date", "end_date"],
            "Status and date fields are direct lifecycle metadata.",
            False,
        ),
        "EU-PSTW": (
            "direct_field",
            ["Status", "Start Year", "End Year"],
            "Status and year fields are direct lifecycle metadata.",
            False,
        ),
        "UK-ATRS": (
            "weak_proxy",
            ["public_timestamp"],
            "Publication date is not deployment lifecycle gate.",
            False,
        ),
    },
    "strategic_sovereignty_vendor_independence": {
        "US-OMB-2025": (
            "weak_proxy",
            ["vendor_name", "contracting_usage"],
            "Vendor listing supports dependency description only.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["vendor_information", "developed_by_en"],
            "Vendor/developer fields are dependency proxies.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["provider"],
            "Provider field is dependency proxy only.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No vendor dependency fields.", False),
        "UK-ATRS": ("no_public_field", [], "No vendor dependency fields.", False),
    },
    "strategic_sovereignty_data_sovereignty": {
        "US-OMB-2025": (
            "weak_proxy",
            ["data_used_for_training", "data_used_for_inference"],
            "Data-use categories are not residency/sovereignty proof.",
            False,
        ),
        "CA-GC-AI-REG": (
            "weak_proxy",
            ["data_sources_en"],
            "Data source narrative is not sovereignty design.",
            False,
        ),
        "NL-ALGO-REG": (
            "weak_proxy",
            ["source_data"],
            "Source data narrative is not sovereignty design.",
            False,
        ),
        "EU-PSTW": ("no_public_field", [], "No data sovereignty fields.", False),
        "UK-ATRS": ("no_public_field", [], "No data sovereignty fields.", False),
    },
    "strategic_sovereignty_infrastructure_control": {
        "US-OMB-2025": ("no_public_field", [], "No infrastructure ownership fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No infrastructure fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No infrastructure fields.", False),
        "EU-PSTW": ("no_public_field", [], "No infrastructure fields.", False),
        "UK-ATRS": ("no_public_field", [], "No infrastructure fields.", False),
    },
    "strategic_sovereignty_portability": {
        "US-OMB-2025": ("no_public_field", [], "No portability/migration fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No portability fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No portability fields.", False),
        "EU-PSTW": ("no_public_field", [], "No portability fields.", False),
        "UK-ATRS": ("no_public_field", [], "No portability fields.", False),
    },
    "strategic_sovereignty_maintainability": {
        "US-OMB-2025": ("no_public_field", [], "No sustainment roadmap fields.", False),
        "CA-GC-AI-REG": ("no_public_field", [], "No sustainment roadmap fields.", False),
        "NL-ALGO-REG": ("no_public_field", [], "No sustainment roadmap fields.", False),
        "EU-PSTW": ("no_public_field", [], "No sustainment roadmap fields.", False),
        "UK-ATRS": ("no_public_field", [], "No sustainment roadmap fields.", False),
    },
}


def compute_shortfall(
    coverage_class: str,
    can_gate: bool,
    expected_artifact_type: str,
) -> tuple[int, str, str]:
    """Return (level, label, reason_gate_not_reachable)."""
    if can_gate:
        return 4, SHORTFALL_LABELS[4], ""

    level = COVERAGE_TO_SHORTFALL.get(coverage_class, 0)
    label = SHORTFALL_LABELS[level]

    if level >= 4:
        return level, label, ""

    reasons = {
        0: (
            f"No native inventory field maps to {expected_artifact_type}; "
            "public schema lacks programme-level signal."
        ),
        1: (
            f"Only weak metadata proxies available; cannot substantiate named "
            f"{expected_artifact_type} for score ≥3 gate."
        ),
        2: (
            f"Partial programme-level inventory fields present but do not constitute "
            f"primary {expected_artifact_type} required for evidence gate ≥3."
        ),
        3: (
            f"Named public artefact may be inferable but does not meet LocalGovBench "
            f"primary-artefact threshold for {expected_artifact_type}."
        ),
    }
    return level, label, reasons.get(level, reasons[0])


def max_shortfall_level(rows: list[dict]) -> int:
    return max(int(r["evidence_shortfall_level"]) for r in rows)


def classify_from_evidence_rows(
    rows: list[dict],
    *,
    criterion_id: str = "",
    evidence_hint: str = "",
    expected_artifact_type: str = "",
) -> str:
    """Deterministic partition from source×criterion shortfall levels + evidence hints."""
    import re

    internal_kw = re.compile(
        r"\b(architecture|IAM|access control|logging|audit trail|retention|"
        r"incident response|runbook|prompt registry|portability|migration|"
        r"infrastructure|RoPA|DPIA|lawful basis register|risk register|"
        r"contract clause|RACI|role description|sustainment)\b",
        re.I,
    )
    partial_kw = re.compile(
        r"\b(oversight|human|lifecycle|stage|status|deployment|vendor|"
        r"supplier|monitoring|classification|impact|governance charter|"
        r"organisation|organization|contact|provider)\b",
        re.I,
    )

    level = max(int(r["evidence_shortfall_level"]) for r in rows)
    has_direct = any(r.get("coverage_class") == "direct_field" for r in rows)
    hint = f"{evidence_hint} {expected_artifact_type}"

    if level >= 3:
        return "public_satisfiable"
    if level >= 2:
        if criterion_id == "operational_lifecycle_management" and has_direct:
            return "public_satisfiable"
        return "partially_public_satisfiable"
    if level == 1:
        if has_direct:
            return "partially_public_satisfiable"
        if partial_kw.search(hint) and not internal_kw.search(hint):
            return "partially_public_satisfiable"
        if internal_kw.search(hint):
            return "structurally_internal"
        return "partially_public_satisfiable"
    return "structurally_internal"
