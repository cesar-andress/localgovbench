# Zenodo Release Guide

This document describes how to publish LocalGovBench as a citable research artifact on [Zenodo](https://zenodo.org), typically via GitHub integration.

## Prerequisites

- Public GitHub repository (update URLs in `README.md`, `pyproject.toml`, and `CITATION.cff`)
- MIT License present (`LICENSE`)
- `CITATION.cff` metadata complete for software artifact
- All committed sample data clearly marked as **synthetic**

## Release checklist

1. **Version** — Bump `version` in `pyproject.toml` and `CITATION.cff`.
2. **Changelog** — Summarize changes since last tag in GitHub release notes.
3. **Tests** — Run `pytest` and `python scripts/validate_repository.py`.
4. **Tag** — Create an annotated Git tag, e.g. `v0.1.0`.
5. **GitHub release** — Publish release from tag; enable Zenodo-GitHub integration if configured.
6. **Zenodo record** — Verify metadata, upload archive, and copy DOI into `CITATION.cff` (`doi:` field) and `README.md`.

## Recommended Zenodo metadata

| Field | Suggested value |
|-------|-----------------|
| Upload type | Software |
| Title | LocalGovBench: … (match `CITATION.cff`) |
| License | MIT |
| Keywords | AI governance, public sector, EU, benchmark |
| Related identifiers | Link to paper DOI when available |

## What not to publish

- Private notes, drafts, or reviewer comments
- Non-anonymized field data without consent
- Credentials or environment files

## Archival integrity

- Use Zenodo's versioned DOI for each release.
- Keep `date-released` in `CITATION.cff` aligned with the Zenodo publication date.
- Document in release notes whether empirical datasets are included or still placeholders.

## Post-release

Update the preferred citation block in `CITATION.cff` when the companion paper is published, and add the paper DOI as a `related_identifiers` entry in Zenodo.
