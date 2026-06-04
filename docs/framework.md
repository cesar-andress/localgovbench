# Local AI Governance Framework

**Version 0.1** — research preview, not empirically validated.

LocalGovBench provides a structured framework for assessing **local and on-premise large language model (LLM) deployments** in European public sector organizations. The framework supports descriptive self-assessment and future benchmarking; it does not replace legal advice or formal conformity assessment.

## Scope

The v0.1 framework targets deployments where:

- Inference runs on institution-controlled infrastructure (on-premise or sovereign cloud enclave)
- Citizen or caseworker interaction data should remain under public authority control
- Governance must address GDPR, EU AI Act themes, and operational sovereignty jointly

## Design principles

1. **Proportionality** — Criterion-level maturity (0–4), not binary certification.
2. **Evidence orientation** — Each criterion suggests documentary evidence types.
3. **Risk awareness** — Missing practices are linked to plausible governance risks (indicative).
4. **Neutrality** — Wording avoids claims of validated effectiveness in v0.1.

## Core components

| Component | Module | Role |
|-----------|--------|------|
| Dimensions | `localgovbench.framework.dimensions` | Five thematic areas with criteria |
| Checklist | `localgovbench.framework.checklist` | One assessable item per criterion |
| Scoring | `localgovbench.framework.scoring` | Maturity aggregation |

## Five dimensions (v0.1)

| ID | Name |
|----|------|
| `legal_regulatory` | Legal and Regulatory Compliance |
| `technical_security` | Technical and Security Readiness |
| `organizational` | Organizational Governance |
| `operational` | Operational Management |
| `strategic_sovereignty` | Strategic Sovereignty |

See [governance_dimensions.md](governance_dimensions.md) for criteria and indicative risks.

The full academic benchmark specification (assessment questions, evidence tables, scoring protocol) is in [benchmark_specification.md](benchmark_specification.md).

## Maturity model

Each checklist item is scored on an integer **0–4** scale:

| Level | Label | Interpretation |
|-------|-------|----------------|
| 0 | Absent | No observable practice |
| 1 | Ad hoc | Informal practice without consistent documentation |
| 2 | Partially defined | Documented but inconsistently applied |
| 3 | Managed | Assigned ownership and defined review cadence |
| 4 | Optimized | Evidence-informed continuous improvement |

Dimension scores are unweighted means of criterion scores in v0.1. **Weights and thresholds are not calibrated** against field data in this release.

## Usage

```python
from localgovbench.framework.dimensions import FRAMEWORK_VERSION, GOVERNANCE_DIMENSIONS
from localgovbench.framework.checklist import build_checklist
from localgovbench.framework.scoring import compute_maturity_score, MATURITY_LEVELS

assert FRAMEWORK_VERSION == "0.1"
checklist = build_checklist()  # 25 items in v0.1
# Map responses: item_id -> score (0-4), then:
# result = compute_maturity_score(responses)
```

## Limitations

- **Not validated:** v0.1 has not been tested for construct validity, inter-rater reliability, or predictive utility.
- **Indicative mappings:** Regulatory cross-walks in `docs/ai_act_mapping.md` and `docs/gdpr_mapping.md` are illustrative.
- **Synthetic examples only** in bundled assessments unless a future release states otherwise.

See [methodology.md](methodology.md) for the intended evaluation programme.
