# Local AI Governance Framework

LocalGovBench defines a **local AI governance framework** for European public sector organizations at municipal, regional, and agency level. The framework is descriptive and evaluative: it helps structure self-assessment and benchmarking rather than replacing legal compliance advice.

## Design principles

1. **Local applicability** — Emphasizes operational decisions made close to citizens and services.
2. **Regulatory alignment** — Maps dimensions to EU AI Act and GDPR themes (see mapping docs).
3. **Proportionality** — Supports tiered maturity rather than binary pass/fail claims.
4. **Transparency** — Encourages documented rationale for AI use in public services.

## Core components

| Component | Module | Role |
|-----------|--------|------|
| Dimensions | `localgovbench.framework.dimensions` | Thematic areas of governance |
| Checklist | `localgovbench.framework.checklist` | Actionable control items |
| Scoring | `localgovbench.framework.scoring` | Maturity aggregation |

## Maturity levels

Scores are normalized to a 0–4 scale:

| Level | Label | Interpretation |
|-------|-------|----------------|
| 0 | Absent | No observable practice |
| 1 | Initial | Ad hoc or undocumented |
| 2 | Defined | Documented but inconsistently applied |
| 3 | Managed | Monitored and assigned ownership |
| 4 | Optimized | Continuous improvement with evidence |

## Usage

```python
from localgovbench.framework.dimensions import GOVERNANCE_DIMENSIONS
from localgovbench.framework.checklist import build_checklist
from localgovbench.framework.scoring import compute_maturity_score

checklist = build_checklist()
# Populate responses via assessment YAML or your own pipeline
```

## Limitations (early-stage artifact)

- Dimension weights are equal by default; empirical calibration is planned.
- Regulatory mappings are indicative, not legal opinions.
- Sample assessments use **synthetic** data only.

See [methodology.md](methodology.md) for evaluation design.
