# LocalGovBench

**Published software:** **v1.0.0** — first stable public release accompanying the submitted manuscript  
**Prior published:** v0.2.0 — DOI [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)  
**Historical archive (v0.1.0):** [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)  
**Specification / coding / pipeline:** 1.0.0  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue.svg)](CHANGELOG.md)
[![Prior DOI v0.2.0](https://zenodo.org/badge/DOI/10.5281/zenodo.21500899.svg)](https://doi.org/10.5281/zenodo.21500899)
[![Historical DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.20543779.svg)](https://doi.org/10.5281/zenodo.20543779)

> **Historical notice.** v0.1.0 represented the original Governance Readiness Benchmark design. It is retained as a historical snapshot but is not the active analytical framework. Provenance archive: [DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779).

> **v1.0.0 notice.** This tag freezes the public repository for manuscript submission and Zenodo archival. The Zenodo **version DOI for v1.0.0** is assigned automatically when the GitHub/Zenodo integration deposits this tag. Until that DOI appears on Zenodo, cite the Git tag `v1.0.0` and retain prior DOIs for earlier deposits.

## 1. What LocalGovBench currently is

LocalGovBench is a **reproducible research repository** for studying:

- **documentary evidence availability** from official public AI / algorithm inventory schemas (frozen public-satisfiability pilot; see §5b);
- **schema disclosure affordance** via **Disclosure Functions v1**;
- structured **human schema coding**;
- planned **record-level realization** and the **affordance–realization gap**;
- **applicability-aware** cross-source comparison;

**without** jurisdiction rankings, readiness/maturity scores, compliance scores, or composite indices.

## 2. What changed after v0.1.0

| | v0.1.0 (historical) | v0.2.0 | v1.0.0 (this release) |
|--|---------------------|--------|------------------------|
| Focus | Governance readiness / GRB | Disclosure affordances (DF v1) | Manuscript-stable public archive (DF + frozen pilot outputs) |
| Zenodo | [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779) | [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899) | Minted on deposit of tag `v1.0.0` |

## 3. What Disclosure Functions v1 measures

**Schema disclosure affordance:** the extent to which a published official AI inventory schema provides dedicated or indirect fields capable of hosting a policy-derived disclosure function (an upper bound on possible disclosure — not transparency achieved, governance quality, or compliance).

Active catalogue: identity (descriptive), purpose, operational status, accountable body, data involvement, plus modules (oversight, risk/impact, legal basis, supplier, technical method, redress pointer).

## 4. Affordance vs realization

| Layer | Question | Status in this repo |
|-------|----------|---------------------|
| **Schema affordance** | Can the published schema host the function? | Specification + coding system ready |
| **Record realization** | Do published records actually disclose it? | Specified; empirical tables **not** completed |
| **Affordance–realization gap** | Where does realization fall short of affordance? | Future analysis stage |

## 5. Current repository architecture

```
localgovbench/                          # package (includes legacy framework/grb code)
localgovbench_measurement_validation/
  affordance/                           # ACTIVE: DF v1 specification + coding
  pilot_public_satisfiability/          # FROZEN manuscript pilot (2026-06-24)
scripts/build_affordance_*.py           # ACTIVE: regenerate DF artefacts
scripts/*public_satisfiability*         # FROZEN pilot pipeline (do not re-run for release)
docs/releases/                          # Release documentation
docs/supplements/                       # Publication supplements A–J
paper_assets/                           # Manuscript table/figure scaffolds
paper_data_policy/                      # Freeze notes for the pilot package
```

## 5b. Manuscript empirical freeze (public satisfiability pilot)

Frozen analytical summaries for the documentary-evidence availability study live under:

[`localgovbench_measurement_validation/pilot_public_satisfiability/`](localgovbench_measurement_validation/pilot_public_satisfiability/)

- **Freeze date:** 2026-06-24 (`paper_data_policy/results_freeze.md`)
- **Tracked:** `outputs/*.csv`, reports, figures, mapping rules, criteria YAML, source registry
- **Not redistributed in git by default:** aggregate `data/pilot_programme_records.csv` (~27 MB; reconstruct via `scripts/build_pilot_corpus.py` when licensing/network allow; verify with `scripts/verify_pilot_corpus.py`)

Do **not** regenerate pilot outputs for this release. Numbers are frozen.

## 6. Phase 1 — specification layer (complete)

Implemented (milestone commit `aa8ea3d`):

- Disclosure Functions v1 YAML catalogue  
- Field normalization, candidates, applicability, realization rules, linkage types  
- Corpus lock over **7,434** public inventory records + observed-field schema inventory  

```bash
python3.12 scripts/build_affordance_specification.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests -q
```

Details: [`localgovbench_measurement_validation/affordance/README.md`](localgovbench_measurement_validation/affordance/README.md).

## 7. Phase 2 — schema-coding layer (complete)

Implemented (milestone commit `ac2669c`):

- Codebook, labels, coding template (**55** units), pilot manifest (**33** units)  
- Validation utilities; double-coding and adjudication protocols  
- IRR **plan** only (no calculated IRR results)

```bash
python3.12 scripts/build_affordance_coding_layer.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/coding/tests -q
```

Do **not** treat blank templates as study results.

## 8. Reproducibility commands (active DF path)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_coding_layer.py
pytest -m "not integration"
python3.12 scripts/validate_repository.py
```

## 8b. Supplementary materials (paper package)

Publication-facing supplements **A–J** are indexed at:

[`docs/supplements/README.md`](docs/supplements/README.md)

## 8c. Manuscript paper assets (tables/figures scaffolds)

[`paper_assets/README.md`](paper_assets/README.md) · [`paper_assets/paper_asset_manifest.md`](paper_assets/paper_asset_manifest.md)

```bash
python3.12 paper_assets/scripts/generate_all_paper_assets.py
```

## 9. Current limitations

- Aggregate pilot corpus CSV not in git by default (size/licensing)  
- Human DF pilot coding not executed for publication Results  
- IRR / adjudication outcomes not reported for DF coding  
- Record realization tables and gap figures not completed  
- Zenodo version DOI for **v1.0.0** appears after deposit of this tag  

## 10. How to cite

**This release (v1.0.0):** cite GitHub tag [`v1.0.0`](https://github.com/cesar-andress/localgovbench/releases/tag/v1.0.0) and, once minted, the Zenodo version DOI shown on the deposit page. Metadata: [`CITATION.cff`](CITATION.cff).

**Prior software citation (v0.2.0):**

```bibtex
@software{localgovbench_v020,
  author  = {Andrés, César},
  title   = {{LocalGovBench}: Disclosure Affordances in Public AI and Algorithm Registers},
  year    = {2026},
  version = {0.2.0},
  doi     = {10.5281/zenodo.21500899},
  url     = {https://doi.org/10.5281/zenodo.21500899},
  note    = {Disclosure Affordance Framework; Disclosure Functions v1}
}
```

**Historical v0.1.0 only** (Governance Readiness Benchmark archive — not the active analytical framework):

```bibtex
@software{localgovbench_v010,
  author  = {Andrés, César},
  title   = {{LocalGovBench} v0.1.0: Governance Readiness Benchmark for Sovereign LLM Deployments},
  year    = {2026},
  version = {0.1.0},
  doi     = {10.5281/zenodo.20543779},
  url     = {https://doi.org/10.5281/zenodo.20543779},
  note    = {Historical archive; not the active analytical framework}
}
```

## 11. Historical and legacy material

| Path | Role |
|------|------|
| `localgovbench/framework/`, `localgovbench/grb/` | v0.1 / GRB software (retained) |
| `docs/*` (most files) | v0.1.0 instrument & GRB documentation — **LEGACY — v0.1.0** banners |
| `validation/`, `examples/`, `data/benchmark/` | Historical validation / GRB materials |

Do not describe deprecated GRB outputs as current outputs.

## Quick install / tests

```bash
pip install -e ".[dev]"
pytest -m "not integration"
```

## Ethical and legal disclaimer

- This repository provides **research software and measurement specifications**.
- It does **not** certify GDPR/AI Act compliance or organisational readiness.
- Do not commit personal data, credentials, or confidential records.
- Empirical studies require appropriate ethics and organisational authorization.

## Status

**v1.0.0** — first stable public release for manuscript submission / Zenodo archival.  
**v0.2.0** — prior Disclosure Functions deposit ([DOI 10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)).  
**v0.1.0** — historical Governance Readiness Benchmark ([DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)).

## Contributing / License

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [LICENSE](LICENSE) (MIT).
