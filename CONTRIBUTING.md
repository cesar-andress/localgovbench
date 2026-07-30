# Contributing to LocalGovBench

Thank you for your interest in this research artifact. Contributions that improve reproducibility, documentation clarity, and test coverage are especially welcome.

## Scope

**Active contributions** should align with Disclosure Functions v1 (schema disclosure affordance and schema coding). See the root [README.md](README.md) and [`docs/releases/public_positioning_v0.2.0.md`](docs/releases/public_positioning_v0.2.0.md).

This repository welcomes:

- Affordance specification and coding-layer improvements
- Documentation clarity for the active framework
- Tests and reproducibility tooling
- Carefully labelled historical (v0.1.0 / GRB) maintenance only when needed for provenance

Please **do not** submit:

- Unpublished manuscript drafts or reviewer correspondence
- Private organizational data, credentials, or identifiable records
- Non-synthetic empirical data without explicit consent and documentation
- Changes that reframe the **active** project as a governance readiness / maturity / ranking instrument

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -m "not integration"
python scripts/validate_repository.py
```

## Pull requests

1. Fork the repository and create a feature branch.
2. Keep changes focused and documented.
3. Add or update tests when changing affordance or coding logic.
4. Run `pytest -m "not integration"` and `python scripts/validate_repository.py` before opening a PR.
5. Describe whether any data files are synthetic or derived from public sources.

Manuscript bibliography verification (OpenAlex) lives in the **private paper repository** (`../paper`): `make bib-verify-offline` is deterministic and CI-safe there; `make bib-verify-live` is optional and requires `OPEN_ALEX_KEY`. Do **not** wire live OpenAlex calls into this software package’s default test suite.

## Versioning

Follow semantic versioning for releases. Update `CITATION.cff` version and `date-released` when tagging a Zenodo release. For v0.2.0 drafts see [`docs/releases/`](docs/releases/). Historical v0.1.0 Zenodo steps remain in `docs/zenodo_release.md` (**LEGACY — v0.1.0**).

## Questions

Open a GitHub issue for bugs, documentation gaps, or collaboration proposals related to the public research artifact.
