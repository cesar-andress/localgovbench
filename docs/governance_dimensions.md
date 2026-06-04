# Governance Dimensions

LocalGovBench organizes local AI governance into **seven dimensions**. Each dimension contains checklist items used for maturity scoring.

## Dimension overview

| ID | Name | Focus |
|----|------|-------|
| `strategy` | Strategy & leadership | Political mandate, AI strategy, executive accountability |
| `risk` | Risk management | Impact assessment, risk registers, escalation |
| `data` | Data governance | Quality, lineage, lawful basis, minimization |
| `transparency` | Transparency & explainability | Citizen-facing disclosure, documentation of logic |
| `accountability` | Accountability & oversight | Roles, audit trails, human oversight |
| `procurement` | Procurement & vendor management | Contractual AI requirements, vendor due diligence |
| `skills` | Skills & capacity | Training, interdisciplinary teams, external expertise |

## Dimension details

### Strategy & leadership (`strategy`)

Ensures AI initiatives align with democratic mandates and organizational priorities.

### Risk management (`risk`)

Covers identification and treatment of harms from AI in public services, including high-impact use cases.

### Data governance (`data`)

Addresses lawful, secure, and purpose-limited use of data feeding AI systems.

### Transparency & explainability (`transparency`)

Supports understandable communication about automated or AI-assisted decisions affecting the public.

### Accountability & oversight (`accountability`)

Defines who is responsible for outcomes and how interventions are logged and reviewed.

### Procurement & vendor management (`procurement`)

Extends governance to third-party models, platforms, and implementation partners.

### Skills & capacity (`skills`)

Captures organizational ability to govern, deploy, and monitor AI responsibly.

## Implementation

Dimension definitions live in `localgovbench/framework/dimensions.py`. Checklist items are generated in `localgovbench/framework/checklist.py`.

Weights are uniform (`1.0`) in this release; weighted scoring may be introduced when empirical calibration data is available.
