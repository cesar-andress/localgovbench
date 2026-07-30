# Final release consistency audit

**Date:** 2026-07-30  
**Role:** Release Manager / Research Software Engineer / Final Publication Auditor  
**Canonical release:** LocalGovBench **v1.0.0**  
**Canonical DOI:** https://doi.org/10.5281/zenodo.21701861  
**GitHub release:** https://github.com/cesar-andress/localgovbench/releases/tag/v1.0.0  

**Scope:** Publication, citation, reproducibility, and release metadata only. No scientific results, tables, figures, mappings, or freeze numbers were modified.

---

## 1. Files modified

### Manuscript (`paper/`)

| File | Change |
|------|--------|
| `sections/12_data_availability.tex` | Canonical DOI; historical priors labeled |
| `sections/13_declarations.tex` | Code/supplementary → v1.0.0 DOI |
| `sections/04_method.tex` | Archive paragraph → published DOI (removed PLACEHOLDER) |
| `sections/01_introduction.tex` | Software cite → `localgovbenchzenodo2026v100` |
| `sections/appendix_artifact.tex` | Cite → v1.0.0 |
| `tables/table_all_criteria.tex` | Cite → v1.0.0 |
| `submission/cover_letter_information_polity.md` | Adds canonical DOI |
| `docs/data_availability_statement.md` | Rewritten for v1.0.0 |
| `docs/software_availability_statement.md` | Rewritten for v1.0.0 |
| `README.md` | Canonical software pointer |
| `FINAL_SUBMISSION_CHECKLIST.md` | PASS on DOI / PLACEHOLDER |
| `references/citation_keys.md` | Canonical key `localgovbenchzenodo2026v100` |

### Shared bibliography

| File | Change |
|------|--------|
| `~/papers/bibliography.bib` | Added `@software{localgovbenchzenodo2026v100}` (DOI 21701861); marked v0.1/v0.2 entries historical |

### Software repository (`localgovbench/`)

| File | Change |
|------|--------|
| `CITATION.cff` | Top-level `doi: 10.5281/zenodo.21701861`; identifiers updated |
| `.zenodo.json` | Description + related_identifiers include canonical DOI |
| `README.md` | Canonical badge/DOI/citation block; historical labeled |
| `CHANGELOG.md` | v1.0.0 entry records published DOI; footer link |
| `docs/releases/NEXT_RELEASE.md` | Canonical baseline DOI |
| `docs/releases/README.md` | Canonical layer status |
| `docs/author_identity.md` | Canonical citation |
| `paper_data_policy/README.md` | Canonical DOI |
| `paper_data_policy/04_methods.md` | Archive note → published DOI |
| `scripts/validate_repository.py` | Requires 21701861 |
| `tests/test_active_documentation_claims.py` | Expects canonical DOI |

### This report

| File | Change |
|------|--------|
| `outputs/reports/final_release_consistency_audit.md` | Created |

---

## 2. Obsolete references removed / superseded

| Obsolete | Action |
|----------|--------|
| `10.5281/zenodo.PLACEHOLDER` | **Removed** from active manuscript build chain, method archive, declarations, paper_data_policy |
| Framing of v0.2.0 as “canonical / active software citation” | **Superseded** by v1.0.0 DOI 21701861 |
| “DOI to be minted upon deposit” future tense | **Replaced** with published archive language |
| README “until DOI appears on Zenodo” | **Removed** |

Historical DOIs `21500899` / `20543779` retained **only** where explicitly labeled historical/provenance (CHANGELOG prior versions, README historical notice, Data availability provenance sentence, CITATION identifiers).

---

## 3. DOI references updated

| Context | Now points to |
|---------|----------------|
| Manuscript Data availability | `10.5281/zenodo.21701861` |
| Manuscript Code availability | `10.5281/zenodo.21701861` |
| Manuscript Method archive | `10.5281/zenodo.21701861` |
| Manuscript software cites | `\citep{localgovbenchzenodo2026v100}` |
| `CITATION.cff` top-level `doi` | `10.5281/zenodo.21701861` |
| README badge / cite block | `10.5281/zenodo.21701861` |
| CHANGELOG `[1.0.0]` link | `https://doi.org/10.5281/zenodo.21701861` |

Verified live: Zenodo API record `21701861` resolves; version `1.0.0`; title matches software metadata.

---

## 4. Version references updated

| Surface | Version |
|---------|---------|
| Software metadata | **1.0.0** |
| GitHub release tag | **v1.0.0** |
| Manuscript reproducibility statements | **v1.0.0** |
| Instrument catalogue name in methods | **LocalGovBench v0.1** (scientific freeze label; not a Zenodo version claim) |

---

## 5. Remaining inconsistencies

1. **Zenodo creators vs repository authors.** Published Zenodo API metadata currently lists **only César Andrés**. Repository `CITATION.cff` / `.zenodo.json` list **César Andrés** and **David Martín-Moncunill**. Manual Zenodo metadata edit recommended so the public deposit matches the manuscript author block. *Not invented; flagged only.*
2. **Annotated Git tag vs post-DOI documentation commits.** The published Zenodo deposit is bound to the GitHub/Zenodo integration snapshot at deposit time. Follow-up commits on `main` that insert the minted DOI into `CITATION.cff`/`README` are documentation synchronization and are **not** retagged here, to avoid creating an unintended new Zenodo version. Cite the **DOI** as authoritative archive; GitHub `main` holds the synced citation files.
3. **Legacy / audit trail files** under `paper/legacy/`, `paper/outputs/reports/citation_related_work_audit/`, `docs/*` with `LEGACY — v0.1.0` banners, and historical release notes (`github_release_v0.2.0.md`, etc.) still mention prior DOIs **as historical context** (intentional).
4. **Scientific instrument label** “LocalGovBench v0.1” remains in Methods/Results as the frozen evidence-requirement catalogue identifier (empirical freeze), distinct from software release **v1.0.0**.

---

## 6. Confirmation

| Check | Status |
|-------|--------|
| Active manuscript PLACEHOLDER tokens | **None** |
| Manuscript PDF contains `21701861` | **Yes** |
| Manuscript PDF PLACEHOLDER | **No** |
| LaTeX build (pdflatex×3 + bibtex) | **Exit 0**; no undefined citations |
| `CITATION.cff` / README / CHANGELOG / `.zenodo.json` | **Canonical DOI present** |
| `validate_repository.py` | **PASS** |
| `pytest -m "not integration"` | **245 passed, 2 deselected** |
| Manuscript ↔ GitHub ↔ Zenodo DOI alignment for **canonical citation** | **YES** — all active surfaces cite **v1.0.0 / 10.5281/zenodo.21701861** |

**Verdict:** The manuscript, GitHub documentation tip, and Zenodo **DOI** are synchronized on the canonical public release:

**LocalGovBench v1.0.0**  
**DOI: https://doi.org/10.5281/zenodo.21701861**
