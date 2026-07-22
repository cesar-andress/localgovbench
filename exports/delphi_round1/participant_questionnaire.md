# LocalGovBench v0.1 — Delphi Round 1 participant questionnaire

**Framework version:** 0.1  
**Round:** 1  
**Generated:** 2026-06-18  
**Criteria:** 25  

Complete one block per criterion. See `participant_instructions.md` for scales.

---

## Legal and Regulatory Compliance (`legal_regulatory`)

### 1. `legal_regulatory_gdpr_readiness`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: GDPR readiness for training, inference, and logging data flows.

**Criterion description:** GDPR readiness for training, inference, and logging data flows.

**Documentation hint (for field study context only; not rated in Round 1):**  
Records of processing, privacy notices, DPIA where applicable, and DPO consultation notes.

**Risk if missing (indicative):**  
Unlawful or undocumented processing; difficulty demonstrating accountability to supervisory authorities.

**Traceability references:**

- **ART** — Accountability: Demonstrate processing accountability. GDPR accountability principle requires demonstrable compliance for training, inference, and logs.
- **EU Trustworthy AI** — Privacy and data governance: Lawful and fair processing. HLEG trustworthy AI list emphasises data governance alongside fundamental rights.
- **AI Act** — Risk management and documentation: Records and DPIA documentation. Deployer documentation duties intersect with governance records for data-intensive LLM systems.
- **Mittelstadt et al.** — Inconclusive risk: Prevent opaque data use. Undocumented flows obscure harms analogous to informational inconclusiveness in socio-technical systems.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 2. `legal_regulatory_ai_act_alignment`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: EU AI Act alignment documented for the deployer role and use case.

**Criterion description:** EU AI Act alignment documented for the deployer role and use case.

**Documentation hint (for field study context only; not rated in Round 1):**  
Use-case classification memo, risk management notes, human oversight description, and technical documentation references.

**Risk if missing (indicative):**  
Gaps in deployer obligations and post-deployment monitoring may go unidentified until external audit or incident.

**Traceability references:**

- **ART** — Responsibility: Align deployer obligations with use case. Assigns institutional responsibility for classifying and governing municipal LLM deployments.
- **EU Trustworthy AI** — Technical robustness and safety: Trustworthy design and deployment. ALTAI prompts assessment of safety and robustness before operational reliance.
- **AI Act** — Risk management: Risk-based governance. AI Act risk management expectations inform internal classification and monitoring design.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 3. `legal_regulatory_data_retention`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Data retention and deletion rules defined for prompts, logs, and embeddings.

**Criterion description:** Data retention and deletion rules defined for prompts, logs, and embeddings.

**Documentation hint (for field study context only; not rated in Round 1):**  
Retention schedule, automated deletion configuration, and backup handling procedures.

**Risk if missing (indicative):**  
Excessive retention of prompts or logs increases exposure and complicates erasure requests.

**Traceability references:**

- **ART** — Accountability: Limit storage of prompts and logs. Retention rules make processing demonstrable and bounded over time.
- **EU Trustworthy AI** — Privacy and data governance: Data minimisation. Trustworthy AI requires proportionate data use across the lifecycle.
- **AI Act** — Data governance: Storage limitation. Governance of logs and embeddings supports post-market monitoring without excess retention.
- **Mittelstadt et al.** — Unfair outcomes: Reduce harm from stale personal data. Excessive retention increases risk of discriminatory or harmful reuse of interaction data.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 4. `legal_regulatory_lawful_basis`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Lawful basis and purpose limitation recorded for each data category used.

**Criterion description:** Lawful basis and purpose limitation recorded for each data category used.

**Documentation hint (for field study context only; not rated in Round 1):**  
Lawful basis register entries, purpose statements in system design documents, and data minimization checklist.

**Risk if missing (indicative):**  
Processing may lack demonstrable legal grounding; harder to justify secondary use of interaction data.

**Traceability references:**

- **ART** — Accountability: Document purpose and legal basis. Purpose limitation and lawful basis are core accountability artefacts under GDPR.
- **EU Trustworthy AI** — Privacy and data governance: Lawful processing. HLEG links lawful processing to trustworthy municipal AI.
- **AI Act** — Data governance: Lawfulness of training and inference data. Deployer governance must trace datasets used in local LLM operations.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 5. `legal_regulatory_cross_border_avoidance`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Cross-border data transfer avoidance for on-premise workloads.

**Criterion description:** Cross-border data transfer avoidance for on-premise workloads.

**Documentation hint (for field study context only; not rated in Round 1):**  
Architecture diagram showing EU hosting, egress controls, vendor sub-processor list, and network policy excerpts.

**Risk if missing (indicative):**  
Unintended transfers via APIs, telemetry, or cloud-backed components may undermine sovereignty claims.

**Traceability references:**

- **ART** — Responsibility: Control data location and egress. Institutional responsibility for sovereignty claims over on-premise workloads.
- **EU Trustworthy AI** — Technical robustness and safety: Resilience and control. Operational control supports resilience when external dependencies are limited.
- **AI Act** — Data governance: Sovereign hosting. Data governance for deployers includes knowing where inference and logs reside.
- **Mittelstadt et al.** — Misguided agency: Avoid hidden external agency. Covert cloud egress can misattribute decisions to local authority control.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

## Technical and Security Readiness (`technical_security`)

### 6. `technical_security_local_architecture`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Local deployment architecture documented end-to-end.

**Criterion description:** Local deployment architecture documented end-to-end.

**Documentation hint (for field study context only; not rated in Round 1):**  
Architecture diagrams, component inventory, segmentation model, and secrets management approach.

**Risk if missing (indicative):**  
Opaque dependencies complicate incident response and sovereignty review.

**Traceability references:**

- **ART** — Transparency: Document end-to-end deployment. Architecture transparency enables oversight of local LLM components.
- **EU Trustworthy AI** — Technical robustness and safety: Technical robustness. HLEG robustness requirement applies to system design documentation.
- **AI Act** — Documentation and record-keeping: Technical documentation. Deployer technical documentation theme for traceable system descriptions.
- **Mittelstadt et al.** — Inconclusive risk: Reduce opaque dependencies. Opaque stacks create inconclusive risk assessment for citizens and auditors.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 7. `technical_security_access_control`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Access control enforces least privilege for operators and end users.

**Criterion description:** Access control enforces least privilege for operators and end users.

**Documentation hint (for field study context only; not rated in Round 1):**  
IAM role matrix, authentication method description, and periodic access review records.

**Risk if missing (indicative):**  
Over-privileged accounts increase risk of data exfiltration or model misuse.

**Traceability references:**

- **ART** — Responsibility: Enforce least privilege. Assigns responsibility for access decisions affecting model and data misuse.
- **EU Trustworthy AI** — Technical robustness and safety: Security and control. Access control is a baseline trustworthy AI security practice.
- **AI Act** — Risk management: Cybersecurity governance. Security measures form part of deployer risk management for AI systems.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 8. `technical_security_logging`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Logging captures security-relevant and operational events without excess personal data.

**Criterion description:** Logging captures security-relevant and operational events without excess personal data.

**Documentation hint (for field study context only; not rated in Round 1):**  
Logging policy, sample log schemas, and redaction or pseudonymization rules.

**Risk if missing (indicative):**  
Forensics and accountability are weakened after security or safety incidents.

**Traceability references:**

- **ART** — Accountability: Security and accountability logging. Logs support ex-post accountability without unnecessary personal data.
- **EU Trustworthy AI** — Transparency: Traceability of operations. Operational transparency for auditors and oversight bodies.
- **AI Act** — Post-market monitoring: Monitoring and logging. Logging practices underpin monitoring of system behaviour over time.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 9. `technical_security_auditability`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Auditability supports traceability of configuration and inference changes.

**Criterion description:** Auditability supports traceability of configuration and inference changes.

**Documentation hint (for field study context only; not rated in Round 1):**  
Audit trail configuration, change management tickets, and immutable log store references.

**Risk if missing (indicative):**  
Inability to reconstruct who changed models, prompts, or policies when investigating harm.

**Traceability references:**

- **ART** — Transparency: Immutable audit trails. Auditability makes configuration and inference changes visible.
- **EU Trustworthy AI** — Transparency: Traceability. Trustworthy AI transparency includes traceable changes.
- **AI Act** — Documentation and record-keeping: Record-keeping. Supports reconstructing deployer actions after incidents.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 10. `technical_security_model_updates`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Model update management defines testing, approval, and rollback.

**Criterion description:** Model update management defines testing, approval, and rollback.

**Documentation hint (for field study context only; not rated in Round 1):**  
Model change procedure, validation results, version registry, and rollback runbook.

**Risk if missing (indicative):**  
Uncontrolled updates may introduce drift, bias, or safety regressions without notice.

**Traceability references:**

- **ART** — Responsibility: Controlled model change. Named approval paths for updates assign responsibility for model risk.
- **EU Trustworthy AI** — Technical robustness and safety: Robustness over lifecycle. Lifecycle testing aligns with HLEG safety expectations.
- **AI Act** — Risk management: Risk management of changes. Model updates trigger reassessment under deployer risk management.
- **Mittelstadt et al.** — Inconclusive risk: Prevent unreviewed capability shifts. Sudden model changes without review recreate inconclusive risk for users.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

## Organizational Governance (`organizational`)

### 11. `organizational_accountability`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Accountability structures link AI outcomes to public service responsibilities.

**Criterion description:** Accountability structures link AI outcomes to public service responsibilities.

**Documentation hint (for field study context only; not rated in Round 1):**  
Governance charter excerpt, committee terms of reference, and service owner nomination.

**Risk if missing (indicative):**  
Responsibility may be diffused between IT vendors and line managers after failures.

**Traceability references:**

- **ART** — Accountability: Link AI outcomes to public duties. Core ART construct operationalised for municipal LLM programmes.
- **EU Trustworthy AI** — Human agency and oversight: Organisational governance. Institutional governance enables human agency at organisational level.
- **AI Act** — Risk management: Governance structure. Accountability structures support AI Act governance of deployer duties.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 12. `organizational_ownership`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Ownership assigns sustained stewardship for each on-premise LLM system.

**Criterion description:** Ownership assigns sustained stewardship for each on-premise LLM system.

**Documentation hint (for field study context only; not rated in Round 1):**  
RACI or ownership matrix, service catalogue entries, and escalation contacts.

**Risk if missing (indicative):**  
Systems may become orphaned when staff rotate or projects end.

**Traceability references:**

- **ART** — Responsibility: Sustained service ownership. Ownership assigns ongoing responsibility beyond project phases.
- **EU Trustworthy AI** — Human agency and oversight: Clear roles. Ownership clarifies who exercises oversight on behalf of the public.
- **AI Act** — Risk management: Governance roles. Risk owners identified for deployer obligations.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 13. `organizational_role_definition`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Role definitions cover legal, technical, data, and operational functions.

**Criterion description:** Role definitions cover legal, technical, data, and operational functions.

**Documentation hint (for field study context only; not rated in Round 1):**  
Role descriptions, training plans, and interdisciplinary workshop minutes.

**Risk if missing (indicative):**  
Critical safeguards may be assumed rather than assigned to named roles.

**Traceability references:**

- **ART** — Responsibility: Interdisciplinary roles. Defines who is responsible for legal, technical, and operational safeguards.
- **EU Trustworthy AI** — Human agency and oversight: Competence and training. Role clarity supports meaningful staff agency in AI operations.
- **AI Act** — Risk management: Organisational measures. Human resources measures in risk management systems.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 14. `organizational_procurement_governance`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Procurement governance addresses AI components, support, and exit.

**Criterion description:** Procurement governance addresses AI components, support, and exit.

**Documentation hint (for field study context only; not rated in Round 1):**  
Contract clauses on model updates, SLAs, audit rights, and transition assistance.

**Risk if missing (indicative):**  
Vendor lock-in and unclear exit paths can constrain future sovereignty choices.

**Traceability references:**

- **ART** — Responsibility: Contractual governance of vendors. Procurement assigns responsibility for vendor performance and exit.
- **EU Trustworthy AI** — Diversity, non-discrimination and fairness: Diversity and fairness in supply chain. Fair procurement reduces biased or opaque vendor dependencies.
- **AI Act** — Risk management: Supply chain governance. Governance of third-party components in deployer risk programmes.
- **Mittelstadt et al.** — Unfair outcomes: Avoid lock-in harms. Lock-in can unfairly limit future municipal choices and public value.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 15. `organizational_risk_ownership`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Risk ownership assigns identification, treatment, and reporting of AI risks.

**Criterion description:** Risk ownership assigns identification, treatment, and reporting of AI risks.

**Documentation hint (for field study context only; not rated in Round 1):**  
Risk register entries, risk appetite statement, and periodic review cadence.

**Risk if missing (indicative):**  
Risks may be tracked only as technical issues without public-value framing.

**Traceability references:**

- **ART** — Accountability: Institutional risk register. Risk ownership makes AI risks accountable to governance bodies.
- **EU Trustworthy AI** — Technical robustness and safety: Risk-based approach. HLEG expects proportionate risk identification and mitigation.
- **AI Act** — Risk management: Risk management system. Direct mapping to AI Act risk management theme.
- **Mittelstadt et al.** — Inconclusive risk: Surface structural harms. Unowned risks remain inconclusive for affected communities.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

## Operational Management (`operational`)

### 16. `operational_monitoring`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Monitoring tracks performance, safety signals, and resource use.

**Criterion description:** Monitoring tracks performance, safety signals, and resource use.

**Documentation hint (for field study context only; not rated in Round 1):**  
Monitoring dashboards, alert thresholds, and sample review reports.

**Risk if missing (indicative):**  
Degradation, abuse, or cost overruns may persist without timely detection.

**Traceability references:**

- **ART** — Accountability: Operational performance and safety monitoring. Monitoring enables accountable response to degradation or misuse.
- **EU Trustworthy AI** — Technical robustness and safety: Reliability monitoring. Continuous monitoring supports robustness claims.
- **AI Act** — Post-market monitoring: Post-market monitoring. Operational metrics feed deployer monitoring duties.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 17. `operational_incident_response`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Incident response covers harmful outputs, outages, and security events.

**Criterion description:** Incident response covers harmful outputs, outages, and security events.

**Documentation hint (for field study context only; not rated in Round 1):**  
Incident response plan, tabletop exercise records, and post-incident review template.

**Risk if missing (indicative):**  
Slow or inconsistent response can amplify harm to citizens and staff.

**Traceability references:**

- **ART** — Responsibility: Respond to harmful outputs and outages. Incident response assigns responsibility for remediation.
- **EU Trustworthy AI** — Technical robustness and safety: Serious incident handling. Preparedness aligns with safety and robustness expectations.
- **AI Act** — Post-market monitoring: Serious incidents. Reporting and response linked to post-market monitoring themes.
- **Mittelstadt et al.** — Unfair outcomes: Mitigate unfair harm. Slow response can allow unfair harms to citizens to accumulate.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 18. `operational_human_oversight`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Human oversight is defined where outputs influence decisions or communications.

**Criterion description:** Human oversight is defined where outputs influence decisions or communications.

**Documentation hint (for field study context only; not rated in Round 1):**  
Oversight procedures, sampling protocols, and appeal or correction pathways.

**Risk if missing (indicative):**  
Automation bias and unreviewed errors may reach citizens or caseworkers.

**Traceability references:**

- **ART** — Responsibility: Human review of consequential outputs. Oversight assigns humans responsibility for consequential decisions.
- **Meaningful Human Control** — Human-in-the-loop / on-the-loop: Meaningful human intervention. Criterion operationalises meaningful human control for local LLM outputs.
- **EU Trustworthy AI** — Human agency and oversight: Human oversight. Direct HLEG requirement for human agency and oversight.
- **AI Act** — Human oversight: Human oversight measures. Maps to AI Act human oversight obligations for deployers.
- **Mittelstadt et al.** — Misguided agency: Counter automation bias. Absent oversight risks misguided agency where users over-trust automation.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 19. `operational_documentation`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Documentation covers prompts, configurations, known limitations, and user guidance.

**Criterion description:** Documentation covers prompts, configurations, known limitations, and user guidance.

**Documentation hint (for field study context only; not rated in Round 1):**  
System documentation set, prompt registry, and operator handbook.

**Risk if missing (indicative):**  
Knowledge loss and inconsistent operation across shifts or sites.

**Traceability references:**

- **ART** — Transparency: Maintain prompts and limitations. Documentation makes system behaviour transparent to operators.
- **EU Trustworthy AI** — Transparency: Explainability and communication. Internal transparency supports trustworthy communication.
- **AI Act** — Transparency: Instructions for use. Operator documentation parallels transparency to deployers and staff.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 20. `operational_lifecycle_management`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Lifecycle management covers pilot, production, scaling, and decommissioning.

**Criterion description:** Lifecycle management covers pilot, production, scaling, and decommissioning.

**Documentation hint (for field study context only; not rated in Round 1):**  
Lifecycle stage gates, decommission checklist, and archival policy.

**Risk if missing (indicative):**  
Experimental systems may remain in de facto production without controls.

**Traceability references:**

- **ART** — Accountability: Stage-gate pilot to decommission. Lifecycle gates maintain accountability as systems mature.
- **EU Trustworthy AI** — Technical robustness and safety: Lifecycle governance. Controlled transitions reduce safety gaps.
- **AI Act** — Risk management: Lifecycle risk management. Risk reassessment across lifecycle stages.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

## Strategic Sovereignty (`strategic_sovereignty`)

### 21. `strategic_sovereignty_vendor_independence`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Vendor independence reduces reliance on single proprietary stacks.

**Criterion description:** Vendor independence reduces reliance on single proprietary stacks.

**Documentation hint (for field study context only; not rated in Round 1):**  
Alternative supplier analysis, open standards usage, and contingency planning.

**Risk if missing (indicative):**  
Negotiating power and optionality decline as dependencies deepen.

**Traceability references:**

- **ART** — Responsibility: Reduce single-vendor dependence. Strategic responsibility for long-term optionality.
- **EU Trustworthy AI** — Diversity, non-discrimination and fairness: Diversity of supply. Vendor diversity mitigates structural dependency risks.
- **AI Act** — Risk management: Supply chain resilience. Third-party risk in deployer governance.
- **Mittelstadt et al.** — Unfair outcomes: Avoid coercive lock-in. Dependency can produce unfair bargaining outcomes for municipalities.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 22. `strategic_sovereignty_data_sovereignty`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Data sovereignty ensures primary data and models remain under institutional control.

**Criterion description:** Data sovereignty ensures primary data and models remain under institutional control.

**Documentation hint (for field study context only; not rated in Round 1):**  
Data residency statement, on-prem storage design, and third-party access restrictions.

**Risk if missing (indicative):**  
Sensitive public sector data may be exposed to external inference or training pipelines.

**Traceability references:**

- **ART** — Accountability: Institutional control of data and models. Sovereignty claims require demonstrable control over data assets.
- **EU Trustworthy AI** — Privacy and data governance: Privacy and data governance. Data sovereignty supports privacy-by-design for local LLMs.
- **AI Act** — Data governance: Data governance. Aligns with deployer data governance expectations.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 23. `strategic_sovereignty_infrastructure_control`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Infrastructure control covers hosting, networking, and capacity planning.

**Criterion description:** Infrastructure control covers hosting, networking, and capacity planning.

**Documentation hint (for field study context only; not rated in Round 1):**  
Infrastructure ownership model, capacity plan, and disaster recovery design.

**Risk if missing (indicative):**  
Service continuity and security depend on opaque external platforms.

**Traceability references:**

- **ART** — Responsibility: Own hosting and capacity. Infrastructure control is a strategic responsibility for continuity.
- **EU Trustworthy AI** — Technical robustness and safety: Resilience. Resilient infrastructure underpins trustworthy operation.
- **AI Act** — Risk management: Operational resilience. Business continuity in risk management programmes.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 24. `strategic_sovereignty_portability`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Portability supports migration of models, prompts, and evaluation assets.

**Criterion description:** Portability supports migration of models, prompts, and evaluation assets.

**Documentation hint (for field study context only; not rated in Round 1):**  
Export formats, container images, and migration test results.

**Risk if missing (indicative):**  
Switching costs may block adoption of improved local models or policies.

**Traceability references:**

- **ART** — Transparency: Migrate models and prompts. Portability makes technical commitments auditable and reversible.
- **EU Trustworthy AI** — Human agency and oversight: Reversibility and contestability. Portability supports contestability when systems fail citizens.
- **AI Act** — Risk management: Interoperability. Reduces dependency risk in technical governance.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

### 25. `strategic_sovereignty_maintainability`

**Assessment question:** For a bounded municipal AI/LLM programme dossier, is the following criterion relevant and clearly worded for programme-level governance readiness assessment? Criterion: Long-term maintainability plans staffing, upgrades, and technical debt management.

**Criterion description:** Long-term maintainability plans staffing, upgrades, and technical debt management.

**Documentation hint (for field study context only; not rated in Round 1):**  
Roadmap, budget lines, and skills development plan for sustaining on-prem AI.

**Risk if missing (indicative):**  
Systems may become unsupported while still handling citizen-facing workloads.

**Traceability references:**

- **ART** — Responsibility: Sustain staffing and upgrades. Long-term maintainability is a governance responsibility, not only IT.
- **EU Trustworthy AI** — Societal and environmental wellbeing: Long-term societal wellbeing. Sustainable operation aligns with HLEG societal wellbeing dimension.
- **AI Act** — Risk management: Lifecycle resource planning. Resource planning for ongoing compliance and monitoring.

**Your ratings**

| Field | Your response |
|-------|---------------|
| Relevance (1–5) | |
| Clarity (1–5) | |
| Essential? (Yes/No) | |

**Suggested revision (optional):**


**Comment (optional):**


---

*End of questionnaire — LocalGovBench v0.1 Delphi Round 1 (programme dossier / evidence-gated validation study)*