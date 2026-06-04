# LocalGovBench

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Project purpose

**LocalGovBench** is an open research artifact for studying **local and on-premise large language model (LLM) governance** in European public sector organizations. It provides:

- A version **0.1** governance framework (five dimensions, 25 criteria)
- Maturity scoring utilities (0–4 scale)
- Indicative mappings to EU AI Act and GDPR **themes** (not legal compliance assessments)
- Documentation and tooling intended for a future **Zenodo** archival release
- A **scientific validation package** (content validity templates, IRR, κ/α metrics)

The artifact supports structured self-assessment, document coding, and empirical validation studies. It does **not** certify legal conformity.

## Relation to the GIQ paper

This repository accompanies work submitted to the **GIQ 2026** track, tentatively titled:

*Towards a Local AI Governance Framework for European Public Sector Organizations*

The paper may describe motivation, related work, and research design. **This repository holds the instrument and reproducibility materials**; it does not include the manuscript. When the paper is published, update [CITATION.cff](CITATION.cff) and the citation section below with the official DOI.

## Repository scope

| In scope | Out of scope (v0.1) |
|----------|---------------------|
| Framework definitions and checklist generation | Published field-study benchmark scores |
| Scientific validation package (templates, IRR tools) | Completed multi-site empirical validation |
| Synthetic example assessments | Real organizational or citizen data |
| Policy theme mappings (indicative) | Legal advice or conformity assessment |
| Tests and validation scripts | Production system integrations |
| Zenodo-oriented release documentation | Manuscript drafts and reviewer materials |

## What is included

- **Framework (v0.1):** `localgovbench/framework/` — dimensions, criteria, checklist, scoring
- **Evaluation helpers:** `localgovbench/evaluation/` — rubric labels, assessment validators
- **Documentation:** `docs/` — framework, [benchmark specification](docs/benchmark_specification.md), [manuscript positioning](docs/manuscript_positioning.md), methodology, governance dimensions, AI Act/GDPR mappings, Zenodo guide
- **Prompt templates:** `prompts/` — structured assessment prompts (research instruments)
- **Synthetic example:** `examples/example_assessment.yaml`
- **Validation package:** `validation/` — content validity, expert review, inter-rater study, reliability metrics
- **GRB experiment (54 indicators):** `localgovbench/grb/`, `examples/grb/` — extended sensitivity / IRR pilot
- **Data placeholders:** `data/raw/`, `data/processed/`, `data/templates/`

### Empirical validation (v0.1 instrument frozen)

| Step | Command / path |
|------|----------------|
| **Protocol** | [docs/validation_protocol.md](docs/validation_protocol.md) |
| Content validity (I-CVI, CVR) | `python scripts/run_content_validity_analysis.py` |
| Inter-rater reliability (κ, α) | `python scripts/run_inter_rater_analysis.py` |
| Discriminant validity | `python scripts/run_discriminant_validity.py` |
| Validation benchmark report | `python scripts/generate_validation_report.py` |
| Package index | [validation/README.md](validation/README.md) |

Bundled cases under `validation/benchmark_cases/` and `validation/ratings/` are **synthetic** — replace with field data before publication claims.

> **Warning:** All bundled assessment scores and metadata in `examples/` are **synthetic** unless a future release explicitly states otherwise.

## What is not included

- Completed field-study expert panel results (templates and analysis scripts only)
- Peer-reviewed confirmation of psychometric validity in a published study
- Unpublished paper PDFs, reviewer correspondence, or private notes
- Credentials, `.env` files, or identifiable public sector records

## Quick start

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/validate_repository.py
python scripts/run_example_assessment.py
python scripts/run_content_validity_analysis.py \
  --input validation/content_validity/indicator_relevance_survey_results.example.yaml
python scripts/run_inter_rater_analysis.py
python scripts/run_discriminant_validity.py
python scripts/generate_validation_report.py
pytest
```

## Repository layout

| Path | Purpose |
|------|---------|
| `localgovbench/` | Core Python package |
| `docs/` | Framework, methodology, regulatory mappings, Zenodo guide |
| `data/` | Data placeholders for future empirical releases |
| `prompts/` | Assessment prompt templates |
| `examples/` | Synthetic runnable examples |
| `tests/` | Unit tests |
| `validation/` | Scientific validation study templates and synthetic IRR cases |
| `scripts/` | Assessment, validation, and analysis scripts |

See [docs/zenodo_release.md](docs/zenodo_release.md) for the publication checklist.

## Citation

### Software (repository / Zenodo)

When citing this artifact, use [CITATION.cff](CITATION.cff). After Zenodo deposit, replace the placeholder DOI:

```bibtex
@software{localgovbench2026,
  author    = {[Author names to be added]},
  title     = {LocalGovBench: A Research Framework for Local AI Governance in European Public Sector Organizations},
  year      = {2026},
  version   = {0.1.0},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://github.com/PLACEHOLDER/localgovbench}
}
```

### Companion paper (placeholder)

```bibtex
@article{giq2026localai,
  author  = {[Authors to be added]},
  title   = {Towards a Local AI Governance Framework for European Public Sector Organizations},
  journal = {[Venue to be added]},
  year    = {2026},
  note    = {Manuscript in preparation}
}
```

## Reproducibility statement

Researchers should cite the **exact Git tag and Zenodo version** used in analysis. For the computational instrument:

1. Install with `pip install -e ".[dev]"` from the tagged commit.
2. Run `pytest` and `python scripts/validate_repository.py`.
3. Record the Zenodo archive checksum listed in the release notes (see [docs/zenodo_release.md](docs/zenodo_release.md)).

Empirical protocols (document analysis, expert validation, case studies, inter-rater agreement) are described in [docs/methodology.md](docs/methodology.md). Those steps are outside the automated tests in this repository.

## Ethical and legal disclaimer

- This project provides a **research instrument** for describing governance practices around on-premise LLMs in public institutions.
- Regulatory mappings in `docs/ai_act_mapping.md` and `docs/gdpr_mapping.md` are **indicative** and **not legal advice**.
- Maturity scores **do not** indicate GDPR or AI Act compliance.
- Do not commit personal data, identifiable case materials, or confidential procurement documents to this repository.
- Empirical studies require appropriate ethics approval, lawful basis for processing, and organizational authorization.

## Status

**Research preview (v0.1)** — Instrument **frozen**; full empirical validation package (content validity, IRR, discriminant cases, κ/α) ready for field studies. Bundled outputs are **synthetic** until expert and municipal data are collected.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Released under the [MIT License](LICENSE).
