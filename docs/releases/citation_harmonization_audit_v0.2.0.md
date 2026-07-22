# Citation harmonization audit — LocalGovBench v0.2.0

**Date:** 2026-07-23  
**Canonical active DOI:** `10.5281/zenodo.21500899`  
**Historical v0.1.0 DOI:** `10.5281/zenodo.20543779`

## Classification legend

- **ACTIVE** — must cite v0.2.0 / `21500899`
- **HISTORICAL** — keep `20543779` (explicit v0.1.0 / GRB / legacy / provenance)
- **AMBIGUOUS** — flagged for review (not auto-replaced)

## Software repository (selected)

| Location | Class | Action |
|----------|-------|--------|
| `CITATION.cff` primary `doi` / version | ACTIVE | Set `doi` + `date-released` to v0.2.0 |
| `README.md` citation / badges | ACTIVE | Cite `21500899`; keep historical notice |
| `CHANGELOG.md` `[0.2.0]` | ACTIVE | Mark released + DOI |
| `docs/author_identity.md` | ACTIVE | Add active DOI |
| `docs/releases/*` drafts saying “DOI not yet” | ACTIVE | Update to published DOI |
| `docs/citation.md`, `docs/zenodo_release.md`, `docs/release_v0_1_checklist.md`, `docs/reproducibility.md`, LEGACY docs | HISTORICAL | Retain `20543779` |
| `paper_data_policy/04_methods.md` PLACEHOLDER | AMBIGUOUS | Study deposit ≠ software DOI; flag |
| `legacy/` | HISTORICAL | Do not modify |

## Manuscript repository (selected)

| Location | Class | Action |
|----------|-------|--------|
| `sections/12_data_availability.tex` | MIXED | Add active software cite; keep v0.1.0 historical for specification used |
| `README.md` instrument pointer | ACTIVE+HIST | Point active software to `21500899`; note v0.1 historical |
| `\citep{localgovbenchzenodo2026}` (tables/appendix/method uses) | HISTORICAL | Keep; ensure bib entry = v0.1.0 |
| `docs/data_availability_statement.md` | HISTORICAL | v0.1.0 synthetic deposit statement — retain |
| `legacy/submission_giq/*` | HISTORICAL | Do not modify |
| Method `PLACEHOLDER` replication deposit | AMBIGUOUS | Not the software DOI; leave placeholder, flag |
| `contribution_statement.tex` Zenodo 20543779 | HISTORICAL | GIQ instrument deposit — retain |
| Shared `~/papers/bibliography.bib` missing key | ACTIVE+HIST | Append v0.1.0 + v0.2.0 entries |
