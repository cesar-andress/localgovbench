#!/usr/bin/env python3
"""Generate LocalGovBench criteria config with public-satisfiability classifications."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_delphi_round1_instrument import build_assessment_question  # noqa: E402
from localgovbench.framework.dimensions import FRAMEWORK_VERSION, GOVERNANCE_DIMENSIONS  # noqa: E402
from localgovbench_measurement_validation.pilot_public_satisfiability.pilot_paths import (  # noqa: E402
    CONFIG_CRITERIA,
)

# Expert preliminary classification for public-satisfiability pilot (not empirically calibrated).
SATISFIABILITY: dict[str, tuple[str, str, str]] = {
    # criterion_id -> (class, expected_artifact_type, rationale)
    "legal_regulatory_gdpr_readiness": (
        "structurally_internal",
        "RoPA/DPIA/DPO consultation records",
        "GDPR accountability artefacts are internal compliance records rarely published in AI inventories.",
    ),
    "legal_regulatory_ai_act_alignment": (
        "partially_public_satisfiable",
        "Use-case classification / impact memo",
        "Inventories may disclose high-impact flags and risk narratives but seldom publish formal classification memos.",
    ),
    "legal_regulatory_data_retention": (
        "structurally_internal",
        "Retention schedule and deletion configuration",
        "Retention rules and backup handling are operational policies not typically inventory fields.",
    ),
    "legal_regulatory_lawful_basis": (
        "structurally_internal",
        "Lawful basis register entries",
        "Purpose limitation registers are internal legal records.",
    ),
    "legal_regulatory_cross_border_avoidance": (
        "structurally_internal",
        "Architecture diagram and egress controls",
        "Hosting/egress evidence requires technical architecture documentation.",
    ),
    "technical_security_local_architecture": (
        "structurally_internal",
        "Architecture diagrams and component inventory",
        "End-to-end deployment architecture is internal technical documentation.",
    ),
    "technical_security_access_control": (
        "structurally_internal",
        "IAM role matrix and access review records",
        "Access control evidence is security operations documentation.",
    ),
    "technical_security_logging": (
        "structurally_internal",
        "Logging policy and log schemas",
        "Logging/redaction policies are internal security artefacts.",
    ),
    "technical_security_auditability": (
        "structurally_internal",
        "Audit trail configuration and change tickets",
        "Immutable audit trails are internal operational records.",
    ),
    "technical_security_model_updates": (
        "structurally_internal",
        "Model change procedure and rollback runbook",
        "Model lifecycle change control is internal MLOps documentation.",
    ),
    "organizational_accountability": (
        "partially_public_satisfiable",
        "Governance charter / committee terms",
        "Inventories may name agencies and impacts but rarely publish governance charters.",
    ),
    "organizational_ownership": (
        "partially_public_satisfiable",
        "RACI / ownership matrix",
        "Contact or bureau fields are weak ownership proxies only.",
    ),
    "organizational_role_definition": (
        "structurally_internal",
        "Role descriptions and training plans",
        "Interdisciplinary role definitions are HR/organizational internal documents.",
    ),
    "organizational_procurement_governance": (
        "partially_public_satisfiable",
        "Contract clauses on AI support and exit",
        "Vendor/contracting fields indicate supplier presence, not contract governance clauses.",
    ),
    "organizational_risk_ownership": (
        "structurally_internal",
        "Risk register and risk appetite statement",
        "Institutional risk registers are internal governance artefacts.",
    ),
    "operational_monitoring": (
        "partially_public_satisfiable",
        "Monitoring dashboards and review reports",
        "Outputs/benefits fields describe intended monitoring outcomes, not dashboards.",
    ),
    "operational_incident_response": (
        "structurally_internal",
        "Incident response plan and exercise records",
        "IR plans are internal operational security documents.",
    ),
    "operational_human_oversight": (
        "partially_public_satisfiable",
        "Human oversight procedures",
        "Some inventories include human-in-the-loop role descriptions as narrative text.",
    ),
    "operational_documentation": (
        "structurally_internal",
        "Prompt registry and operator handbook",
        "System documentation sets are internal operator materials.",
    ),
    "operational_lifecycle_management": (
        "public_satisfiable",
        "Lifecycle stage gates / deployment status",
        "Official inventories commonly publish development or deployment stage metadata.",
    ),
    "strategic_sovereignty_vendor_independence": (
        "partially_public_satisfiable",
        "Supplier analysis and contingency plan",
        "Vendor fields support dependency description, not independence analysis.",
    ),
    "strategic_sovereignty_data_sovereignty": (
        "structurally_internal",
        "Data residency and storage design",
        "Data sovereignty requires technical/data architecture evidence.",
    ),
    "strategic_sovereignty_infrastructure_control": (
        "structurally_internal",
        "Infrastructure ownership and DR design",
        "Hosting/capacity plans are internal infrastructure documents.",
    ),
    "strategic_sovereignty_portability": (
        "structurally_internal",
        "Migration test results and export formats",
        "Portability evidence requires migration testing records.",
    ),
    "strategic_sovereignty_maintainability": (
        "structurally_internal",
        "Sustainment roadmap and budget lines",
        "Long-term staffing and upgrade plans are internal financial/HR planning.",
    ),
}


def main() -> int:
    try:
        import yaml
    except ImportError:
        print("PyYAML required", file=sys.stderr)
        return 1

    criteria_out: list[dict] = []
    for dimension in GOVERNANCE_DIMENSIONS:
        for criterion in dimension.criteria:
            cid = f"{dimension.id}_{criterion.id}"
            sat_class, artifact_type, rationale = SATISFIABILITY[cid]
            criteria_out.append(
                {
                    "criterion_id": cid,
                    "dimension_id": dimension.id,
                    "dimension_name": dimension.name,
                    "assessment_question": build_assessment_question(criterion.statement),
                    "criterion_statement": criterion.statement,
                    "evidence_hint": criterion.suggested_evidence,
                    "expected_artifact_type": artifact_type,
                    "preliminary_public_satisfiability_class": sat_class,
                    "rationale_for_classification": rationale,
                    "evidence_gate_score_3_requires": (
                        "≥1 primary named artefact per LocalGovBench v0.1 scoring rubric"
                    ),
                }
            )

    doc = {
        "schema_version": "1.0",
        "instrument_version": "v0.1.0",
        "framework_version": FRAMEWORK_VERSION,
        "study_framing": {
            "claim": "public_satisfiability_of_evidence_requirements",
            "not_measured": ["readiness_scores", "municipality_rankings", "legal_compliance"],
            "paper2_firewall": [
                "no_paper2_corpus",
                "no_documentary_observability_analysis",
                "no_vendor_stewardship_central_claim",
                "no_document_genre_comparison",
                "no_documentary_accountability_architecture",
            ],
        },
        "criteria": criteria_out,
    }

    CONFIG_CRITERIA.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Generated from localgovbench/framework/dimensions.py\n"
        "# Regenerate: python3.12 scripts/generate_localgovbench_criteria_config.py\n\n"
    )
    CONFIG_CRITERIA.write_text(
        header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"Wrote {CONFIG_CRITERIA.relative_to(ROOT)} ({len(criteria_out)} criteria)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
