# LocalGovBench

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**LocalGovBench** is an early-stage, open research artifact supporting work on local AI governance for European public sector organizations. It provides a lightweight framework, scoring utilities, and benchmark scaffolding aligned with the paper *Towards a Local AI Governance Framework for European Public Sector Organizations*.

> **Status:** This repository is a **research preview**. APIs, dimensions, and sample data may change before a formal Zenodo release. Empirical datasets and evaluation results will be added in later releases.

## What is included

- A **governance framework** with dimensions, checklists, and scoring helpers (`localgovbench/framework`)
- **Evaluation** rubrics and validators (`localgovbench.evaluation`)
- **Documentation** on methodology, governance dimensions, and regulatory mappings (`docs/`)
- **Prompt templates** for structured assessments (`prompts/`)
- **Synthetic example** assessments and data placeholders (`examples/`, `data/`)

## What is not included (yet)

- Real organizational or citizen data
- Peer-reviewed benchmark scores from field studies
- Production integrations with case management or procurement systems

All sample files in `examples/` and placeholder paths under `data/` are **synthetic** unless explicitly labeled otherwise in file headers or release notes.

## Quick start

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python scripts/run_example_assessment.py
python scripts/validate_repository.py
pytest
```

## Repository layout

| Path | Purpose |
|------|---------|
| `localgovbench/` | Core Python package |
| `docs/` | Framework and methodology documentation |
| `data/` | Data placeholders (raw, processed, templates) |
| `prompts/` | Assessment prompt templates |
| `examples/` | Runnable synthetic examples |
| `tests/` | Unit tests |
| `scripts/` | Utility scripts |

See [docs/zenodo_release.md](docs/zenodo_release.md) for publication and versioning guidance.

## Citation

If you use this artifact, please cite the repository (see [CITATION.cff](CITATION.cff)). A Zenodo DOI will be added when the first release is published.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

This project is released under the [MIT License](LICENSE).
