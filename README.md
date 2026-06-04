# LocalGovBench

**Version 0.1.0** — research preview (pre-release for GitHub and Zenodo)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)

## Project purpose

**LocalGovBench** is an open research artifact for studying **local and on-premise large language model (LLM) governance** in European public sector organizations. It provides:

- A version **0.1.0** governance framework (five dimensions, 25 criteria)
- Maturity scoring utilities (0–4 scale)
- Indicative mappings to EU AI Act and GDPR **themes** (not legal compliance assessments)
- Documentation and tooling for **Zenodo** archival release
- A **scientific validation package** (content validity templates, IRR, κ/α metrics)
- A **GRB experiment** (54 indicators): synthetic validation, sensitivity analysis, inter-rater reliability pilot
- An **Ollama evidence extraction prototype** (candidate evidence only — no auto-scoring)

The artifact supports structured self-assessment, document coding, and empirical validation studies. It does **not** certify legal conformity.

> **Empirical validation is pending.** v0.1.0 ships synthetic examples, templates, and analysis scripts. Do not treat bundled scores as field-study benchmarks.

### Release documentation

| Document | Description |
|----------|-------------|
| [docs/artifact_description.md](docs/artifact_description.md) | Purpose, scope, included/excluded materials, validation status |
| [docs/reproducibility.md](docs/reproducibility.md) | Exact commands to install, test, and rerun analyses |
| [docs/release_v0_1_checklist.md](docs/release_v0_1_checklist.md) | Pre-release checklist for GitHub and Zenodo |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [docs/construct_traceability.md](docs/construct_traceability.md) | Literature traceability for 25 v0.1 criteria |
| [docs/demo_walkthrough.md](docs/demo_walkthrough.md) | GRB end-to-end workflow demo (reproducible commands) |

## Relation to the GIQ paper

This repository accompanies work submitted to the **GIQ 2026** track, tentatively titled:

*Towards a Local AI Governance Framework for European Public Sector Organizations*

The paper may describe motivation, related work, and research design. **This repository holds the instrument and reproducibility materials**; it does not include the manuscript. When the paper is published, update [CITATION.cff](CITATION.cff) and the citation section below with the official DOI.

## Repository scope

| In scope | Out of scope (v0.1.0) |
|----------|------------------------|
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
- **GRB experiment (54 indicators):** `localgovbench/grb/`, `examples/grb/` — sensitivity analysis and inter-rater reliability pilot
- **Ollama prototype:** `localgovbench/llm/evidence_extraction.py`, `scripts/run_ollama_evidence_extraction.py`
- **Data placeholders:** `data/raw/`, `data/processed/`, `data/templates/`

### Empirical validation (v0.1 instrument frozen — field work pending)

| Step | Command / path |
|------|----------------|
| **Protocol** | [docs/validation_protocol.md](docs/validation_protocol.md) |
| Content validity (I-CVI, CVR) | `python scripts/run_content_validity_analysis.py` |
| Inter-rater reliability (κ, α) | `python scripts/run_inter_rater_analysis.py` |
| Discriminant validity | `python scripts/run_discriminant_validity.py` |
| Validation benchmark report | `python scripts/generate_validation_report.py` |
| Package index | [validation/README.md](validation/README.md) |

Bundled cases under `validation/benchmark_cases/` and `validation/ratings/` are **synthetic** — replace with field data before publication claims.

### GRB validation (frozen 54-indicator experiment — synthetic pilots complete)

| Step | Command / path |
|------|----------------|
| Sensitivity analysis | `python scripts/run_grb_sensitivity_analysis.py` |
| Inter-rater reliability | `python scripts/run_inter_rater_reliability.py` |
| IRR protocol | [docs/inter_rater_reliability_protocol.md](docs/inter_rater_reliability_protocol.md) |
| Pilot cases & ratings | `examples/grb/inter_rater/` |

GRB specification, indicators, scoring formula, and safeguards are **not modified** in these scripts.

### End-to-end workflow demo

Step-by-step commands (template → demo scores → readiness → optional Ollama): **[docs/demo_walkthrough.md](docs/demo_walkthrough.md)**.

Quick start after `pip install -e ".[dev]"`:

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template

python scripts/fill_demo_scores.py \
  --input outputs/demo_municipality/assessor_scoring_template.yaml \
  --output outputs/demo_municipality/assessor_scoring_completed.yaml

python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --scores outputs/demo_municipality/assessor_scoring_completed.yaml \
  --output-dir outputs/demo_municipality \
  --compute-score
```

> **Warning:** Demo scores from `fill_demo_scores.py` are **synthetic walkthrough placeholders**, not validation evidence. All bundled examples remain **synthetic** unless stated otherwise.

## What is not included

- Completed field-study expert panel results (templates and analysis scripts only)
- Peer-reviewed confirmation of psychometric validity in a published study
- Unpublished paper PDFs, reviewer correspondence, or private notes
- Credentials, `.env` files, or identifiable public sector records

## Quick start

Requires Python 3.11 or newer. Full command list: [docs/reproducibility.md](docs/reproducibility.md).

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -m "not integration"
python scripts/validate_repository.py
python scripts/run_example_assessment.py
```

## Repository layout

| Path | Purpose |
|------|---------|
| `localgovbench/` | Core Python package |
| `docs/` | Framework, methodology, regulatory mappings, release guides |
| `data/` | Data placeholders for future empirical releases |
| `prompts/` | Assessment prompt templates |
| `examples/` | Synthetic runnable examples |
| `tests/` | Unit tests |
| `validation/` | Scientific validation study templates and synthetic IRR cases |
| `scripts/` | Assessment, validation, and analysis scripts |

See [docs/zenodo_release.md](docs/zenodo_release.md) and [docs/release_v0_1_checklist.md](docs/release_v0_1_checklist.md) for publication steps.

## Citation

### Software (repository / Zenodo)

When citing this artifact, use [CITATION.cff](CITATION.cff):

```bibtex
@software{localgovbench2026,
  author    = {Andrés, César},
  title     = {LocalGovBench},
  year      = {2026},
  version   = {0.1.0},
  orcid     = {0009-0001-8968-3404},
  doi       = {10.5281/zenodo.TBD},
  url       = {https://github.com/PLACEHOLDER/localgovbench}
}
```

Replace `10.5281/zenodo.TBD` and the repository URL after deposit and public GitHub release.

### Companion paper (placeholder)

```bibtex
@article{giq2026localai,
  author  = {Andrés, César},
  title   = {Towards a Local AI Governance Framework for European Public Sector Organizations},
  journal = {[Venue to be added]},
  year    = {2026},
  note    = {Manuscript in preparation}
}
```

## Reproducibility statement

Researchers should cite the **exact Git tag (`v0.1.0`) and Zenodo version** used in analysis. See [docs/reproducibility.md](docs/reproducibility.md) for install and script commands, and [docs/release_v0_1_checklist.md](docs/release_v0_1_checklist.md) for archive checksum recording.

## Ethical and legal disclaimer

- This project provides a **research instrument** for describing governance practices around on-premise LLMs in public institutions.
- Regulatory mappings in `docs/ai_act_mapping.md` and `docs/gdpr_mapping.md` are **indicative** and **not legal advice**.
- Maturity scores **do not** indicate GDPR or AI Act compliance.
- Do not commit personal data, identifiable case materials, or confidential procurement documents to this repository.
- Empirical studies require appropriate ethics approval, lawful basis for processing, and organizational authorization.

## Status

**v0.1.0 pre-release** — Instrument **frozen**; synthetic validation tooling complete; **empirical field validation pending**. Ready for public GitHub and Zenodo deposit following the release checklist.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Released under the [MIT License](LICENSE).
