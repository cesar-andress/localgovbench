# Methodology

This document outlines the intended methodology for LocalGovBench. **Empirical studies and field datasets are not yet part of this repository release.**

## Research objective

Develop a reproducible framework and benchmark scaffolding to:

1. Characterize local AI governance practices in European public sector bodies.
2. Enable structured self-assessment and comparative analysis (with appropriate ethics and consent).
3. Support alignment discussions with EU AI Act and GDPR obligations.

## Assessment workflow (planned)

```mermaid
flowchart LR
  A[Scope AI system] --> B[Map dimensions]
  B --> C[Complete checklist]
  C --> D[Score maturity]
  D --> E[Validate responses]
  E --> F[Report and review]
```

## Data policy

| Stage | Status in this release |
|-------|------------------------|
| Synthetic examples | Included in `examples/` |
| Template instruments | Placeholders in `data/templates/` |
| Raw field data | **Not included** — `data/raw/` is empty |
| Processed benchmark results | **Not included** — `data/processed/` is empty |

> **Warning:** Any demonstration output from scripts in this repository is based on **synthetic** inputs unless a future release note states otherwise.

## Validation

- **Structural:** `scripts/validate_repository.py` checks required paths and metadata.
- **Logical:** `localgovbench.evaluation.validators` checks score ranges and required fields.
- **Statistical / inter-rater:** Planned for releases that include empirical benchmark data.

## Reproducibility

1. Pin Python 3.11+ and install via `pip install -e ".[dev]"`.
2. Run `pytest` and example scripts from repository root.
3. Archive releases on Zenodo with version tags matching `CITATION.cff` (see [zenodo_release.md](zenodo_release.md)).

## Ethics

Future empirical work must follow institutional ethics review, data minimization, and public sector transparency obligations. Do not commit identifiable records to this repository.
