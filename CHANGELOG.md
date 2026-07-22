# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] — Unreleased (documentation/metadata draft)

Framework **transition** release preparation. Not a completed empirical-results release.  
**Conceptual incompatibility with v0.1.0:** the active measurement target is schema disclosure affordance (Disclosure Functions v1), not governance readiness / GRB maturity scoring.

### Added

- Disclosure Functions v1 **specification layer** (`localgovbench_measurement_validation/affordance/`): corpus lock (7,434 records), schema inventory, function catalogue, candidate maps, applicability, realization rules, linkage types (milestone `aa8ea3d`)
- Disclosure Functions v1 **schema coding layer**: codebook, coding template (55 units), pilot manifest (33 units), validation utilities, double-coding and adjudication protocols (milestone `ac2669c`)
- Release preparation docs under `docs/releases/` (positioning, audit, Zenodo draft metadata, GitHub release notes draft, manifest, readiness)
- Active-documentation claim checks (tests)

### Changed

- Root `README.md`, `CITATION.cff`, and `pyproject.toml` repositioned for Disclosure Functions v1
- Package version provisional **0.2.0**
- Keywords and abstracts remove readiness/maturity as the active claim

### Deprecated

- Treating GRB / 25-criterion readiness scoring as the active paper framework
- Unqualified public claims that LocalGovBench currently measures governance readiness, maturity, sovereign LLM deployment readiness, shortfall scores, jurisdiction rankings, or compliance scores

### Removed

- Nothing deleted from the historical v0.1.0 archive surface; legacy docs labelled instead

### Fixed

- Public entrypoint no longer presents v0.1.0 GRB outputs as current primary outputs

### Reproducibility

```bash
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_coding_layer.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests -q
```

### Documentation

- LEGACY banners on v0.1.0 / GRB documentation
- Active affordance README remains the SoT for DF v1

### Known limitations

- Human coding, IRR, realization rates, and gap analysis not completed
- No Zenodo DOI for v0.2.0 yet (do not reuse 10.5281/zenodo.20543779 as current version DOI)
- Formal Git tag / GitHub Release not created in this preparation step

## [0.1.0] — 2026-06-04

### Added

- **v0.1.0 initial research artifact** — LocalGovBench framework (five dimensions, 25 criteria), scoring utilities, documentation, and repository validation script
- **GRB instrument** — Governance Readiness Benchmark experiment (six dimensions, 54 indicators, readiness bands, safeguard G1)
- **Synthetic examples** — v0.1 and GRB example assessments; validation benchmark cases; GRB inter-rater evidence packs
- **Sensitivity analysis** — GRB structural sensitivity (≥150 profiles) and legacy 100-profile sweep
- **Validation package** — Content validity templates, inter-rater study materials, discriminant validity cases, Cohen's κ and Krippendorff's α for v0.1; GRB Fleiss' κ and disagreement tables
- **Ollama evidence extraction prototype** — Candidate evidence proposals only (no automated scoring)

### Added (post-checklist)

- Construct traceability package: literature mapping for 25 v0.1 criteria, CSV, validation script
- **LLM model benchmark** — Compare Ollama models on gold-labelled evidence extraction tasks (`scripts/run_llm_model_benchmark.py`)

### Documentation

- Pre-release package: artifact description, reproducibility guide, v0.1.0 release checklist
- Construct traceability guide (`docs/construct_traceability.md`)
- Empirical validation protocol, GRB inter-rater reliability protocol, Zenodo release guide

### Notes

- Instrument v0.1 and GRB specification are **frozen** for this release
- Bundled scores are **synthetic**; empirical field validation is **pending**
- Zenodo DOI: [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)

[0.2.0]: https://github.com/cesar-andress/localgovbench/tree/main
[0.1.0]: https://github.com/cesar-andress/localgovbench/releases/tag/v0.1.0
