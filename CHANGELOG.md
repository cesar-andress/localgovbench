# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased] — 0.2.1 candidate

Release-engineering and tip completeness relative to published **v0.2.0**.  
**Not published.** Future DOI placeholder: `10.5281/zenodo.NEXT_DOI_TBD`.  
Published v0.2.0 (DOI `10.5281/zenodo.21500899`) remains unchanged.

### Added

- Phase 3 experiment pipeline and documentation
- Pilot Round 01 launch package (blank independent coder packets)
- Supplements A–J and `paper_assets/` Methods scaffolds (no fabricated Results)
- Corpus verification script and reproducibility docs
- GitHub Actions CI for the active Disclosure Functions stack
- Legacy/non-DF notices on results-looking directories
- Release candidate notes: `docs/releases/NEXT_RELEASE.md`

### Fixed

- Runtime package version aligned with `pyproject.toml` (0.2.1 tip)
- Release documentation contradictions (published v0.2.0 vs unreleased main)
- Pilot package relative link; portable checksum paths; portable corpus path field
- PyYAML declared as a runtime dependency
- Adjudication merge no longer treats confidence/rationale-only diffs as substantive disagreements
- Repository validator coverage for the active DF stack

### Known limitations

- Aggregated corpus CSV not distributed in git by default
- No human coding Results / IRR / realization / gaps
- Next Zenodo deposit not minted

## [0.2.0] — 2026-07-23

Framework **transition** release. Not a completed empirical-results release.  
**Conceptual incompatibility with v0.1.0:** the active measurement target is schema disclosure affordance (Disclosure Functions v1), not governance readiness / GRB maturity scoring.  
**Canonical DOI:** [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)  
**Zenodo record title:** LocalGovBench: Disclosure Affordances in Public AI and Algorithm Registers  
**Release title:** LocalGovBench v0.2.0: Disclosure Affordance Framework for Public AI and Algorithm Registers

### Added

- Disclosure Functions v1 **specification layer** (`localgovbench_measurement_validation/affordance/`): corpus lock (7,434 records), schema inventory, function catalogue, candidate maps, applicability, realization rules, linkage types (milestone `aa8ea3d`)
- Disclosure Functions v1 **schema coding layer**: codebook, coding template (55 units), pilot manifest (33 units), validation utilities, double-coding and adjudication protocols (milestone `ac2669c`)
- Release preparation docs under `docs/releases/` (positioning, audit, Zenodo draft metadata, GitHub release notes draft, manifest, readiness)
- Active-documentation claim checks (tests)

### Changed

- Root `README.md`, `CITATION.cff`, and `pyproject.toml` repositioned for Disclosure Functions v1
- Package version **0.2.0** (published)
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
- Do not reuse historical DOI 10.5281/zenodo.20543779 as the current version DOI

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

[0.2.0]: https://doi.org/10.5281/zenodo.21500899
[0.1.0]: https://github.com/cesar-andress/localgovbench/releases/tag/v0.1.0
