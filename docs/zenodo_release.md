# Zenodo Release Guide

This document describes how to publish LocalGovBench as a **citable, reproducible research artifact** on [Zenodo](https://zenodo.org), typically via GitHub integration.

## Prerequisites

- Public GitHub repository (update URLs in `README.md`, `pyproject.toml`, and `CITATION.cff`)
- [MIT License](../LICENSE) present in repository root
- `CITATION.cff` complete enough for software citation (authors, version, abstract)
- All sample data clearly marked **synthetic** where applicable

---

## Release checklist

**Primary checklist:** [release_v0_1_checklist.md](release_v0_1_checklist.md) (GitHub + Zenodo pre-release for v0.1.0).

Use the summary below or the linked document before creating a Zenodo record. Mark each item when complete.

### Documentation and metadata

- [ ] **README complete** — Purpose, scope, GIQ paper relation, reproducibility, disclaimers (see [README.md](../README.md))
- [ ] **License selected** — MIT (`LICENSE` file matches Zenodo license field)
- [x] **Citation file complete** — `CITATION.cff` author **César Andrés**, ORCID, affiliation, email, Zenodo DOI `10.5281/zenodo.20543779`

### Version control and quality

- [ ] **Version tag created** — Annotated Git tag (e.g. `v0.1.0`) matching `pyproject.toml` and `CITATION.cff`
- [ ] **Tests passing** — `pytest` succeeds on tagged commit
- [ ] **Structure validation** — `python scripts/validate_repository.py` succeeds

### Data and content hygiene

- [ ] **Synthetic/sample data clearly marked** — `metadata.synthetic: true` in examples; warnings in `data/README.md` and `examples/README.md`
- [ ] **No private data** — No personal data, credentials, or organizational identifiers in the archive
- [ ] **No manuscript drafts** — No paper PDFs, LaTeX sources, or internal drafts in the repository
- [ ] **No reviewer correspondence** — No peer-review files, rebuttals, or editorial comments

### Archival deposit

- [x] **DOI created through Zenodo** — https://doi.org/10.5281/zenodo.20543779 (v0.1.0; reflected in `CITATION.cff` and README)
- [ ] **Archive checksum stored** — SHA-256 (or Zenodo file hash) recorded in release notes or a `RELEASE.md` / GitHub release body for verification

### Optional but recommended

- [ ] Changelog or GitHub release notes summarizing changes since prior tag
- [ ] Related identifier for companion paper DOI (when available)
- [ ] Zenodo keywords aligned with `CITATION.cff`

---

## Step-by-step publication

1. Complete the checklist above on a clean working tree.
2. Bump `version` in `pyproject.toml` and `CITATION.cff`; set `date-released` to publication date.
3. Commit and push; create annotated tag: `git tag -a v0.1.0 -m "v0.1.0"`.
4. Push tag: `git push origin v0.1.0`.
5. Create GitHub Release from tag with checksum of source archive (GitHub-generated zip/tar.gz).
6. Trigger or confirm Zenodo-GitHub hook; review Zenodo metadata.
7. Copy DOI to `CITATION.cff` (v0.1.0: `10.5281/zenodo.20543779`).

8. Commit DOI update on `main` and document in [citation.md](citation.md) and README.

## Recommended Zenodo metadata

| Field | Suggested value |
|-------|-----------------|
| Upload type | Software |
| Title | Match `CITATION.cff` title |
| License | MIT |
| Keywords | AI governance, public sector, EU, on-premise LLM, benchmark |
| Related identifiers | GIQ paper DOI (when published) |

## What must not appear in the Zenodo archive

- Private notes and lab notebooks with identifiable cases
- Non-anonymized field transcripts or exports
- `.env`, API keys, or infrastructure secrets
- Manuscript drafts and reviewer correspondence

## Archival integrity

- Prefer Zenodo **versioned DOI** for each release; cite the specific version in papers.
- Store checksum, for example:

  ```bash
  sha256sum localgovbench-v0.1.0.zip
  ```

- Record checksum in GitHub release notes and/or institutional data catalogue entry.

## Post-release maintenance

- Update `preferred-citation` in `CITATION.cff` when the companion GIQ paper is published.
- Add paper DOI as `related_identifiers` in Zenodo and cross-link from README.
- For new empirical data releases, publish a separate Zenodo dataset with its own DOI if required by policy.
