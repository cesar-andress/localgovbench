# EU AI Act Mapping (Indicative, v0.1)

> **Disclaimer:** This document supports **research orientation and structured self-assessment**. It is **not legal advice** and does not determine legal classification, conformity, or compliance. Public authorities should consult qualified legal counsel and official guidance for binding interpretations of Regulation (EU) 2024/1689 (AI Act).

## Purpose of this mapping

The Local AI Governance Framework (v0.1) was designed for **local and on-premise large language model deployments** in European public sector contexts. The tables below suggest **where framework criteria may inform documentation or review** related to commonly discussed AI Act themes.

Mappings are **indicative**: applicability depends on system type, deployer/provider role, risk category, and national implementing measures. The framework has **not** been validated against legal text or enforcement practice in v0.1.

## Framework dimensions (reference)

| Dimension ID | Name |
|--------------|------|
| `legal_regulatory` | Legal and Regulatory Compliance |
| `technical_security` | Technical and Security Readiness |
| `organizational` | Organizational Governance |
| `operational` | Operational Management |
| `strategic_sovereignty` | Strategic Sovereignty |

---

## 1. Risk management

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `legal_regulatory` / `ai_act_alignment` | May support internal records on use-case framing and deployer-oriented risk considerations (subject to classification). |
| `organizational` / `risk_ownership` | May relate to assignment of risk identification, treatment, and reporting within the institution. |
| `organizational` / `accountability`, `ownership` | May help link AI risks to service-level accountability rather than treating risk as purely technical. |
| `operational` / `monitoring`, `incident_response` | May support operational detection and response practices discussed in risk management programmes. |
| `technical_security` / `model_updates` | May document controlled change processes that can reduce unreviewed model-related risk. |

**Research note:** This theme is often assessed through document analysis (risk registers, classification memos) and expert review workshops.

---

## 2. Transparency

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `operational` / `documentation` | May capture instructions, limitations, and operator-facing transparency materials. |
| `operational` / `human_oversight` | May document how staff and citizens are informed about AI-assisted steps. |
| `legal_regulatory` / `ai_act_alignment` | May hold deployer-facing transparency artefacts where required for the use case. |
| `organizational` / `role_definition` | May clarify who maintains public-facing and internal transparency content. |

**Research note:** Transparency in the AI Act is obligation-specific; the framework does not substitute for statutory disclosure requirements.

---

## 3. Human oversight

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `operational` / `human_oversight` | Primary locus for procedures, triggers, and appeal or correction pathways. |
| `organizational` / `accountability`, `ownership` | May define who authorizes overrides and reviews harmful outputs. |
| `organizational` / `role_definition` | May specify training and competence expectations for overseeing staff. |
| `technical_security` / `access_control` | May constrain who can alter prompts, models, or production configurations. |

---

## 4. Technical documentation

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `technical_security` / `local_architecture` | May describe system components, data flows, and on-premise boundaries. |
| `operational` / `documentation` | May aggregate runbooks, prompt registries, and known limitations. |
| `legal_regulatory` / `ai_act_alignment` | May cross-reference technical documentation expected for deployers/providers. |
| `strategic_sovereignty` / `infrastructure_control` | May document hosting, networking, and dependency structure. |

---

## 5. Logging and record keeping

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `technical_security` / `logging` | Primary locus for security and operational logging policy. |
| `technical_security` / `auditability` | May support traceability of configuration and inference-related changes. |
| `legal_regulatory` / `data_retention` | May align log retention with data protection rules. |
| `operational` / `incident_response` | May specify log preservation for investigations. |

---

## 6. Accuracy, robustness, and cybersecurity

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `technical_security` / `local_architecture`, `access_control` | May inform cybersecurity measures around on-premise stacks. |
| `technical_security` / `model_updates` | May document validation before deployment of new models or weights. |
| `operational` / `monitoring` | May track performance drift, error rates, or safety signals. |
| `operational` / `lifecycle_management` | May define testing stages before production use. |

**Caution:** The framework does not prescribe technical test metrics; it structures **whether** governance practices exist to address these concerns.

---

## 7. Post-market monitoring

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `operational` / `monitoring` | May support ongoing observation after deployment. |
| `operational` / `incident_response` | May cover serious incidents and corrective actions. |
| `organizational` / `risk_ownership` | May define periodic risk review cadence post-deployment. |
| `technical_security` / `model_updates` | May govern post-deployment model or configuration changes. |

---

## 8. Accountability

| Framework locus | Indicative relevance to AI Act themes |
|-----------------|--------------------------------------|
| `organizational` / `accountability` | Primary institutional accountability locus. |
| `organizational` / `ownership`, `role_definition` | May clarify responsible roles across legal, technical, and service functions. |
| `legal_regulatory` / `gdpr_readiness`, `lawful_basis` | May complement accountability under data protection law (see GDPR mapping). |
| `technical_security` / `auditability` | May provide evidentiary trails for retrospective review. |

---

## Cross-theme matrix (summary)

| AI Act theme (research lens) | Primary dimensions | Secondary dimensions |
|-----------------------------|-------------------|---------------------|
| Risk management | `organizational`, `operational` | `legal_regulatory`, `technical_security` |
| Transparency | `operational` | `organizational`, `legal_regulatory` |
| Human oversight | `operational` | `organizational`, `technical_security` |
| Technical documentation | `technical_security`, `operational` | `legal_regulatory`, `strategic_sovereignty` |
| Logging and record keeping | `technical_security` | `legal_regulatory`, `operational` |
| Accuracy, robustness, cybersecurity | `technical_security`, `operational` | `organizational` |
| Post-market monitoring | `operational` | `organizational`, `technical_security` |
| Accountability | `organizational` | `legal_regulatory`, `technical_security` |

## Public sector deployer perspective

Public bodies often act as **deployers** of AI systems, including on-premise LLMs integrated into administrative workflows. This mapping may help researchers **code documentary evidence** during case studies; it should not be read as a conformity checklist.

## Limitations

- No claim of completeness relative to the AI Act or future guidelines.
- National transposition and sector rules may impose additional requirements.
- v0.1 criteria have not been empirically tested for coverage of legal obligations.

## References (non-exhaustive)

- Regulation (EU) 2024/1689 (Artificial Intelligence Act)
- European Commission and office-holder guidance (verify current versions at release time)
