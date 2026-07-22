# LocalGovBench

**Provisional version 0.2.0** — documentation and metadata preparation for the Disclosure Functions framework transition  
**Historical archive:** [v0.1.0 on Zenodo](https://doi.org/10.5281/zenodo.20543779)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.2.0--draft-orange.svg)](CHANGELOG.md)
[![Historical DOI v0.1.0](https://zenodo.org/badge/DOI/10.5281/zenodo.20543779.svg)](https://doi.org/10.5281/zenodo.20543779)

> **Historical notice.** **v0.1.0** represented the original **Governance Readiness Benchmark** design for sovereign LLM deployments. That design is retained for provenance ([DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)) but is **not** the active analytical framework.

## What LocalGovBench is now

LocalGovBench is a **reproducible research repository** for studying:

- **schema disclosure affordance** in public AI / algorithm registers;
- **Disclosure Functions v1** (what a published schema can host);
- structured **human schema coding**;
- planned **record-level realization** and the **affordance–realization gap**;
- **applicability-aware** cross-source comparison;

**without** jurisdiction rankings, readiness/maturity scores, shortfall scores, compliance scores, or composite indices.

## What changed after v0.1.0

| | v0.1.0 (historical) | v0.2.0 path (active) |
|--|---------------------|----------------------|
| Focus | Governance readiness / GRB for sovereign LLM programmes | Disclosure affordances of official register schemas |
| Unit | Programme dossier / maturity criteria | Schema × disclosure function (+ planned record realization) |
| Status | Frozen on Zenodo | Specification + coding layers implemented; empirical results not claimed complete |

## What Disclosure Functions v1 measures

**Schema disclosure affordance:** the extent to which a published official AI inventory schema provides dedicated or indirect fields capable of hosting a policy-derived disclosure function (an upper bound on possible disclosure — not transparency achieved, governance quality, or compliance).

Active catalogue: identity (descriptive), purpose, operational status, accountable body, data involvement, plus modules (oversight, risk/impact, legal basis, supplier, technical method, redress pointer).

## What the repository currently contains

### Active

| Path | Role |
|------|------|
| [`localgovbench_measurement_validation/affordance/`](localgovbench_measurement_validation/affordance/) | Disclosure Functions v1 specification + schema coding layer |
| [`scripts/build_affordance_specification.py`](scripts/build_affordance_specification.py) | Regenerate corpus lock + schema inventory |
| [`scripts/build_affordance_coding_layer.py`](scripts/build_affordance_coding_layer.py) | Regenerate codebook, coding template, pilot manifest |
| Frozen pilot corpus (local) | `pilot_public_satisfiability/data/pilot_programme_records.csv` (N=7,434; see corpus lock) |

### Legacy (labelled; retained for provenance)

| Path | Role |
|------|------|
| `localgovbench/framework/`, `localgovbench/grb/` | v0.1 / GRB software |
| `docs/*` (most files) | v0.1.0 instrument & GRB documentation — **LEGACY banners** |
| `validation/`, `examples/`, `data/benchmark/` | Historical validation / GRB materials |

## How to reproduce the specification layer

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3.12 scripts/build_affordance_specification.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests -q
```

See [`localgovbench_measurement_validation/affordance/README.md`](localgovbench_measurement_validation/affordance/README.md).

## How to use the schema coding layer

```bash
python3.12 scripts/build_affordance_coding_layer.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/coding/tests -q
```

Human coding uses:

- `affordance/coding/config/codebook_affordance_v1.md`
- `affordance/coding/templates/schema_coding_template_v1.csv`
- `affordance/coding/templates/pilot_coding_manifest_v1.csv`

Do **not** treat blank templates as study results. IRR, adjudication outcomes, realization rates, and gap figures are **not** completed in this preparation.

## What is not yet completed

- Full independent human schema coding and reported IRR
- Record-level realization tables and affordance–realization gap analysis
- Manuscript rewrite / journal submission package for the inventory study
- Formal Git tag `v0.2.0`, GitHub Release, and Zenodo deposit for v0.2.0

Draft release materials: [`docs/releases/`](docs/releases/).

## Citation (before formal v0.2.0 release)

Until a Zenodo version DOI for v0.2.0 is minted, cite the **Git commit** of this repository and, for the historical instrument only, the v0.1.0 archive:

- **Historical v0.1.0 DOI:** https://doi.org/10.5281/zenodo.20543779  
- **Software (current `main`):** cite commit hash + URL `https://github.com/cesar-andress/localgovbench`  
- Metadata: [`CITATION.cff`](CITATION.cff)

```bibtex
@software{localgovbench_v020_draft,
  author  = {Andrés, César},
  title   = {{LocalGovBench}: Disclosure Affordances in Public AI and Algorithm Registers},
  year    = {2026},
  version = {0.2.0-draft},
  url     = {https://github.com/cesar-andress/localgovbench},
  note    = {Provisional documentation for the Disclosure Functions v1 framework; not a completed empirical-results release}
}
```

For the frozen v0.1.0 readiness instrument only:

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

## Quick install / tests

```bash
pip install -e ".[dev]"
pytest -m "not integration"
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests -q
```

## Ethical and legal disclaimer

- This repository provides **research software and measurement specifications**.
- It does **not** certify GDPR/AI Act compliance or organisational readiness.
- Do not commit personal data, credentials, or confidential records.
- Empirical studies require appropriate ethics and organisational authorization.

## Status

**v0.2.0 (draft metadata)** — active framework = Disclosure Functions v1 (specification + schema coding).  
**v0.1.0** — historical Governance Readiness Benchmark, archived at [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779).

## Contributing / License

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [LICENSE](LICENSE) (MIT).
