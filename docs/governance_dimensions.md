> **Status: LEGACY — v0.1.0**  
> This document describes the historical Governance Readiness Benchmark / v0.1 instrument design.  
> It is retained for provenance and is **not** the active analytical framework.  
> **Active framework:** Disclosure Functions v1 — see [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and the root [`README.md`](../README.md).


# Governance Dimensions (v0.1)

The Local AI Governance Framework **version 0.1** comprises **five dimensions**, each with **five criteria** (25 assessable items in total). Criteria are implemented in `localgovbench/framework/dimensions.py` and exposed via `build_checklist()`.

> This instrument is a research scaffold. It has **not** been empirically validated in v0.1.

## Overview

| ID | Name | Focus |
|----|------|-------|
| `legal_regulatory` | Legal and Regulatory Compliance | GDPR, AI Act themes, retention, lawful basis, transfer avoidance |
| `technical_security` | Technical and Security Readiness | On-prem architecture, access, logging, audit, model updates |
| `organizational` | Organizational Governance | Accountability, ownership, roles, procurement, risk ownership |
| `operational` | Operational Management | Monitoring, incidents, oversight, documentation, lifecycle |
| `strategic_sovereignty` | Strategic Sovereignty | Vendor independence, data/hosting control, portability, maintainability |

## 1. Legal and Regulatory Compliance (`legal_regulatory`)

**Description:** Regulatory and data-protection alignment for on-premise LLM processing in European public bodies.

| Criterion ID | Topic |
|--------------|-------|
| `gdpr_readiness` | GDPR readiness |
| `ai_act_alignment` | EU AI Act alignment (deployer-oriented documentation) |
| `data_retention` | Data retention and deletion |
| `lawful_basis` | Lawful basis and purpose limitation |
| `cross_border_avoidance` | Cross-border transfer avoidance |

**Suggested evidence (examples):** records of processing, DPIA materials, retention schedules, architecture egress controls.

**Indicative risks if weak:** accountability gaps, unlawful processing exposure, unintended international transfers.

## 2. Technical and Security Readiness (`technical_security`)

**Description:** Security and operability of local LLM stacks.

| Criterion ID | Topic |
|--------------|-------|
| `local_architecture` | Local deployment architecture |
| `access_control` | Access control |
| `logging` | Logging |
| `auditability` | Auditability |
| `model_updates` | Model update management |

**Suggested evidence:** architecture diagrams, IAM matrices, logging policies, change-management records.

**Indicative risks if weak:** forensic gaps, privilege abuse, uncontrolled model drift.

## 3. Organizational Governance (`organizational`)

**Description:** Institutional accountability for AI-supported public services.

| Criterion ID | Topic |
|--------------|-------|
| `accountability` | Accountability |
| `ownership` | Ownership |
| `role_definition` | Role definition |
| `procurement_governance` | Procurement governance |
| `risk_ownership` | Risk ownership |

**Suggested evidence:** governance charters, RACI matrices, contracts, risk registers.

**Indicative risks if weak:** diffused responsibility, vendor-dominated decisions, untracked AI risks.

## 4. Operational Management (`operational`)

**Description:** Day-to-day running of local LLM services.

| Criterion ID | Topic |
|--------------|-------|
| `monitoring` | Monitoring |
| `incident_response` | Incident response |
| `human_oversight` | Human oversight |
| `documentation` | Documentation |
| `lifecycle_management` | Lifecycle management |

**Suggested evidence:** dashboards, IR plans, oversight procedures, operator handbooks, decommission checklists.

**Indicative risks if weak:** undetected degradation, harmful outputs reaching users, orphaned pilots in production.

## 5. Strategic Sovereignty (`strategic_sovereignty`)

**Description:** Long-term control over data, infrastructure, and maintainability.

| Criterion ID | Topic |
|--------------|-------|
| `vendor_independence` | Vendor independence |
| `data_sovereignty` | Data sovereignty |
| `infrastructure_control` | Infrastructure control |
| `portability` | Portability |
| `maintainability` | Long-term maintainability |

**Suggested evidence:** supplier analysis, residency statements, DR design, migration tests, sustainment roadmap.

**Indicative risks if weak:** lock-in, loss of data control, brittle unsupported services.

## Implementation notes

- Full criterion text, evidence hints, and per-criterion risks: `localgovbench/framework/dimensions.py`
- Checklist item ids: `{dimension_id}_{criterion_id}` (e.g. `legal_regulatory_gdpr_readiness`)
- Scoring: `localgovbench/framework/scoring.py` (0–4 scale, uniform dimension weights in v0.1)

Weighted scoring and empirical calibration may be introduced in later versions after field studies.
