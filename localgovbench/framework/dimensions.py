"""Local AI Governance Framework (v0.1) — dimension definitions."""

from __future__ import annotations

from dataclasses import dataclass

FRAMEWORK_VERSION = "0.1"


@dataclass(frozen=True, slots=True)
class GovernanceCriterion:
    """An assessable criterion within a governance dimension."""

    id: str
    statement: str
    suggested_evidence: str
    risk_if_missing: str


@dataclass(frozen=True, slots=True)
class GovernanceDimension:
    """A thematic area for assessing local/on-premise LLM deployments."""

    id: str
    name: str
    description: str
    criteria: tuple[GovernanceCriterion, ...]
    weight: float = 1.0


GOVERNANCE_DIMENSIONS: tuple[GovernanceDimension, ...] = (
    GovernanceDimension(
        id="legal_regulatory",
        name="Legal and Regulatory Compliance",
        description=(
            "Assesses whether the deployment aligns with applicable data protection and "
            "AI regulatory expectations, including lawful processing, retention, and "
            "jurisdictional constraints for on-premise systems in European public bodies."
        ),
        criteria=(
            GovernanceCriterion(
                id="gdpr_readiness",
                statement="GDPR readiness for training, inference, and logging data flows.",
                suggested_evidence=(
                    "Records of processing, privacy notices, DPIA where applicable, "
                    "and DPO consultation notes."
                ),
                risk_if_missing=(
                    "Unlawful or undocumented processing; difficulty demonstrating "
                    "accountability to supervisory authorities."
                ),
            ),
            GovernanceCriterion(
                id="ai_act_alignment",
                statement="EU AI Act alignment documented for the deployer role and use case.",
                suggested_evidence=(
                    "Use-case classification memo, risk management notes, human oversight "
                    "description, and technical documentation references."
                ),
                risk_if_missing=(
                    "Gaps in deployer obligations and post-deployment monitoring may go "
                    "unidentified until external audit or incident."
                ),
            ),
            GovernanceCriterion(
                id="data_retention",
                statement="Data retention and deletion rules defined for prompts, logs, and embeddings.",
                suggested_evidence=(
                    "Retention schedule, automated deletion configuration, and backup "
                    "handling procedures."
                ),
                risk_if_missing=(
                    "Excessive retention of prompts or logs increases exposure and "
                    "complicates erasure requests."
                ),
            ),
            GovernanceCriterion(
                id="lawful_basis",
                statement="Lawful basis and purpose limitation recorded for each data category used.",
                suggested_evidence=(
                    "Lawful basis register entries, purpose statements in system design "
                    "documents, and data minimization checklist."
                ),
                risk_if_missing=(
                    "Processing may lack demonstrable legal grounding; harder to justify "
                    "secondary use of interaction data."
                ),
            ),
            GovernanceCriterion(
                id="cross_border_avoidance",
                statement="Cross-border data transfer avoidance for on-premise workloads.",
                suggested_evidence=(
                    "Architecture diagram showing EU hosting, egress controls, vendor "
                    "sub-processor list, and network policy excerpts."
                ),
                risk_if_missing=(
                    "Unintended transfers via APIs, telemetry, or cloud-backed components "
                    "may undermine sovereignty claims."
                ),
            ),
        ),
    ),
    GovernanceDimension(
        id="technical_security",
        name="Technical and Security Readiness",
        description=(
            "Covers the security posture of local or on-premise large language model "
            "deployments, including access control, observability, and controlled model change."
        ),
        criteria=(
            GovernanceCriterion(
                id="local_architecture",
                statement="Local deployment architecture documented end-to-end.",
                suggested_evidence=(
                    "Architecture diagrams, component inventory, segmentation model, and "
                    "secrets management approach."
                ),
                risk_if_missing=(
                    "Opaque dependencies complicate incident response and sovereignty review."
                ),
            ),
            GovernanceCriterion(
                id="access_control",
                statement="Access control enforces least privilege for operators and end users.",
                suggested_evidence=(
                    "IAM role matrix, authentication method description, and periodic "
                    "access review records."
                ),
                risk_if_missing=(
                    "Over-privileged accounts increase risk of data exfiltration or model misuse."
                ),
            ),
            GovernanceCriterion(
                id="logging",
                statement="Logging captures security-relevant and operational events without excess personal data.",
                suggested_evidence=(
                    "Logging policy, sample log schemas, and redaction or pseudonymization rules."
                ),
                risk_if_missing=(
                    "Forensics and accountability are weakened after security or safety incidents."
                ),
            ),
            GovernanceCriterion(
                id="auditability",
                statement="Auditability supports traceability of configuration and inference changes.",
                suggested_evidence=(
                    "Audit trail configuration, change management tickets, and immutable log store references."
                ),
                risk_if_missing=(
                    "Inability to reconstruct who changed models, prompts, or policies when investigating harm."
                ),
            ),
            GovernanceCriterion(
                id="model_updates",
                statement="Model update management defines testing, approval, and rollback.",
                suggested_evidence=(
                    "Model change procedure, validation results, version registry, and rollback runbook."
                ),
                risk_if_missing=(
                    "Uncontrolled updates may introduce drift, bias, or safety regressions without notice."
                ),
            ),
        ),
    ),
    GovernanceDimension(
        id="organizational",
        name="Organizational Governance",
        description=(
            "Examines institutional arrangements: accountability, ownership, roles, "
            "procurement, and assignment of AI-related risk."
        ),
        criteria=(
            GovernanceCriterion(
                id="accountability",
                statement="Accountability structures link AI outcomes to public service responsibilities.",
                suggested_evidence=(
                    "Governance charter excerpt, committee terms of reference, and service owner nomination."
                ),
                risk_if_missing=(
                    "Responsibility may be diffused between IT vendors and line managers after failures."
                ),
            ),
            GovernanceCriterion(
                id="ownership",
                statement="Ownership assigns sustained stewardship for each on-premise LLM system.",
                suggested_evidence=(
                    "RACI or ownership matrix, service catalogue entries, and escalation contacts."
                ),
                risk_if_missing=(
                    "Systems may become orphaned when staff rotate or projects end."
                ),
            ),
            GovernanceCriterion(
                id="role_definition",
                statement="Role definitions cover legal, technical, data, and operational functions.",
                suggested_evidence=(
                    "Role descriptions, training plans, and interdisciplinary workshop minutes."
                ),
                risk_if_missing=(
                    "Critical safeguards may be assumed rather than assigned to named roles."
                ),
            ),
            GovernanceCriterion(
                id="procurement_governance",
                statement="Procurement governance addresses AI components, support, and exit.",
                suggested_evidence=(
                    "Contract clauses on model updates, SLAs, audit rights, and transition assistance."
                ),
                risk_if_missing=(
                    "Vendor lock-in and unclear exit paths can constrain future sovereignty choices."
                ),
            ),
            GovernanceCriterion(
                id="risk_ownership",
                statement="Risk ownership assigns identification, treatment, and reporting of AI risks.",
                suggested_evidence=(
                    "Risk register entries, risk appetite statement, and periodic review cadence."
                ),
                risk_if_missing=(
                    "Risks may be tracked only as technical issues without public-value framing."
                ),
            ),
        ),
    ),
    GovernanceDimension(
        id="operational",
        name="Operational Management",
        description=(
            "Addresses day-to-day operation of local LLM services: monitoring, incidents, "
            "human oversight, documentation, and lifecycle management."
        ),
        criteria=(
            GovernanceCriterion(
                id="monitoring",
                statement="Monitoring tracks performance, safety signals, and resource use.",
                suggested_evidence=(
                    "Monitoring dashboards, alert thresholds, and sample review reports."
                ),
                risk_if_missing=(
                    "Degradation, abuse, or cost overruns may persist without timely detection."
                ),
            ),
            GovernanceCriterion(
                id="incident_response",
                statement="Incident response covers harmful outputs, outages, and security events.",
                suggested_evidence=(
                    "Incident response plan, tabletop exercise records, and post-incident review template."
                ),
                risk_if_missing=(
                    "Slow or inconsistent response can amplify harm to citizens and staff."
                ),
            ),
            GovernanceCriterion(
                id="human_oversight",
                statement="Human oversight is defined where outputs influence decisions or communications.",
                suggested_evidence=(
                    "Oversight procedures, sampling protocols, and appeal or correction pathways."
                ),
                risk_if_missing=(
                    "Automation bias and unreviewed errors may reach citizens or caseworkers."
                ),
            ),
            GovernanceCriterion(
                id="documentation",
                statement="Documentation covers prompts, configurations, known limitations, and user guidance.",
                suggested_evidence=(
                    "System documentation set, prompt registry, and operator handbook."
                ),
                risk_if_missing=(
                    "Knowledge loss and inconsistent operation across shifts or sites."
                ),
            ),
            GovernanceCriterion(
                id="lifecycle_management",
                statement="Lifecycle management covers pilot, production, scaling, and decommissioning.",
                suggested_evidence=(
                    "Lifecycle stage gates, decommission checklist, and archival policy."
                ),
                risk_if_missing=(
                    "Experimental systems may remain in de facto production without controls."
                ),
            ),
        ),
    ),
    GovernanceDimension(
        id="strategic_sovereignty",
        name="Strategic Sovereignty",
        description=(
            "Evaluates longer-term control over data, infrastructure, vendors, and maintainability "
            "for on-premise LLM capacity in public sector contexts."
        ),
        criteria=(
            GovernanceCriterion(
                id="vendor_independence",
                statement="Vendor independence reduces reliance on single proprietary stacks.",
                suggested_evidence=(
                    "Alternative supplier analysis, open standards usage, and contingency planning."
                ),
                risk_if_missing=(
                    "Negotiating power and optionality decline as dependencies deepen."
                ),
            ),
            GovernanceCriterion(
                id="data_sovereignty",
                statement="Data sovereignty ensures primary data and models remain under institutional control.",
                suggested_evidence=(
                    "Data residency statement, on-prem storage design, and third-party access restrictions."
                ),
                risk_if_missing=(
                    "Sensitive public sector data may be exposed to external inference or training pipelines."
                ),
            ),
            GovernanceCriterion(
                id="infrastructure_control",
                statement="Infrastructure control covers hosting, networking, and capacity planning.",
                suggested_evidence=(
                    "Infrastructure ownership model, capacity plan, and disaster recovery design."
                ),
                risk_if_missing=(
                    "Service continuity and security depend on opaque external platforms."
                ),
            ),
            GovernanceCriterion(
                id="portability",
                statement="Portability supports migration of models, prompts, and evaluation assets.",
                suggested_evidence=(
                    "Export formats, container images, and migration test results."
                ),
                risk_if_missing=(
                    "Switching costs may block adoption of improved local models or policies."
                ),
            ),
            GovernanceCriterion(
                id="maintainability",
                statement="Long-term maintainability plans staffing, upgrades, and technical debt management.",
                suggested_evidence=(
                    "Roadmap, budget lines, and skills development plan for sustaining on-prem AI."
                ),
                risk_if_missing=(
                    "Systems may become unsupported while still handling citizen-facing workloads."
                ),
            ),
        ),
    ),
)


def get_dimension(dimension_id: str) -> GovernanceDimension:
    """Return a dimension by id or raise KeyError."""
    for dimension in GOVERNANCE_DIMENSIONS:
        if dimension.id == dimension_id:
            return dimension
    raise KeyError(f"Unknown governance dimension: {dimension_id!r}")


def get_criterion(dimension_id: str, criterion_id: str) -> GovernanceCriterion:
    """Return a criterion within a dimension or raise KeyError."""
    dimension = get_dimension(dimension_id)
    for criterion in dimension.criteria:
        if criterion.id == criterion_id:
            return criterion
    raise KeyError(
        f"Unknown criterion {criterion_id!r} in dimension {dimension_id!r}"
    )
