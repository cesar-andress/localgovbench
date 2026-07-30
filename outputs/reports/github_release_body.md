## LocalGovBench v1.0.0 — Stable Reproducibility Release

Public research software for measuring **documentary evidence availability** in official public AI / algorithm inventory schemas: how far native published fields align with a fixed evidence-requirement catalogue, under frozen mapping rules.

### Purpose

This repository archives the companion software, configuration, frozen pilot outputs, and reproducibility scripts for the LocalGovBench empirical package used in the manuscript:

*What Public AI Inventories Disclose: Documentary Evidence Availability in Digital-Government Transparency Infrastructures*

(target venue: *Information Polity*).

It is a measurement and reproducibility artefact. It does **not** provide governance readiness scores, maturity indices, jurisdiction rankings, or legal compliance conclusions.

### Software version

- **Version:** 1.0.0
- **Git tag:** `v1.0.0` (this Release)
- **Compatibility:** Python 3.12 (see `pyproject.toml`)

### Archival DOI and citation

**Canonical archive:** [https://doi.org/10.5281/zenodo.21701861](https://doi.org/10.5281/zenodo.21701861)

Please cite the Zenodo version DOI and this tag when reusing the software or frozen pilot package. See `CITATION.cff` in the repository root.

Authors: César Andrés (corresponding); David Martín-Moncunill.

### Reproducibility

- Frozen public-satisfiability pilot outputs under `localgovbench_measurement_validation/pilot_public_satisfiability/` (empirical freeze **2026-06-24**; LocalGovBench **v0.1** requirement catalogue; \(N = 7{,}434\) programme records as observational volume).
- Authoritative numerics: `paper_data_policy/results_freeze.md`.
- Aggregate corpus CSV is intentionally outside git by default; rebuild/verify with `scripts/build_pilot_corpus.py` and `scripts/verify_pilot_corpus.py` when needed.
- Repository structure check: `python scripts/validate_repository.py`.

### Validation summary (as of tag tip)

- Offline software test suite: **246 passed** (`pytest -m "not integration"`; integration tests skipped without live services).
- Repository validation: **passed**.
- GitHub Actions CI on the tagged tip: **passed**.
- Active manuscript bibliography checked against OpenAlex/Crossref (live verification; grey literature noted where OpenAlex has no work record).
- Reproducibility package included in this archive (scripts, frozen outputs, supplements index, citation metadata).

Historical deposits (v0.2.0 / v0.1.0) remain available on Zenodo for provenance only and are not the canonical citation for this release.
