# Contributing to LocalGovBench

Thank you for your interest in this research artifact. Contributions that improve reproducibility, documentation clarity, and test coverage are especially welcome.

## Scope

This repository is intended for:

- Framework definitions (dimensions, checklists, scoring)
- Documentation and regulatory mapping references
- Synthetic examples and validation scripts
- Tests and lightweight tooling

Please **do not** submit:

- Unpublished manuscript drafts or reviewer correspondence
- Private organizational data or identifiable records
- Non-synthetic empirical data without explicit consent and documentation

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python scripts/validate_repository.py
```

## Pull requests

1. Fork the repository and create a feature branch.
2. Keep changes focused and documented.
3. Add or update tests when changing framework logic.
4. Run `pytest` and `python scripts/validate_repository.py` before opening a PR.
5. Describe whether any data files are synthetic or derived from real sources.

## Versioning

Follow semantic versioning for releases. Update `CITATION.cff` version and `date-released` when tagging a Zenodo release (see `docs/zenodo_release.md`).

## Questions

Open a GitHub issue for bugs, documentation gaps, or collaboration proposals related to the public research artifact.
