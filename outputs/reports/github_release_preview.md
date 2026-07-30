# GitHub Release preview — LocalGovBench v1.0.0

**Date:** 2026-07-30  
**Status:** Tag exists; **Release object missing** (API `GET /releases/tags/v1.0.0` → 404).  
**Tag:** `v1.0.0` → commit `d2aa5af` (annotated tag object `b5de506`)  
**Constraint:** Do **not** create a new tag, change the version, or modify commits. Create a Release **from the existing tag only**.

---

## Verification summary

| Item | Result |
|------|--------|
| Git tag `v1.0.0` | Present |
| GitHub Release object | **Absent** |
| Release notes on GitHub | **Missing** (no Release) |
| Zenodo DOI | `10.5281/zenodo.21701861` (unchanged) |
| Soft version | `1.0.0` |

`gh release create` / `gh release view` currently fail with token scope `repository.release` (403). Publish via the GitHub web UI using the body below, or with a token that has the `contents: write` / release permission.

---

## 1. Suggested Release title

```
LocalGovBench v1.0.0 — Stable Reproducibility Release
```

---

## 2. Complete Release body

Copy everything between the markers into the GitHub “Describe this release” field.

```markdown
## LocalGovBench v1.0.0 — Stable Reproducibility Release

Public research software for measuring **documentary evidence availability** in official public AI / algorithm inventory schemas: how far native published fields align with a fixed evidence-requirement catalogue, under frozen mapping rules.

### Purpose

This repository archives the companion software, configuration, frozen pilot outputs, and reproducibility scripts for the LocalGovBench empirical package used in the manuscript:

*What Public AI Inventories Disclose: Documentary Evidence Availability in Digital-Government Transparency Infrastructures*

(target venue: *Information Polity*).

It is a measurement and reproducibility artefact. It does **not** provide governance readiness scores, maturity indices, jurisdiction rankings, or legal compliance conclusions.

### Software version

- **Version:** 1.0.0  
- **Git tag:** `v1.0.0` (this Release)  
- **Compatibility:** Python 3.12 (see `pyproject.toml`)

### Archival DOI and citation

**Canonical archive:** [https://doi.org/10.5281/zenodo.21701861](https://doi.org/10.5281/zenodo.21701861)

Please cite the Zenodo version DOI and this tag when reusing the software or frozen pilot package. See `CITATION.cff` in the repository root.

Authors: César Andrés (corresponding); David Martín-Moncunill.

### Reproducibility

- Frozen public-satisfiability pilot outputs under `localgovbench_measurement_validation/pilot_public_satisfiability/` (empirical freeze **2026-06-24**; LocalGovBench **v0.1** requirement catalogue; \(N = 7{,}434\) programme records as observational volume).  
- Authoritative numerics: `paper_data_policy/results_freeze.md`.  
- Aggregate corpus CSV is intentionally outside git by default; rebuild/verify with `scripts/build_pilot_corpus.py` and `scripts/verify_pilot_corpus.py` when needed.  
- Repository structure check: `python scripts/validate_repository.py`.

### Validation summary (as of tag tip)

- Offline software test suite: **246 passed** (`pytest -m "not integration"`; integration tests skipped without live services).  
- Repository validation: **passed**.  
- GitHub Actions CI on the tagged tip: **passed**.  
- Active manuscript bibliography checked against OpenAlex/Crossref (live verification; grey literature noted where OpenAlex has no work record).  
- Reproducibility package included in this archive (scripts, frozen outputs, supplements index, citation metadata).

Historical deposits (v0.2.0 / v0.1.0) remain available on Zenodo for provenance only and are not the canonical citation for this release.
```

---

## 3. Checklist before clicking “Publish release”

- [ ] You are on https://github.com/cesar-andress/localgovbench/releases/new  
- [ ] **Choose existing tag:** `v1.0.0` (do **not** “Create new tag”)  
- [ ] Target is the commit already pointed to by `v1.0.0` (`d2aa5af`) — do not retarget  
- [ ] Title set exactly to: `LocalGovBench v1.0.0 — Stable Reproducibility Release`  
- [ ] Body pasted from §2 (markdown)  
- [ ] **Set as the latest release** (optional but recommended)  
- [ ] **Do not** check “Create a discussion” unless desired  
- [ ] **Do not** attach substitute binaries that replace the Zenodo archive; source from the tag is enough  
- [ ] Confirm DOI in the body remains `10.5281/zenodo.21701861`  
- [ ] Confirm no version bump (still 1.0.0)  
- [ ] After publish: `GET https://api.github.com/repos/cesar-andress/localgovbench/releases/tags/v1.0.0` returns **200**  
- [ ] Optional: set repository **Description** / **Homepage** (homepage → Zenodo DOI) in Settings — separate from this Release  

### CLI alternative (when token allows releases)

```bash
cd /path/to/localgovbench
gh release create v1.0.0 \
  --title "LocalGovBench v1.0.0 — Stable Reproducibility Release" \
  --notes-file outputs/reports/github_release_body.md
```

(Do not pass `--target` with a new commit; do not use a new tag name.)

---

## Note on test count

The preparation brief mentioned “245 software tests passed.” The current offline suite on the tagged tip reports **246 passed, 2 deselected**. The Release body uses **246** to avoid under- or over-stating.

---

No scientific changes. No new tag. No version change. No commit modification.
