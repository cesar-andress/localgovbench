"""GRB indicator specification — 6 dimensions × 3 subdimensions × 3 indicators."""

from __future__ import annotations

from dataclasses import dataclass

GRB_SPEC_VERSION = "0.1-experiment"

# Dimensions subject to safeguard rule G1 (cap readiness at 60 if score < 2.0).
SAFEGUARD_DIMENSION_IDS = frozenset({"d2", "d4"})


@dataclass(frozen=True, slots=True)
class GRBIndicator:
    """A single observable governance indicator."""

    id: str
    dimension_id: str
    subdimension_id: str
    name: str
    prompt: str


@dataclass(frozen=True, slots=True)
class GRBSubdimension:
    """Three indicators grouped for subdimension-level scoring."""

    id: str
    dimension_id: str
    name: str
    indicators: tuple[GRBIndicator, ...]


@dataclass(frozen=True, slots=True)
class GRBDimension:
    """Six top-level GRB dimensions."""

    id: str
    name: str
    subdimensions: tuple[GRBSubdimension, ...]


def _build_specification() -> tuple[GRBDimension, ...]:
    """Build the 54-indicator GRB tree."""
    dimensions: list[GRBDimension] = []

    structure: tuple[tuple[str, str, tuple[tuple[str, str], ...]], ...] = (
        (
            "d1",
            "Accountability Architecture",
            (
                ("mandate", "Political mandate and purpose", ("policy_roadmap", "use_case_inventory", "mandate_review")),
                ("ownership", "Ownership and RACI", ("service_owner", "raci_matrix", "escalation_contacts")),
                ("accountability", "Ex-post accountability", ("complaint_procedure", "corrective_actions", "governance_report")),
            ),
        ),
        (
            "d2",
            "Human Oversight and Control",
            (
                ("oversight_design", "Oversight design", ("influence_map", "review_thresholds", "automation_limits")),
                ("intervention", "Intervention capacity", ("override_procedure", "response_sla", "supervisor_training")),
                ("traceability", "Control traceability", ("prompt_approval_log", "review_samples", "case_linkage")),
            ),
        ),
        (
            "d3",
            "Transparency and Justification",
            (
                ("internal_transparency", "Internal transparency", ("capability_docs", "prompt_registry", "limitations_guide")),
                ("external_transparency", "External transparency", ("citizen_notice", "rights_information", "logic_description")),
                ("justification", "Justification of use", ("relevant_reasons_template", "rejection_log", "utility_risk_review")),
            ),
        ),
        (
            "d4",
            "Data and Legal Legitimacy",
            (
                ("lawfulness", "Lawfulness and purpose", ("ropa_entries", "lawful_basis_register", "dpia_reference")),
                ("minimization", "Minimization and retention", ("minimization_rules", "retention_schedule", "log_redaction")),
                ("data_sovereignty", "Data sovereignty", ("residency_diagram", "subprocessor_list", "egress_controls")),
            ),
        ),
        (
            "d5",
            "Risk and Assurance Governance",
            (
                ("risk_identification", "Risk identification", ("ai_risk_register", "risk_classification", "post_change_review")),
                ("security_change", "Security and change", ("least_privilege", "patch_management", "config_audit")),
                ("monitoring_incidents", "Monitoring and incidents", ("monitoring_plan", "incident_response", "post_incident_review")),
            ),
        ),
        (
            "d6",
            "Strategic Sovereignty",
            (
                ("infrastructure", "Infrastructure control", ("hosting_model", "dr_bcp", "capacity_plan")),
                ("vendor_independence", "Vendor independence", ("dependency_analysis", "contract_exit", "migration_path")),
                ("capacity", "Sustainability", ("budget_line", "skills_plan", "technical_debt_register")),
            ),
        ),
    )

    for dim_id, dim_name, subdims in structure:
        sub_list: list[GRBSubdimension] = []
        for sub_id, sub_name, indicator_suffixes in subdims:
            indicators: list[GRBIndicator] = []
            for idx, suffix in enumerate(indicator_suffixes, start=1):
                ind_id = f"{dim_id}_{sub_id}_{idx:02d}"
                indicators.append(
                    GRBIndicator(
                        id=ind_id,
                        dimension_id=dim_id,
                        subdimension_id=sub_id,
                        name=suffix.replace("_", " ").title(),
                        prompt=f"Assess {suffix.replace('_', ' ')} for sovereign LLM governance.",
                    )
                )
            sub_list.append(
                GRBSubdimension(
                    id=sub_id,
                    dimension_id=dim_id,
                    name=sub_name,
                    indicators=tuple(indicators),
                )
            )
        dimensions.append(GRBDimension(id=dim_id, name=dim_name, subdimensions=tuple(sub_list)))

    return tuple(dimensions)


GRB_DIMENSIONS: tuple[GRBDimension, ...] = _build_specification()


def load_indicator_specification() -> tuple[GRBDimension, ...]:
    """Return the full GRB indicator specification."""
    return GRB_DIMENSIONS


def all_indicator_ids() -> tuple[str, ...]:
    """Return all 54 indicator ids in specification order."""
    ids: list[str] = []
    for dimension in GRB_DIMENSIONS:
        for subdimension in dimension.subdimensions:
            for indicator in subdimension.indicators:
                ids.append(indicator.id)
    return tuple(ids)


def indicator_count() -> int:
    return len(all_indicator_ids())
