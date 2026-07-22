# LocalGovBench

**Version v0.2.0** — Disclosure Affordance Framework for Public AI and Algorithm Registers  
**Canonical DOI:** [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)  
**Historical archive (v0.1.0):** [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21500899.svg)](https://doi.org/10.5281/zenodo.21500899)
[![Historical DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.20543779.svg)](https://doi.org/10.5281/zenodo.20543779)

> **Historical notice.** v0.1.0 represented the original Governance Readiness Benchmark design. It is retained as a historical snapshot but is not the active analytical framework. Provenance archive: [DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779).

Public positioning: [`docs/releases/public_positioning_v0.2.0.md`](docs/releases/public_positioning_v0.2.0.md).

## 1. What LocalGovBench currently is

LocalGovBench is a **reproducible research repository** for studying:

- **schema disclosure affordance** in public AI / algorithm registers;
- **Disclosure Functions v1** (what a published schema can host);
- structured **human schema coding**;
- planned **record-level realization** and the **affordance–realization gap**;
- **applicability-aware** cross-source comparison;

**without** jurisdiction rankings, readiness/maturity scores, shortfall scores, compliance scores, or composite indices.

## 2. What changed after v0.1.0

| | v0.1.0 (historical) | v0.2.0 (active) |
|--|---------------------|-----------------|
| Focus | Governance readiness / GRB for sovereign LLM programmes | Disclosure affordances of official register schemas |
| Unit | Programme dossier / maturity criteria | Schema × disclosure function (+ planned record realization) |
| Zenodo | [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779) | [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899) |

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
scripts/build_affordance_*.py           # ACTIVE: regenerate artefacts
docs/releases/                          # ACTIVE: v0.2.0 release documentation
docs/*.md, validation/, examples/       # LEGACY — v0.1.0 (labelled)
```

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

## 8. Reproducibility commands (active path)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_coding_layer.py
pytest -m "not integration"
```

## 8b. Supplementary materials (paper package)

Publication-facing supplements **A–J** (corpus, inventory, Disclosure Functions v1, coding, validation, pipeline, reproducibility, structure, citation, versions) are indexed at:

[`docs/supplements/README.md`](docs/supplements/README.md)

They wrap existing frozen artefacts only and do **not** invent coding results, IRR, realization rates, or gaps.

## 9. Current limitations

- Human pilot coding not executed for publication  
- IRR / adjudication outcomes not reported  
- Record realization tables and gap figures not completed  
- Companion manuscript not claimed finished  

## 10. Next research phases

1. Human pilot coding → adjudication → IRR  
2. Full schema coding where planned  
3. Record-level realization and affordance–realization gap analysis  
4. Manuscript finalisation  

## 11. How to cite

**Preferred software citation (active):**

LocalGovBench v0.2.0: Disclosure Affordance Framework for Public AI and Algorithm Registers.  
https://doi.org/10.5281/zenodo.21500899

Zenodo record title: *LocalGovBench: Disclosure Affordances in Public AI and Algorithm Registers* (v0.2.0).

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

Metadata: [`CITATION.cff`](CITATION.cff).

## 12. Historical and legacy material

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

**v0.2.0** — active framework = Disclosure Functions v1 ([DOI 10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)).  
**v0.1.0** — historical Governance Readiness Benchmark ([DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)).

## Contributing / License

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [LICENSE](LICENSE) (MIT).
