"""Construct traceability for LocalGovBench v0.1 checklist indicators."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from localgovbench.framework.checklist import build_checklist
from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS

CSV_COLUMNS: tuple[str, ...] = (
    "indicator_id",
    "dimension",
    "governance_requirement",
    "source_framework",
    "source_concept",
    "rationale",
)

DIMENSION_NAMES: dict[str, str] = {d.id: d.name for d in GOVERNANCE_DIMENSIONS}


@dataclass(frozen=True, slots=True)
class TraceabilityRow:
    indicator_id: str
    dimension: str
    governance_requirement: str
    source_framework: str
    source_concept: str
    rationale: str

    def as_dict(self) -> dict[str, str]:
        return {
            "indicator_id": self.indicator_id,
            "dimension": self.dimension,
            "governance_requirement": self.governance_requirement,
            "source_framework": self.source_framework,
            "source_concept": self.source_concept,
            "rationale": self.rationale,
        }


def expected_indicator_ids() -> frozenset[str]:
    """All v0.1 checklist indicator ids (25 criteria)."""
    return frozenset(item.id for item in build_checklist())


def expected_dimension_ids() -> frozenset[str]:
    return frozenset(d.id for d in GOVERNANCE_DIMENSIONS)


def _row(
    indicator_id: str,
    dimension_id: str,
    requirement: str,
    framework: str,
    concept: str,
    rationale: str,
) -> TraceabilityRow:
    return TraceabilityRow(
        indicator_id=indicator_id,
        dimension=DIMENSION_NAMES[dimension_id],
        governance_requirement=requirement,
        source_framework=framework,
        source_concept=concept,
        rationale=rationale,
    )


def build_traceability_rows() -> tuple[TraceabilityRow, ...]:
    """Canonical construct traceability mappings for all 25 indicators."""
    rows: list[TraceabilityRow] = []

    def extend(indicator_id: str, dimension_id: str, mappings: tuple[tuple[str, str, str, str], ...]) -> None:
        for requirement, framework, concept, rationale in mappings:
            rows.append(_row(indicator_id, dimension_id, requirement, framework, concept, rationale))

    # --- legal_regulatory ---
    extend(
        "legal_regulatory_gdpr_readiness",
        "legal_regulatory",
        (
            ("Demonstrate processing accountability", "ART", "Accountability",
             "GDPR accountability principle requires demonstrable compliance for training, inference, and logs."),
            ("Lawful and fair processing", "EU Trustworthy AI", "Privacy and data governance",
             "HLEG trustworthy AI list emphasises data governance alongside fundamental rights."),
            ("Records and DPIA documentation", "AI Act", "Risk management and documentation",
             "Deployer documentation duties intersect with governance records for data-intensive LLM systems."),
            ("Prevent opaque data use", "Mittelstadt et al.", "Inconclusive risk",
             "Undocumented flows obscure harms analogous to informational inconclusiveness in socio-technical systems."),
        ),
    )
    extend(
        "legal_regulatory_ai_act_alignment",
        "legal_regulatory",
        (
            ("Align deployer obligations with use case", "ART", "Responsibility",
             "Assigns institutional responsibility for classifying and governing municipal LLM deployments."),
            ("Trustworthy design and deployment", "EU Trustworthy AI", "Technical robustness and safety",
             "ALTAI prompts assessment of safety and robustness before operational reliance."),
            ("Risk-based governance", "AI Act", "Risk management",
             "AI Act risk management expectations inform internal classification and monitoring design."),
        ),
    )
    extend(
        "legal_regulatory_data_retention",
        "legal_regulatory",
        (
            ("Limit storage of prompts and logs", "ART", "Accountability",
             "Retention rules make processing demonstrable and bounded over time."),
            ("Data minimisation", "EU Trustworthy AI", "Privacy and data governance",
             "Trustworthy AI requires proportionate data use across the lifecycle."),
            ("Storage limitation", "AI Act", "Data governance",
             "Governance of logs and embeddings supports post-market monitoring without excess retention."),
            ("Reduce harm from stale personal data", "Mittelstadt et al.", "Unfair outcomes",
             "Excessive retention increases risk of discriminatory or harmful reuse of interaction data."),
        ),
    )
    extend(
        "legal_regulatory_lawful_basis",
        "legal_regulatory",
        (
            ("Document purpose and legal basis", "ART", "Accountability",
             "Purpose limitation and lawful basis are core accountability artefacts under GDPR."),
            ("Lawful processing", "EU Trustworthy AI", "Privacy and data governance",
             "HLEG links lawful processing to trustworthy municipal AI."),
            ("Lawfulness of training and inference data", "AI Act", "Data governance",
             "Deployer governance must trace datasets used in local LLM operations."),
        ),
    )
    extend(
        "legal_regulatory_cross_border_avoidance",
        "legal_regulatory",
        (
            ("Control data location and egress", "ART", "Responsibility",
             "Institutional responsibility for sovereignty claims over on-premise workloads."),
            ("Resilience and control", "EU Trustworthy AI", "Technical robustness and safety",
             "Operational control supports resilience when external dependencies are limited."),
            ("Sovereign hosting", "AI Act", "Data governance",
             "Data governance for deployers includes knowing where inference and logs reside."),
            ("Avoid hidden external agency", "Mittelstadt et al.", "Misguided agency",
             "Covert cloud egress can misattribute decisions to local authority control."),
        ),
    )

    # --- technical_security ---
    extend(
        "technical_security_local_architecture",
        "technical_security",
        (
            ("Document end-to-end deployment", "ART", "Transparency",
             "Architecture transparency enables oversight of local LLM components."),
            ("Technical robustness", "EU Trustworthy AI", "Technical robustness and safety",
             "HLEG robustness requirement applies to system design documentation."),
            ("Technical documentation", "AI Act", "Documentation and record-keeping",
             "Deployer technical documentation theme for traceable system descriptions."),
            ("Reduce opaque dependencies", "Mittelstadt et al.", "Inconclusive risk",
             "Opaque stacks create inconclusive risk assessment for citizens and auditors."),
        ),
    )
    extend(
        "technical_security_access_control",
        "technical_security",
        (
            ("Enforce least privilege", "ART", "Responsibility",
             "Assigns responsibility for access decisions affecting model and data misuse."),
            ("Security and control", "EU Trustworthy AI", "Technical robustness and safety",
             "Access control is a baseline trustworthy AI security practice."),
            ("Cybersecurity governance", "AI Act", "Risk management",
             "Security measures form part of deployer risk management for AI systems."),
        ),
    )
    extend(
        "technical_security_logging",
        "technical_security",
        (
            ("Security and accountability logging", "ART", "Accountability",
             "Logs support ex-post accountability without unnecessary personal data."),
            ("Traceability of operations", "EU Trustworthy AI", "Transparency",
             "Operational transparency for auditors and oversight bodies."),
            ("Monitoring and logging", "AI Act", "Post-market monitoring",
             "Logging practices underpin monitoring of system behaviour over time."),
        ),
    )
    extend(
        "technical_security_auditability",
        "technical_security",
        (
            ("Immutable audit trails", "ART", "Transparency",
             "Auditability makes configuration and inference changes visible."),
            ("Traceability", "EU Trustworthy AI", "Transparency",
             "Trustworthy AI transparency includes traceable changes."),
            ("Record-keeping", "AI Act", "Documentation and record-keeping",
             "Supports reconstructing deployer actions after incidents."),
        ),
    )
    extend(
        "technical_security_model_updates",
        "technical_security",
        (
            ("Controlled model change", "ART", "Responsibility",
             "Named approval paths for updates assign responsibility for model risk."),
            ("Robustness over lifecycle", "EU Trustworthy AI", "Technical robustness and safety",
             "Lifecycle testing aligns with HLEG safety expectations."),
            ("Risk management of changes", "AI Act", "Risk management",
             "Model updates trigger reassessment under deployer risk management."),
            ("Prevent unreviewed capability shifts", "Mittelstadt et al.", "Inconclusive risk",
             "Sudden model changes without review recreate inconclusive risk for users."),
        ),
    )

    # --- organizational ---
    extend(
        "organizational_accountability",
        "organizational",
        (
            ("Link AI outcomes to public duties", "ART", "Accountability",
             "Core ART construct operationalised for municipal LLM programmes."),
            ("Organisational governance", "EU Trustworthy AI", "Human agency and oversight",
             "Institutional governance enables human agency at organisational level."),
            ("Governance structure", "AI Act", "Risk management",
             "Accountability structures support AI Act governance of deployer duties."),
        ),
    )
    extend(
        "organizational_ownership",
        "organizational",
        (
            ("Sustained service ownership", "ART", "Responsibility",
             "Ownership assigns ongoing responsibility beyond project phases."),
            ("Clear roles", "EU Trustworthy AI", "Human agency and oversight",
             "Ownership clarifies who exercises oversight on behalf of the public."),
            ("Governance roles", "AI Act", "Risk management",
             "Risk owners identified for deployer obligations."),
        ),
    )
    extend(
        "organizational_role_definition",
        "organizational",
        (
            ("Interdisciplinary roles", "ART", "Responsibility",
             "Defines who is responsible for legal, technical, and operational safeguards."),
            ("Competence and training", "EU Trustworthy AI", "Human agency and oversight",
             "Role clarity supports meaningful staff agency in AI operations."),
            ("Organisational measures", "AI Act", "Risk management",
             "Human resources measures in risk management systems."),
        ),
    )
    extend(
        "organizational_procurement_governance",
        "organizational",
        (
            ("Contractual governance of vendors", "ART", "Responsibility",
             "Procurement assigns responsibility for vendor performance and exit."),
            ("Diversity and fairness in supply chain", "EU Trustworthy AI", "Diversity, non-discrimination and fairness",
             "Fair procurement reduces biased or opaque vendor dependencies."),
            ("Supply chain governance", "AI Act", "Risk management",
             "Governance of third-party components in deployer risk programmes."),
            ("Avoid lock-in harms", "Mittelstadt et al.", "Unfair outcomes",
             "Lock-in can unfairly limit future municipal choices and public value."),
        ),
    )
    extend(
        "organizational_risk_ownership",
        "organizational",
        (
            ("Institutional risk register", "ART", "Accountability",
             "Risk ownership makes AI risks accountable to governance bodies."),
            ("Risk-based approach", "EU Trustworthy AI", "Technical robustness and safety",
             "HLEG expects proportionate risk identification and mitigation."),
            ("Risk management system", "AI Act", "Risk management",
             "Direct mapping to AI Act risk management theme."),
            ("Surface structural harms", "Mittelstadt et al.", "Inconclusive risk",
             "Unowned risks remain inconclusive for affected communities."),
        ),
    )

    # --- operational ---
    extend(
        "operational_monitoring",
        "operational",
        (
            ("Operational performance and safety monitoring", "ART", "Accountability",
             "Monitoring enables accountable response to degradation or misuse."),
            ("Reliability monitoring", "EU Trustworthy AI", "Technical robustness and safety",
             "Continuous monitoring supports robustness claims."),
            ("Post-market monitoring", "AI Act", "Post-market monitoring",
             "Operational metrics feed deployer monitoring duties."),
        ),
    )
    extend(
        "operational_incident_response",
        "operational",
        (
            ("Respond to harmful outputs and outages", "ART", "Responsibility",
             "Incident response assigns responsibility for remediation."),
            ("Serious incident handling", "EU Trustworthy AI", "Technical robustness and safety",
             "Preparedness aligns with safety and robustness expectations."),
            ("Serious incidents", "AI Act", "Post-market monitoring",
             "Reporting and response linked to post-market monitoring themes."),
            ("Mitigate unfair harm", "Mittelstadt et al.", "Unfair outcomes",
             "Slow response can allow unfair harms to citizens to accumulate."),
        ),
    )
    extend(
        "operational_human_oversight",
        "operational",
        (
            ("Human review of consequential outputs", "ART", "Responsibility",
             "Oversight assigns humans responsibility for consequential decisions."),
            ("Meaningful human intervention", "Meaningful Human Control", "Human-in-the-loop / on-the-loop",
             "Criterion operationalises meaningful human control for local LLM outputs."),
            ("Human oversight", "EU Trustworthy AI", "Human agency and oversight",
             "Direct HLEG requirement for human agency and oversight."),
            ("Human oversight measures", "AI Act", "Human oversight",
             "Maps to AI Act human oversight obligations for deployers."),
            ("Counter automation bias", "Mittelstadt et al.", "Misguided agency",
             "Absent oversight risks misguided agency where users over-trust automation."),
        ),
    )
    extend(
        "operational_documentation",
        "operational",
        (
            ("Maintain prompts and limitations", "ART", "Transparency",
             "Documentation makes system behaviour transparent to operators."),
            ("Explainability and communication", "EU Trustworthy AI", "Transparency",
             "Internal transparency supports trustworthy communication."),
            ("Instructions for use", "AI Act", "Transparency",
             "Operator documentation parallels transparency to deployers and staff."),
        ),
    )
    extend(
        "operational_lifecycle_management",
        "operational",
        (
            ("Stage-gate pilot to decommission", "ART", "Accountability",
             "Lifecycle gates maintain accountability as systems mature."),
            ("Lifecycle governance", "EU Trustworthy AI", "Technical robustness and safety",
             "Controlled transitions reduce safety gaps."),
            ("Lifecycle risk management", "AI Act", "Risk management",
             "Risk reassessment across lifecycle stages."),
        ),
    )

    # --- strategic_sovereignty ---
    extend(
        "strategic_sovereignty_vendor_independence",
        "strategic_sovereignty",
        (
            ("Reduce single-vendor dependence", "ART", "Responsibility",
             "Strategic responsibility for long-term optionality."),
            ("Diversity of supply", "EU Trustworthy AI", "Diversity, non-discrimination and fairness",
             "Vendor diversity mitigates structural dependency risks."),
            ("Supply chain resilience", "AI Act", "Risk management",
             "Third-party risk in deployer governance."),
            ("Avoid coercive lock-in", "Mittelstadt et al.", "Unfair outcomes",
             "Dependency can produce unfair bargaining outcomes for municipalities."),
        ),
    )
    extend(
        "strategic_sovereignty_data_sovereignty",
        "strategic_sovereignty",
        (
            ("Institutional control of data and models", "ART", "Accountability",
             "Sovereignty claims require demonstrable control over data assets."),
            ("Privacy and data governance", "EU Trustworthy AI", "Privacy and data governance",
             "Data sovereignty supports privacy-by-design for local LLMs."),
            ("Data governance", "AI Act", "Data governance",
             "Aligns with deployer data governance expectations."),
        ),
    )
    extend(
        "strategic_sovereignty_infrastructure_control",
        "strategic_sovereignty",
        (
            ("Own hosting and capacity", "ART", "Responsibility",
             "Infrastructure control is a strategic responsibility for continuity."),
            ("Resilience", "EU Trustworthy AI", "Technical robustness and safety",
             "Resilient infrastructure underpins trustworthy operation."),
            ("Operational resilience", "AI Act", "Risk management",
             "Business continuity in risk management programmes."),
        ),
    )
    extend(
        "strategic_sovereignty_portability",
        "strategic_sovereignty",
        (
            ("Migrate models and prompts", "ART", "Transparency",
             "Portability makes technical commitments auditable and reversible."),
            ("Reversibility and contestability", "EU Trustworthy AI", "Human agency and oversight",
             "Portability supports contestability when systems fail citizens."),
            ("Interoperability", "AI Act", "Risk management",
             "Reduces dependency risk in technical governance."),
        ),
    )
    extend(
        "strategic_sovereignty_maintainability",
        "strategic_sovereignty",
        (
            ("Sustain staffing and upgrades", "ART", "Responsibility",
             "Long-term maintainability is a governance responsibility, not only IT."),
            ("Long-term societal wellbeing", "EU Trustworthy AI", "Societal and environmental wellbeing",
             "Sustainable operation aligns with HLEG societal wellbeing dimension."),
            ("Lifecycle resource planning", "AI Act", "Risk management",
             "Resource planning for ongoing compliance and monitoring."),
        ),
    )

    return tuple(rows)


@dataclass
class TraceabilityValidationResult:
    ok: bool
    expected_indicators: int
    mapped_indicators: int
    orphan_indicator_ids: tuple[str, ...]
    missing_indicator_ids: tuple[str, ...]
    missing_dimension_ids: tuple[str, ...]
    row_count: int


def load_mapping_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(CSV_COLUMNS):
            raise ValueError(
                f"CSV columns must be {list(CSV_COLUMNS)}, got {reader.fieldnames}"
            )
        return list(reader)


def validate_traceability(
    rows: list[dict[str, str]],
    *,
    expected_ids: frozenset[str] | None = None,
    expected_dims: frozenset[str] | None = None,
) -> TraceabilityValidationResult:
    """Validate mapping coverage and detect orphan indicators."""
    expected_ids = expected_ids or expected_indicator_ids()
    expected_dims = expected_dims or expected_dimension_ids()
    dim_name_to_id = {name: did for did, name in DIMENSION_NAMES.items()}

    by_indicator: dict[str, int] = defaultdict(int)
    dimensions_seen: set[str] = set()
    orphan: list[str] = []

    for row in rows:
        ind = row["indicator_id"].strip()
        dim_label = row["dimension"].strip()
        if ind not in expected_ids:
            orphan.append(ind)
        else:
            by_indicator[ind] += 1
            for did, dname in DIMENSION_NAMES.items():
                if dname == dim_label:
                    dimensions_seen.add(did)
                    break
            else:
                if dim_label in dim_name_to_id:
                    dimensions_seen.add(dim_name_to_id[dim_label])
        if not row.get("source_framework", "").strip():
            raise ValueError(f"Row for {ind} missing source_framework")
        if not row.get("source_concept", "").strip():
            raise ValueError(f"Row for {ind} missing source_concept")

    missing = sorted(expected_ids - set(by_indicator))
    missing_dims = sorted(expected_dims - dimensions_seen)
    ok = not missing and not orphan and not missing_dims and all(c > 0 for c in by_indicator.values())

    return TraceabilityValidationResult(
        ok=ok,
        expected_indicators=len(expected_ids),
        mapped_indicators=len(by_indicator),
        orphan_indicator_ids=tuple(sorted(set(orphan))),
        missing_indicator_ids=tuple(missing),
        missing_dimension_ids=tuple(missing_dims),
        row_count=len(rows),
    )


def write_mapping_csv(path: Path, rows: Iterable[TraceabilityRow] | None = None) -> int:
    data = list(rows or build_traceability_rows())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_COLUMNS))
        writer.writeheader()
        for row in data:
            writer.writerow(row.as_dict())
    return len(data)


def render_traceability_report(
    result: TraceabilityValidationResult,
    rows: list[dict[str, str]],
) -> str:
    """Build Markdown traceability validation report."""
    by_framework: dict[str, int] = defaultdict(int)
    by_dimension: dict[str, int] = defaultdict(int)
    for row in rows:
        by_framework[row["source_framework"]] += 1
        by_dimension[row["dimension"]] += 1

    lines = [
        "# Construct Traceability Report",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Expected indicators (v0.1) | {result.expected_indicators} |",
        f"| Indicators with ≥1 mapping | {result.mapped_indicators} |",
        f"| Mapping rows | {result.row_count} |",
        f"| Validation status | {'PASS' if result.ok else 'FAIL'} |",
        "",
    ]
    if result.missing_indicator_ids:
        lines.extend(["## Missing indicators", "", *[f"- `{i}`" for i in result.missing_indicator_ids], ""])
    if result.orphan_indicator_ids:
        lines.extend(["## Orphan indicator ids", "", *[f"- `{i}`" for i in result.orphan_indicator_ids], ""])
    if result.missing_dimension_ids:
        lines.extend(
            ["## Missing dimensions", "", *[f"- `{d}`" for d in result.missing_dimension_ids], ""]
        )

    lines.extend(
        [
            "## Mappings by source framework",
            "",
            "| Source framework | Rows |",
            "|------------------|------|",
        ]
    )
    for framework in sorted(by_framework):
        lines.append(f"| {framework} | {by_framework[framework]} |")

    lines.extend(["", "## Mappings by dimension", "", "| Dimension | Rows |", "|-----------|------|"])
    for dimension in sorted(by_dimension):
        lines.append(f"| {dimension} | {by_dimension[dimension]} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Each LocalGovBench v0.1 criterion is linked to published governance constructs "
            "(ART, meaningful human control, EU Trustworthy AI, AI Act themes, and Mittelstadt "
            "risk categories where applicable). This supports construct traceability claims in "
            "manuscript methods sections; it does not replace empirical content validity testing.",
            "",
            "---",
            "*Generated by `scripts/validate_traceability.py`*",
        ]
    )
    return "\n".join(lines)


def sync_traceability_artifacts(
    *,
    csv_path: Path,
    report_path: Path,
) -> TraceabilityValidationResult:
    """Write CSV, validate, and generate report."""
    write_mapping_csv(csv_path)
    loaded = load_mapping_csv(csv_path)
    result = validate_traceability(loaded)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_traceability_report(result, loaded), encoding="utf-8")
    return result
