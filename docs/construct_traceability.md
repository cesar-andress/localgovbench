> **Status: LEGACY — v0.1.0**  
> Retained for provenance of the historical Governance Readiness Benchmark / v0.1 instrument.  
> **Do not use this document as the current analytical specification.**  
> **Active framework:** Disclosure Functions v1 — see [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and the root [`README.md`](../README.md).

# Construct Traceability — LocalGovBench v0.1

**Purpose:** Demonstrate that every **LocalGovBench v0.1 criterion** (25 checklist indicators) is traceable to established governance concepts in the literature and EU policy instruments.

**Machine-readable mapping:** [data/traceability/indicator_mapping.csv](../data/traceability/indicator_mapping.csv)  
**Validation:** `python scripts/validate_traceability.py` → [reports/traceability_report.md](../reports/traceability_report.md)

**Scope:** LocalGovBench v0.1 only (five dimensions, 25 criteria). The separate GRB 54-indicator experiment maintains its own specification and is not covered here.

---

## Source frameworks

| Framework | Literature / policy basis | Traceability role |
|-----------|---------------------------|-------------------|
| **ART** | Accountability, Responsibility, Transparency (public-sector and algorithmic governance literature) | Normative backbone for institutional duties |
| **Meaningful Human Control** | Human-in / on / over the loop (automation and AI ethics) | Operational control over LLM outputs |
| **EU Trustworthy AI** | EU High-Level Expert Group requirements; ALTAI self-assessment list | Seven trustworthy AI dimensions |
| **AI Act governance themes** | Regulation (EU) 2024/1689 deployer-oriented themes (indicative) | Links criteria to commonly cited governance duties |
| **Mittelstadt et al.** | Four ethical risk categories in sociotechnical systems | Where applicable — inconclusive risk, misguided agency, unfair outcomes |

Mappings are **inductive and indicative** for manuscript methods sections. They support **construct traceability** claims; they do **not** replace content validity expert review ([validation_protocol.md](validation_protocol.md)).

---

## Coverage summary

| Dimension | Indicators | Mapping rows |
|-----------|------------|--------------|
| Legal and Regulatory Compliance | 5 | 18 |
| Technical and Security Readiness | 5 | 17 |
| Organizational Governance | 5 | 17 |
| Operational Management | 5 | 17 |
| Strategic Sovereignty | 5 | 17 |
| **Total** | **25** | **86** |

Every indicator has **at least one** literature source; **no orphan** indicator ids; **all five dimensions** are represented in the mapping file.

---

## Indicator traceability tables

Rationales for each row are in the CSV. Below: compact matrix per indicator.

### Legal and Regulatory Compliance

#### `legal_regulatory_gdpr_readiness`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Demonstrate processing accountability | ART | Accountability |
| Lawful and fair processing | EU Trustworthy AI | Privacy and data governance |
| Records and DPIA documentation | AI Act | Risk management and documentation |
| Prevent opaque data use | Mittelstadt et al. | Inconclusive risk |

#### `legal_regulatory_ai_act_alignment`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Align deployer obligations with use case | ART | Responsibility |
| Trustworthy design and deployment | EU Trustworthy AI | Technical robustness and safety |
| Risk-based governance | AI Act | Risk management |

#### `legal_regulatory_data_retention`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Limit storage of prompts and logs | ART | Accountability |
| Data minimisation | EU Trustworthy AI | Privacy and data governance |
| Storage limitation | AI Act | Data governance |
| Reduce harm from stale personal data | Mittelstadt et al. | Unfair outcomes |

#### `legal_regulatory_lawful_basis`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Document purpose and legal basis | ART | Accountability |
| Lawful processing | EU Trustworthy AI | Privacy and data governance |
| Lawfulness of training and inference data | AI Act | Data governance |

#### `legal_regulatory_cross_border_avoidance`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Control data location and egress | ART | Responsibility |
| Resilience and control | EU Trustworthy AI | Technical robustness and safety |
| Sovereign hosting | AI Act | Data governance |
| Avoid hidden external agency | Mittelstadt et al. | Misguided agency |

### Technical and Security Readiness

#### `technical_security_local_architecture`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Document end-to-end deployment | ART | Transparency |
| Technical robustness | EU Trustworthy AI | Technical robustness and safety |
| Technical documentation | AI Act | Documentation and record-keeping |
| Reduce opaque dependencies | Mittelstadt et al. | Inconclusive risk |

#### `technical_security_access_control`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Enforce least privilege | ART | Responsibility |
| Security and control | EU Trustworthy AI | Technical robustness and safety |
| Cybersecurity governance | AI Act | Risk management |

#### `technical_security_logging`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Security and accountability logging | ART | Accountability |
| Traceability of operations | EU Trustworthy AI | Transparency |
| Monitoring and logging | AI Act | Post-market monitoring |

#### `technical_security_auditability`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Immutable audit trails | ART | Transparency |
| Traceability | EU Trustworthy AI | Transparency |
| Record-keeping | AI Act | Documentation and record-keeping |

#### `technical_security_model_updates`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Controlled model change | ART | Responsibility |
| Robustness over lifecycle | EU Trustworthy AI | Technical robustness and safety |
| Risk management of changes | AI Act | Risk management |
| Prevent unreviewed capability shifts | Mittelstadt et al. | Inconclusive risk |

### Organizational Governance

#### `organizational_accountability`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Link AI outcomes to public duties | ART | Accountability |
| Organisational governance | EU Trustworthy AI | Human agency and oversight |
| Governance structure | AI Act | Risk management |

#### `organizational_ownership`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Sustained service ownership | ART | Responsibility |
| Clear roles | EU Trustworthy AI | Human agency and oversight |
| Governance roles | AI Act | Risk management |

#### `organizational_role_definition`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Interdisciplinary roles | ART | Responsibility |
| Competence and training | EU Trustworthy AI | Human agency and oversight |
| Organisational measures | AI Act | Risk management |

#### `organizational_procurement_governance`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Contractual governance of vendors | ART | Responsibility |
| Diversity and fairness in supply chain | EU Trustworthy AI | Diversity, non-discrimination and fairness |
| Supply chain governance | AI Act | Risk management |
| Avoid lock-in harms | Mittelstadt et al. | Unfair outcomes |

#### `organizational_risk_ownership`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Institutional risk register | ART | Accountability |
| Risk-based approach | EU Trustworthy AI | Technical robustness and safety |
| Risk management system | AI Act | Risk management |
| Surface structural harms | Mittelstadt et al. | Inconclusive risk |

### Operational Management

#### `operational_monitoring`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Operational performance and safety monitoring | ART | Accountability |
| Reliability monitoring | EU Trustworthy AI | Technical robustness and safety |
| Post-market monitoring | AI Act | Post-market monitoring |

#### `operational_incident_response`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Respond to harmful outputs and outages | ART | Responsibility |
| Serious incident handling | EU Trustworthy AI | Technical robustness and safety |
| Serious incidents | AI Act | Post-market monitoring |
| Mitigate unfair harm | Mittelstadt et al. | Unfair outcomes |

#### `operational_human_oversight`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Human review of consequential outputs | ART | Responsibility |
| Meaningful human intervention | Meaningful Human Control | Human-in-the-loop / on-the-loop |
| Human oversight | EU Trustworthy AI | Human agency and oversight |
| Human oversight measures | AI Act | Human oversight |
| Counter automation bias | Mittelstadt et al. | Misguided agency |

#### `operational_documentation`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Maintain prompts and limitations | ART | Transparency |
| Explainability and communication | EU Trustworthy AI | Transparency |
| Instructions for use | AI Act | Transparency |

#### `operational_lifecycle_management`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Stage-gate pilot to decommission | ART | Accountability |
| Lifecycle governance | EU Trustworthy AI | Technical robustness and safety |
| Lifecycle risk management | AI Act | Risk management |

### Strategic Sovereignty

#### `strategic_sovereignty_vendor_independence`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Reduce single-vendor dependence | ART | Responsibility |
| Diversity of supply | EU Trustworthy AI | Diversity, non-discrimination and fairness |
| Supply chain resilience | AI Act | Risk management |
| Avoid coercive lock-in | Mittelstadt et al. | Unfair outcomes |

#### `strategic_sovereignty_data_sovereignty`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Institutional control of data and models | ART | Accountability |
| Privacy and data governance | EU Trustworthy AI | Privacy and data governance |
| Data governance | AI Act | Data governance |

#### `strategic_sovereignty_infrastructure_control`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Own hosting and capacity | ART | Responsibility |
| Resilience | EU Trustworthy AI | Technical robustness and safety |
| Operational resilience | AI Act | Risk management |

#### `strategic_sovereignty_portability`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Migrate models and prompts | ART | Transparency |
| Reversibility and contestability | EU Trustworthy AI | Human agency and oversight |
| Interoperability | AI Act | Risk management |

#### `strategic_sovereignty_maintainability`

| Governance requirement | Source | Concept |
|------------------------|--------|---------|
| Sustain staffing and upgrades | ART | Responsibility |
| Long-term societal wellbeing | EU Trustworthy AI | Societal and environmental wellbeing |
| Lifecycle resource planning | AI Act | Risk management |

---

## Maintenance

1. Edit mappings in `localgovbench/traceability.py` (canonical source).
2. Regenerate CSV and report: `python scripts/validate_traceability.py`.
3. Update this document if indicator statements change in a future instrument version.

---

## Limitations

- Traceability ≠ empirical content validity or legal compliance.
- AI Act themes are **governance-oriented** and **indicative** (see [ai_act_mapping.md](ai_act_mapping.md)).
- Mittelstadt categories apply **where relevant**; not every indicator maps to all four risks.
- Expert panel may consolidate or split criteria in v0.2+; remapping required after instrument revision.

---

*LocalGovBench v0.1 construct traceability — research documentation*
