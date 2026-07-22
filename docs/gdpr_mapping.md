> **Status: LEGACY — v0.1.0**  
> Retained for provenance of the historical Governance Readiness Benchmark / v0.1 instrument.  
> **Do not use this document as the current analytical specification.**  
> **Active framework:** Disclosure Functions v1 — see [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and the root [`README.md`](../README.md).

# GDPR Mapping (Indicative, v0.1)

> **Disclaimer:** This document supports **research orientation and structured self-assessment**. It is **not legal advice**. Public sector processing remains subject to Regulation (EU) 2016/679 (GDPR), national supplements, and sector-specific rules. Consult qualified counsel and supervisory authority guidance for compliance decisions.

## Purpose of this mapping

The Local AI Governance Framework (v0.1) addresses **governance practices** around on-premise LLM deployments that often process personal data (prompts, logs, embeddings, metadata). The tables below suggest **where framework criteria may inform review** of GDPR-related themes. They do not determine lawfulness or compliance.

Mappings are **indicative** and the instrument is **not validated** against GDPR enforcement practice in v0.1.

## Framework dimensions (reference)

| Dimension ID | Name |
|--------------|------|
| `legal_regulatory` | Legal and Regulatory Compliance |
| `technical_security` | Technical and Security Readiness |
| `organizational` | Organizational Governance |
| `operational` | Operational Management |
| `strategic_sovereignty` | Strategic Sovereignty |

---

## 1. Lawfulness, fairness, and transparency

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `legal_regulatory` / `lawful_basis` | May document legal bases and fairness considerations for processing. |
| `legal_regulatory` / `gdpr_readiness` | May aggregate RoPA entries, privacy notices, and governance contacts. |
| `operational` / `documentation`, `human_oversight` | May support transparency toward staff; public transparency may require additional artefacts. |
| `organizational` / `accountability` | May link fairness and transparency duties to named service ownership. |

---

## 2. Purpose limitation

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `legal_regulatory` / `lawful_basis` | May record specified, explicit, and legitimate purposes per processing activity. |
| `operational` / `lifecycle_management` | May define stage gates preventing scope creep from pilot to production. |
| `operational` / `documentation` | May maintain purpose statements in system documentation. |
| `strategic_sovereignty` / `data_sovereignty` | May clarify institutional control over purposes of on-premise processing. |

---

## 3. Data minimization

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `legal_regulatory` / `lawful_basis`, `data_retention` | May document categories of data collected and exclusion rules. |
| `technical_security` / `logging` | May define redaction, pseudonymization, or exclusion of personal data in logs. |
| `strategic_sovereignty` / `data_sovereignty` | May limit external copying of prompts or embeddings. |
| `operational` / `monitoring` | May use sampling rather than full content retention where appropriate. |

---

## 4. Storage limitation

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `legal_regulatory` / `data_retention` | Primary locus for retention schedules and deletion for prompts, logs, and derived artefacts. |
| `technical_security` / `logging` | May implement technical deletion or rotation aligned with policy. |
| `operational` / `lifecycle_management` | May include decommissioning and archival rules. |

---

## 5. Integrity and confidentiality

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `technical_security` / `access_control`, `local_architecture` | May describe security of processing (Art. 32-oriented measures in research coding). |
| `technical_security` / `logging`, `auditability` | May support detection of unauthorized access or changes. |
| `legal_regulatory` / `cross_border_avoidance` | May reduce confidentiality risks from unintended transfers. |
| `operational` / `incident_response` | May address personal data breaches as part of incident handling. |

---

## 6. Accountability

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `organizational` / `accountability`, `ownership` | May demonstrate responsibility assignments under Art. 5(2). |
| `legal_regulatory` / `gdpr_readiness` | May include DPO consultation records and compliance documentation. |
| `technical_security` / `auditability` | May provide evidence of implemented measures. |
| `organizational` / `risk_ownership` | May connect GDPR risks to institutional risk processes. |

---

## 7. Data subject rights

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `operational` / `human_oversight` | May define pathways for correction when AI outputs affect individuals. |
| `legal_regulatory` / `data_retention` | May support erasure when logs or embeddings contain personal data. |
| `operational` / `documentation` | May describe how requests are routed (access, rectification, erasure, restriction). |
| `organizational` / `role_definition` | May assign roles for handling data subject requests involving AI systems. |

**Note:** Art. 22 (automated decision-making) may be relevant where LLM outputs contribute to significant decisions; this requires case-specific legal analysis beyond the framework.

---

## 8. Data protection impact assessment (DPIA)

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `legal_regulatory` / `gdpr_readiness` | May reference completed or planned DPIAs where triggers apply. |
| `organizational` / `risk_ownership` | May integrate DPIA outcomes into risk registers. |
| `technical_security` / `local_architecture` | May supply technical descriptions for DPIA annexes. |
| `operational` / `lifecycle_management` | May require DPIA review before scaling processing. |

The framework **does not replace** a DPIA; it may help researchers locate documentary evidence during case studies.

---

## 9. Processor and controller responsibilities

| Framework locus | Indicative relevance to GDPR themes |
|-----------------|-------------------------------------|
| `organizational` / `procurement_governance` | May address Art. 28-style arrangements with vendors hosting models or support services. |
| `legal_regulatory` / `cross_border_avoidance` | May clarify sub-processors and transfer mechanisms. |
| `strategic_sovereignty` / `vendor_independence`, `data_sovereignty` | May document controller control over processing locations and subprocessors. |
| `organizational` / `role_definition` | May distinguish controller, processor, and joint arrangement roles in practice. |

---

## Cross-theme matrix (summary)

| GDPR theme (research lens) | Primary dimensions | Secondary dimensions |
|---------------------------|-------------------|---------------------|
| Lawfulness, fairness, transparency | `legal_regulatory` | `organizational`, `operational` |
| Purpose limitation | `legal_regulatory` | `operational`, `strategic_sovereignty` |
| Data minimization | `legal_regulatory`, `technical_security` | `strategic_sovereignty`, `operational` |
| Storage limitation | `legal_regulatory` | `technical_security`, `operational` |
| Integrity and confidentiality | `technical_security` | `legal_regulatory`, `operational` |
| Accountability | `organizational`, `legal_regulatory` | `technical_security` |
| Data subject rights | `operational` | `legal_regulatory`, `organizational` |
| DPIA | `legal_regulatory` | `organizational`, `technical_security` |
| Processor/controller responsibilities | `organizational` | `legal_regulatory`, `strategic_sovereignty` |

## Synthetic and future empirical data

Bundled examples contain **no personal data** and are marked `synthetic: true`. Future field studies should publish only anonymized or aggregated materials with ethics approval and lawful basis documentation.

## Limitations

- Mapping does not cover all GDPR articles or national variants.
- Public sector exemptions and specific national laws are out of scope for v0.1.
- Framework maturity scores are **not** compliance scores.

## References (non-exhaustive)

- Regulation (EU) 2016/679 (GDPR)
- EDPB guidelines (automated decision-making, DPIA, breach notification — verify current versions)
