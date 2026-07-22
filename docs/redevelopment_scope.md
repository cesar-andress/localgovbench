> **Status: LEGACY — v0.1.0**  
> Historical reproducibility / scope documentation for the v0.1 instrument.  
> **Active framework:** [`../localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and root [`README.md`](../README.md). Commands for Disclosure Functions v1 are documented there.


# LocalGovBench redevelopment scope

## Purpose

LocalGovBench is being **redeveloped** as an **instrument-development and validation study** focused on **programme-level governance readiness** assessed from **confidential municipal LLM/AI programme dossiers** by **independent assessors**.

This layer is distinct from any work on **public-record documentary observability**.

## Relationship to Vendor Stewardship

**Vendor Stewardship in the Public Record** is a **separate submitted paper**. It covers public-document observability, a 20-municipality Europe/North America corpus, official document genres, registers/portals, D4 procurement/vendor stewardship, and Documentary Accountability Architecture.

That submitted paper must remain **fully reproducible** from this repository. Files that support it are **not** part of the new LocalGovBench validation manuscript and must **not** be moved, renamed, or deleted as part of this redevelopment.

## Public-record assets in this repository

Public-record observability assets (for example under `paper/data/open_pilot/` in the companion manuscript repository, and related reproduction materials) may remain in the monorepo **only for reproducibility of Vendor Stewardship**, **not** as primary validation evidence for the new LocalGovBench manuscript.

The new manuscript-facing validation layer lives under:

- `validation/dossier/`
- `validation/content_validity/delphi/`
- `data/dossiers/` (confidential programme dossiers; gitignored contents)
- `data/vignettes/` (assessor training only)
- `exports/validation/` (publishable aggregates from real expert/dossier studies)
- `docs/partner/` (recruitment and ethics templates)

## Synthetic fixtures

Synthetic fixtures are allowed **only** for:

- automated tests (`tests/`)
- assessor training vignettes (`data/vignettes/`)
- internal demo pipelines explicitly marked non-publishable

Synthetic IRR, synthetic municipality corpora, or synthetic benchmark scores must **never** be presented as **field validation evidence** in the redevelopment layer.

## Primary evidence for the new study

| Allowed primary evidence | Forbidden as primary evidence |
|--------------------------|-------------------------------|
| Expert Delphi / content validity (I-CVI, CVR) | Public-document observability rates |
| Real programme dossier assessments | Public AI registers or transparency portals as study corpus |
| Independent assessor scoring + adjudication | Document genre analysis |
| Field inter-rater reliability on real dossiers | D4 procurement/vendor stewardship as main outcome |
| Gate ablation and sensitivity on real scores | Documentary Accountability Architecture as contribution |
| | Synthetic IRR presented as field validation |
| | open_pilot outputs (must not use as validation evidence) |

## Scope enforcement

Run before committing changes to the redevelopment layer:

```bash
python3.12 scripts/validate_redevelopment_scope.py
```

See `validation/redevelopment_scope.yaml` for machine-readable paths and guard rules.

## Local environment

- Use **Python 3.12** (the scope validator and package require a modern interpreter).
- Install dev dependencies before running validation scripts:

```bash
pip install -e ".[dev]"
```

- Run the scope guard:

```bash
python3.12 scripts/validate_redevelopment_scope.py
```
