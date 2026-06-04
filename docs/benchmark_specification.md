# LocalGovBench Benchmark Specification

**Instrument:** Governance Readiness Benchmark for sovereign large language model (LLM) deployments in municipalities  
**Version:** 0.1 (research preview)  
**Status:** Not empirically validated; indicative regulatory alignment only  
**Date:** 2026

---

## Abstract

LocalGovBench is a **governance readiness benchmark** that evaluates whether a municipality possesses the institutional capability to **deploy and operate a sovereign LLM responsibly**. The benchmark assesses **governance maturity**, not technical model performance (e.g., accuracy, perplexity, or benchmark leaderboards).

The instrument is designed to be **auditable** (evidence-linked scoring), **practical** (document- and process-based indicators), and **compatible in orientation** with EU AI Act deployer themes, the EU High-Level Expert Group (HLEG) Trustworthy AI Guidelines, and established principles of **accountability** and **meaningful human oversight**. It does **not** provide legal advice or conformity certification.

---

## 1. Purpose and scope

### 1.1 Purpose

To support researchers and public institutions in:

1. Structuring self-assessment or third-party review before scaling an on-premise or sovereign-enclave LLM.
2. Identifying governance gaps that may impede responsible deployment.
3. Producing a reproducible **readiness score** with an explicit evidence trail.

### 1.2 Unit of assessment

A **municipal LLM deployment programme** defined by:

- Institutional boundary (municipality or mandated inter-municipal body)
- Stated use case(s) (e.g., internal drafting, citizen-facing information support)
- Sovereign deployment model (on-premise or institution-controlled hosting without unmanaged third-country inference)

### 1.3 Out of scope

| In scope | Out of scope |
|----------|--------------|
| Governance processes, roles, documentation | Model accuracy, F1, hallucination rate benchmarks |
| Lawful processing and oversight arrangements | Formal CE marking or Notified Body assessment |
| Risk and incident governance | Penetration testing scores as sole metric |
| Strategic sovereignty and exit paths | Vendor marketing maturity claims |

### 1.4 Design principles

| Principle | Operationalization |
|-----------|-------------------|
| Governance-focused | Every item scores institutional practice, not GPU throughput |
| Auditable | Score ≥3 requires cited evidence artefact(s) |
| Practical | Indicators verifiable from policies, registers, contracts, logs policy |
| EU AI Act–oriented | Mapped to deployer-relevant themes (see [ai_act_mapping.md](ai_act_mapping.md)) |
| Trustworthy AI–aligned | Structured around HLEG requirements at governance level |
| Accountability & oversight | Dedicated items for RACI, human review, and ex-post review |

---

## 2. Benchmark dimensions

Five dimensions comprise **25 assessment items** (five criteria per dimension). Each criterion maps to one checklist item in `localgovbench/framework/`.

| ID | Dimension | Readiness focus | HLEG / AI Act orientation (indicative) |
|----|-----------|-----------------|----------------------------------------|
| `legal_regulatory` | Legal and Regulatory Compliance | Lawful, retention-bound, jurisdictionally controlled processing | Privacy & data governance; accountability |
| `technical_security` | Technical and Security Readiness | Secure, observable, controlled on-prem stack | Technical robustness & safety; logging |
| `organizational` | Organizational Governance | Clear ownership, roles, procurement, risk assignment | Accountability; human agency (institutional) |
| `operational` | Operational Management | Monitoring, incidents, oversight, lifecycle | Human oversight; post-deployment monitoring |
| `strategic_sovereignty` | Strategic Sovereignty | Long-term control, portability, sustainment | Strategic autonomy; supply-chain governance |

**Readiness hypothesis (research):** responsible sovereign deployment is feasible only when no critical dimension remains at maturity **0–1** for production-facing use cases. This hypothesis requires empirical testing.

---

## 3. Assessment questions and evidence

Each **assessment question** corresponds to one criterion. Evaluators record:

- Maturity score (0–4)
- Evidence references (document ID, date, location)
- Optional notes (gaps, planned actions)

### Dimension A — Legal and Regulatory Compliance (`legal_regulatory`)

#### A1 — GDPR readiness (`gdpr_readiness`)

**Assessment question:** Has the municipality established and maintained GDPR-aligned governance for all personal data flows in the LLM lifecycle (prompts, logs, embeddings, fine-tuning data)?

**Evidence required (examples):**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Records of processing (RoPA) entries for the LLM system |
| Required for score ≥3 | DPO consultation or documented DPO advice on the deployment |
| Supporting | Privacy notice or internal data protection guideline referencing the LLM |
| Supporting | Data flow diagram (on-prem boundaries) |

---

#### A2 — EU AI Act alignment (`ai_act_alignment`)

**Assessment question:** Has the municipality documented its deployer-oriented understanding of how the AI Act may apply to the LLM use case(s), including classification rationale and assigned responsibilities?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Internal AI Act review memo or checklist (non-binding) |
| Required for score ≥3 | Use-case description with affected populations and decision significance |
| Supporting | References to technical documentation or vendor instructions for use |
| Supporting | Human oversight summary cross-linked to operational procedures |

*Indicative AI Act themes: risk management, transparency, accountability (deployer duties).*

---

#### A3 — Data retention (`data_retention`)

**Assessment question:** Are retention and deletion rules defined and implemented for prompts, inference logs, embeddings, and backups?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Written retention schedule with maximum periods |
| Required for score ≥3 | Technical configuration or procedure evidencing deletion/rotation |
| Supporting | Backup and restore policy including LLM artefacts |

---

#### A4 — Lawful basis (`lawful_basis`)

**Assessment question:** Is a lawful basis and purpose documented for each category of personal data processed by the LLM?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Lawful basis register or RoPA field per processing activity |
| Required for score ≥3 | Purpose limitation statement in system design or policy |
| Supporting | Data minimization checklist used at project gate |

---

#### A5 — Cross-border transfer avoidance (`cross_border_avoidance`)

**Assessment question:** Has the municipality defined and enforced boundaries to avoid unintended cross-border transfers in sovereign operation?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Architecture/network diagram with data residency and egress controls |
| Required for score ≥3 | Sub-processor / vendor list with processing locations |
| Supporting | Contract clauses restricting offshore inference or telemetry |

---

### Dimension B — Technical and Security Readiness (`technical_security`)

#### B1 — Local deployment architecture (`local_architecture`)

**Assessment question:** Is the end-to-end on-premise (or sovereign enclave) architecture documented, including components, integrations, and trust boundaries?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Approved architecture diagram (versioned) |
| Required for score ≥3 | Component inventory (models, gateways, vector stores) |
| Supporting | Secrets management description |

*HLEG: technical robustness & safety (governance of system design).*

---

#### B2 — Access control (`access_control`)

**Assessment question:** Does access control enforce least privilege for administrators, operators, and end users of the LLM?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | IAM role matrix for the LLM environment |
| Required for score ≥3 | Authentication method and review cadence documentation |
| Supporting | Sample access review record (last 12 months) |

---

#### B3 — Logging (`logging`)

**Assessment question:** Is security- and governance-relevant logging implemented with proportionate personal data handling?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Logging policy (events captured, retention, redaction) |
| Required for score ≥3 | Sample log schema or SIEM integration description |
| Supporting | DPIA or privacy note on log content |

*AI Act theme: logging and record-keeping (institutional implementation).*

---

#### B4 — Auditability (`auditability`)

**Assessment question:** Can configuration and material changes to models, prompts, and policies be traced to accountable actors?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Audit trail configuration or change log exports |
| Required for score ≥3 | Change management tickets linked to production changes |
| Supporting | Immutable log store reference |

*Supports accountability and meaningful human control (tracing).*

---

#### B5 — Model update management (`model_updates`)

**Assessment question:** Are model and weight updates subject to defined testing, approval, and rollback?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Model change standard operating procedure |
| Required for score ≥3 | Validation record for last production update |
| Supporting | Version registry with approval signatures |

---

### Dimension C — Organizational Governance (`organizational`)

#### C1 — Accountability (`accountability`)

**Assessment question:** Are public service accountability lines defined for outcomes influenced by the LLM?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Governance charter or council mandate referencing AI accountability |
| Required for score ≥3 | Named executive or political sponsor |
| Supporting | Committee terms of reference |

*HLEG: accountability; ART framework (accountability dimension).*

---

#### C2 — Ownership (`ownership`)

**Assessment question:** Is sustained service ownership assigned (not delegated solely to a vendor)?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Service owner nomination in service catalogue |
| Required for score ≥3 | RACI matrix covering legal, DPO, security, operations |
| Supporting | Escalation contact list |

---

#### C3 — Role definition (`role_definition`)

**Assessment question:** Are roles and competencies defined for legal, ethical, technical, and operational functions?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Role descriptions or responsibility assignments |
| Required for score ≥3 | Training plan by role |
| Supporting | Interdisciplinary workshop or steering group minutes |

*HLEG: human agency and oversight (institutional capacity).*

---

#### C4 — Procurement governance (`procurement_governance`)

**Assessment question:** Do contracts and procurement processes govern AI performance, monitoring, updates, and exit?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Contract excerpts on SLAs, model change notification, audit rights |
| Required for score ≥3 | Vendor due diligence record for AI components |
| Supporting | Transition assistance clause |

---

#### C5 — Risk ownership (`risk_ownership`)

**Assessment question:** Is AI risk identification, treatment, and reporting assigned within municipal risk management?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Risk register entries for the LLM programme |
| Required for score ≥3 | Risk review cadence and last review date |
| Supporting | Risk appetite statement reference |

*AI Act theme: risk management (institutional).*

---

### Dimension D — Operational Management (`operational`)

#### D1 — Monitoring (`monitoring`)

**Assessment question:** Is ongoing monitoring defined for operational health, safety signals, and governance KPIs?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Monitoring plan with metrics and thresholds |
| Required for score ≥3 | Sample dashboard or periodic review report |
| Supporting | Escalation rules tied to metrics |

*AI Act theme: post-market monitoring (adapted to deployer context).*

---

#### D2 — Incident response (`incident_response`)

**Assessment question:** Does an incident response plan cover harmful outputs, security events, and service outages?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Incident response plan including AI-specific scenarios |
| Required for score ≥3 | Tabletop exercise or drill record |
| Supporting | Post-incident review template |

---

#### D3 — Human oversight (`human_oversight`)

**Assessment question:** Are human oversight procedures defined where LLM outputs influence staff work or citizen-facing services?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Oversight procedure with review triggers |
| Required for score ≥3 | Sampling or review protocol for outputs |
| Supporting | Appeal or correction pathway documentation |

*HLEG: human agency and oversight; meaningful human control (intervention).*

---

#### D4 — Documentation (`documentation`)

**Assessment question:** Is operator and maintainer documentation complete, including limitations and prohibited uses?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | System documentation set (version controlled) |
| Required for score ≥3 | Prompt registry or configuration catalogue |
| Supporting | “When not to use” guidance for staff |

*HLEG: transparency; AI Act technical documentation (institutional holding).*

---

#### D5 — Lifecycle management (`lifecycle_management`)

**Assessment question:** Are stage gates defined for pilot, production, scale, and decommissioning?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Lifecycle gate criteria document |
| Required for score ≥3 | Decommissioning checklist |
| Supporting | Archival policy for models and logs |

---

### Dimension E — Strategic Sovereignty (`strategic_sovereignty`)

#### E1 — Vendor independence (`vendor_independence`)

**Assessment question:** Has the municipality analysed and mitigated critical vendor dependencies?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Dependency analysis or contingency plan |
| Supporting | Open standards / dual-sourcing notes |

---

#### E2 — Data sovereignty (`data_sovereignty`)

**Assessment question:** Is primary data for the LLM under institutional control with restricted third-party access?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Data residency / sovereignty statement |
| Required for score ≥3 | Access restrictions on training and inference stores |
| Supporting | Third-party access log review |

---

#### E3 — Infrastructure control (`infrastructure_control`)

**Assessment question:** Are hosting, networking, capacity, and disaster recovery under documented municipal control?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Infrastructure ownership model |
| Required for score ≥3 | DR/BCP design with test date |
| Supporting | Capacity plan (3–5 years) |

---

#### E4 — Portability (`portability`)

**Assessment question:** Can models, prompts, and evaluation assets be migrated without prohibitive lock-in?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Migration plan or portability test record |
| Supporting | Export format documentation |

---

#### E5 — Maintainability (`maintainability`)

**Assessment question:** Are budget, staffing, and skills planned for sustained operation beyond pilot funding?

**Evidence required:**

| Priority | Artefact |
|----------|----------|
| Required for score ≥3 | Medium-term roadmap with budget line |
| Required for score ≥3 | Skills development plan |
| Supporting | Technical debt register |

---

## 4. Scoring methodology

### 4.1 Level of scoring

| Level | Object scored |
|-------|----------------|
| Criterion | Each of 25 items (primary unit) |
| Dimension | Mean of five criteria in dimension |
| Overall readiness | Weighted mean of five dimensions (default: equal weights) |

### 4.2 Computation

Let \(s_i \in \{0,1,2,3,4\}\) be the score for criterion \(i\).

**Dimension score:**

\[
S_d = \frac{1}{n_d} \sum_{i \in d} s_i
\]

where \(n_d = 5\) for all dimensions in v0.1.

**Overall maturity (0–4 scale):**

\[
S_{\text{overall}} = \frac{\sum_{d} w_d \cdot S_d}{\sum_{d} w_d}, \quad w_d = 1 \text{ (default)}
\]

**Readiness index (0–100):**

\[
R = 100 \cdot \frac{S_{\text{overall}}}{4}
\]

Implemented in `localgovbench.framework.scoring.compute_maturity_score`.

### 4.3 Evidence gate (auditable scoring rule)

| Rule | Description |
|------|-------------|
| **E1** | Scores 0–2 may be assigned with assessor notes only |
| **E2** | Score **3** requires ≥1 required artefact per criterion table |
| **E3** | Score **4** requires ≥2 artefacts including one showing review in last 12 months |
| **E4** | Evidence log fields: `artefact_id`, `type`, `date`, `reviewer`, `uri` (internal) |

### 4.4 Optional safeguard rules (research protocol)

| Rule | Description |
|------|-------------|
| **G1** | If `operational_human_oversight` ≤ 1 and use case is citizen-facing, cap \(R \leq 60\) |
| **G2** | If `legal_regulatory_lawful_basis` = 0, flag **not ready for production** regardless of \(R\) |
| **G3** | Report dimension scores separately; do not rank municipalities without consent |

### 4.5 Inter-rater reliability

For multi-coder studies:

1. Joint training on synthetic example (`examples/example_assessment.yaml`)
2. Independent coding with shared codebook (this document)
3. Report Cohen's κ or Krippendorff's α per dimension
4. Adjudication protocol for disagreement >1 point

### 4.6 Output artefacts

| Output | Description |
|--------|-------------|
| Criterion score table | 25 rows with evidence IDs |
| Dimension profile | Radar or table of \(S_d\) |
| \(R\) readiness index | 0–100 with band label |
| Gap narrative | Criteria ≤2 with risk_if_missing from framework |
| Version stamp | `framework_version: "0.1"` in metadata |

---

## 5. Maturity levels

### 5.1 Criterion-level scale

| Score | Label | Definition | Typical evidence profile |
|-------|-------|------------|---------------------------|
| **0** | Absent | No practice or documentation found | None |
| **1** | Ad hoc | Informal practice; fragmented docs | Emails, oral tradition |
| **2** | Partially defined | Documented; uneven application | Draft policy; partial RoPA |
| **3** | Managed | Assigned owner; periodic review | Approved policy; register entries |
| **4** | Optimized | Continuous improvement with metrics | Review cycle + KPI trends |

**Important:** Level 4 denotes **governance maturity**, not legal compliance or model safety certification.

### 5.2 Dimension-level interpretation

| \(S_d\) range | Dimension readiness |
|---------------|---------------------|
| 0.0 – 0.9 | Critical gap |
| 1.0 – 1.9 | Emerging |
| 2.0 – 2.9 | Partially ready |
| 3.0 – 3.6 | Largely ready |
| 3.7 – 4.0 | Advanced governance practice |

### 5.3 Overall readiness bands

| \(R\) (0–100) | Band | Suggested municipal interpretation (research) |
|---------------|------|---------------------------------------------|
| 0 – 24 | **Not ready** | Do not expand beyond controlled lab/pilot without remediation plan |
| 25 – 49 | **Emerging** | Address legal and oversight gaps before citizen-facing use |
| 50 – 74 | **Substantially ready** | Production possible with monitored rollout and residual gap plan |
| 75 – 100 | **Advanced readiness** | Strong governance; maintain review cycles; still not legal certification |

### 5.4 Mapping to Trustworthy AI and oversight principles

| Maturity band | Trustworthy AI orientation (indicative) |
|---------------|----------------------------------------|
| Not ready / Emerging | Human oversight and accountability mechanisms insufficient for responsible scale-up |
| Substantially ready | Core HLEG requirements addressed at organizational level; verify case-by-case |
| Advanced | Broad institutionalization; continue DPIA/legal review for new use cases |

---

## 6. Assessment protocol (practical workflow)

| Phase | Activity | Duration (indicative) |
|-------|----------|------------------------|
| 1 — Scoping | Define use case, deployment boundary, assessor team | 1–2 days |
| 2 — Evidence collection | Gather artefacts per Section 3 | 1–2 weeks |
| 3 — Scoring workshop | Score criteria with evidence gate E1–E3 | 1 day |
| 4 — Aggregation | Compute \(S_d\), \(R\); apply optional safeguards G1–G2 | 0.5 day |
| 5 — Reporting | Gap narrative + dimension profile; no public ranking without consent | 1 day |

**Roles:** service owner (lead), DPO/legal advisor, IT security, operations, optional external researcher.

---

## 7. Regulatory and ethical positioning

- **EU AI Act:** Benchmark items help **organize deployer documentation and practices**; they do not determine legal classification or conformity.
- **Trustworthy AI Guidelines:** Dimensions map to seven requirements at **governance** level (see [ai_act_mapping.md](ai_act_mapping.md), [gdpr_mapping.md](gdpr_mapping.md)).
- **Accountability & human oversight:** Embedded in `organizational_*` and `operational_human_oversight` criteria with mandatory evidence for higher maturity.

---

## 8. Limitations and future work

| Limitation | Planned research |
|------------|------------------|
| Not validated for construct validity | Expert panel review |
| Equal weights uncalibrated | Weight estimation from case studies |
| 25 items may miss local context | Optional regional annex |
| Self-assessment bias | Independent assessors + inter-rater metrics |

---

## 9. Machine-readable implementation

| Artefact | Location |
|----------|----------|
| Criterion definitions | `localgovbench/framework/dimensions.py` |
| Checklist generation | `localgovbench/framework/checklist.py` |
| Scoring functions | `localgovbench/framework/scoring.py` |
| Synthetic example | `examples/example_assessment.yaml` |
| Validation | `localgovbench/evaluation/validators.py` |

**Checklist item ID convention:** `{dimension_id}_{criterion_id}`

---

## 10. References (indicative)

- European Commission High-Level Expert Group on AI (2019). *Ethics Guidelines for Trustworthy AI.*
- Regulation (EU) 2024/1689 (Artificial Intelligence Act).
- Regulation (EU) 2016/679 (GDPR).
- Dignum, V. (2019). *Responsible Artificial Intelligence.* ART: Accountability, Responsibility, Transparency.
- Mittelstadt, B. D., et al. (2016). The ethics of algorithms: Mapping the debate. *Big Data & Society.*
- Santoni de Sio, F., & van den Hoven, J. (2018). Meaningful human control over autonomous systems. *Minds and Machines.*

---

## Appendix A — Quick reference: all assessment questions

| ID | Question (short form) |
|----|------------------------|
| `legal_regulatory_gdpr_readiness` | GDPR governance in place for LLM data flows? |
| `legal_regulatory_ai_act_alignment` | AI Act deployer documentation for use case? |
| `legal_regulatory_data_retention` | Retention/deletion defined and implemented? |
| `legal_regulatory_lawful_basis` | Lawful basis per data category documented? |
| `legal_regulatory_cross_border_avoidance` | Cross-border transfer controls enforced? |
| `technical_security_local_architecture` | Architecture documented end-to-end? |
| `technical_security_access_control` | Least-privilege access enforced? |
| `technical_security_logging` | Governance logging with proportionate data? |
| `technical_security_auditability` | Changes traceable to accountable actors? |
| `technical_security_model_updates` | Updates tested, approved, rollback-ready? |
| `organizational_accountability` | Service accountability lines defined? |
| `organizational_ownership` | Sustained service owner assigned? |
| `organizational_role_definition` | Roles and training defined? |
| `organizational_procurement_governance` | Contracts govern AI lifecycle? |
| `organizational_risk_ownership` | AI risks in municipal risk register? |
| `operational_monitoring` | Ongoing monitoring defined? |
| `operational_incident_response` | AI-aware incident response plan? |
| `operational_human_oversight` | Human oversight for influential outputs? |
| `operational_documentation` | Complete operator documentation? |
| `operational_lifecycle_management` | Pilot-to-production gates defined? |
| `strategic_sovereignty_vendor_independence` | Vendor dependency analysed? |
| `strategic_sovereignty_data_sovereignty` | Data under institutional control? |
| `strategic_sovereignty_infrastructure_control` | Infrastructure and DR documented? |
| `strategic_sovereignty_portability` | Migration path documented/tested? |
| `strategic_sovereignty_maintainability` | Long-term sustainment planned? |

---

*End of specification — LocalGovBench v0.1*
