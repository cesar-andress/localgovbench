# Zenodo metadata draft — LocalGovBench v0.2.0

**Status:** draft for user review — **do not publish yet**  
**Previous version DOI (v0.1.0 only):** `10.5281/zenodo.20543779`  
**Concept DOI:** **USER CONFIRMATION REQUIRED** — not verified from repository evidence; do not invent or guess.

## Proposed upload fields

| Field | Proposed value |
|-------|----------------|
| upload_type | `software` |
| title | LocalGovBench v0.2.0: Disclosure Affordances in Public AI and Algorithm Registers |
| creators | César Andrés (ORCID `0009-0001-8968-3404`); affiliation CRIA-BDHS Research Group, Higher Polytechnic School of Technology and Science, Universidad Camilo José Cela, Madrid, Spain; email `cesar.andress@ucjc.edu` |
| version | `0.2.0` |
| publication_date | `YYYY-MM-DD` — **placeholder; set on publish day** |
| license | MIT |
| language | eng |
| access_rights | open |
| communities | **USER CONFIRMATION** (none assumed) |
| subjects | artificial intelligence; public administration; open government data; algorithmic transparency |

## Description (proposed)

LocalGovBench v0.2.0 is a reproducible research software deposit for studying **schema disclosure affordance** in public AI and algorithm registers using **Disclosure Functions v1**.

This version is a **framework transition** from the historical LocalGovBench v0.1.0 design (Governance Readiness Benchmark for sovereign LLM deployments; DOI `10.5281/zenodo.20543779`). The v0.1.0 materials remain available for provenance and are **not** the active analytical framework of v0.2.0.

The deposit includes:

- the Disclosure Functions v1 normative catalogue and anti-overcredit rules;
- field-normalization, candidate-mapping, applicability, and realization specifications;
- a corpus lock over **7,434** public inventory records and an observed-field **schema inventory**;
- an applicability-aware **human schema-coding** system (codebook, templates, validation utilities);
- **double-coding and adjudication** infrastructure and an IRR preparation plan;
- a **33-unit** pilot coding manifest.

v0.2.0 does **not** include completed human coding results, inter-rater reliability statistics, record-level realization tables, affordance–realization gap figures, jurisdiction rankings, readiness/maturity scores, shortfall scores, compliance scores, or a finished journal manuscript. It is a framework-transition software release, not a completed empirical-results release.

## Keywords

`artificial intelligence`, `public sector`, `algorithm registers`, `AI inventories`, `algorithmic transparency`, `disclosure affordance`, `schema coding`, `reproducibility`

## Related identifiers

| Relation | Identifier | Note |
|----------|------------|------|
| isNewVersionOf | 10.5281/zenodo.20543779 | Previous **version** DOI (v0.1.0 only) |
| isSupplementTo | https://github.com/cesar-andress/localgovbench | GitHub repository |
| cites / isCitedBy | — | Companion paper DOI: **USER CONFIRMATION** (do not invent) |
| Concept DOI | — | **USER CONFIRMATION** if a Zenodo concept DOI exists |

## Notes for deposit

- Mint a **new version DOI** for v0.2.0; do not overwrite or repurpose `10.5281/zenodo.20543779`.
- Prefer uploading a release archive from the Git tag (once created) rather than an unclean working tree.
- Exclude secrets, `.env`, caches, and confidential Delphi response YAMLs.
- Include affordance specification + coding artefacts; label GRB/v0.1 paths as legacy in documentation.

## Included artefacts (proposed)

- Affordance specification + coding layers and tests  
- Build scripts, root README, CITATION.cff, CHANGELOG, LICENSE  
- `docs/releases/` preparation set  
- Legacy code/docs clearly labelled (**USER CONFIRMATION** on full-tree vs DF-focused archive)

## Excluded artefacts (proposed)

- Secrets, credentials, `.env`  
- Virtualenvs, caches, temporary files  
- Confidential Delphi response YAMLs  
- Unpublished manuscript material unless user explicitly includes it  

## Draft `.zenodo.json` (review only)

A machine-readable draft is provided at [`zenodo_v0.2.0.draft.json`](zenodo_v0.2.0.draft.json). It must not be treated as a published deposit.
