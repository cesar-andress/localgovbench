# Supplement J — Version history

## Purpose

Record the **version planes** relevant to Disclosure Functions v1: software releases, specification/coding/pipeline layer versions, and major milestone commits — without presenting later empirical results as part of earlier tags.

Authoritative changelog: root `CHANGELOG.md`.

## Inputs

| Input | Path |
|-------|------|
| Changelog | `CHANGELOG.md` |
| Package metadata | `pyproject.toml` |
| Layer versions | `affordance/__init__.py`, coding/experiments path constants |
| Git tags | `v0.1.0`, `v0.2.0` |

## Outputs

### Table J1 — Version planes

| Plane | Version | Meaning |
|-------|---------|---------|
| Software release (active) | **0.2.0** | Disclosure Affordance Framework transition release; DOI `10.5281/zenodo.21500899` |
| Historical software | **0.1.0** | Governance Readiness Benchmark archive; DOI `10.5281/zenodo.20543779` |
| Disclosure Functions specification | **1.0.0** | Normative catalogue + Phase 1 configs |
| Coding layer | **1.0.0** | Codebook, labels, templates, protocols |
| Experiment pipeline | **1.0.0** | Phase 3 infrastructure version (when present in the cited tree) |

### Table J2 — Software timeline (high level)

| Version / event | Date (as documented) | Notes |
|-----------------|----------------------|-------|
| `v0.1.0` | Historical | GRB / readiness instrument archive |
| DF Phase 1 freeze | milestone `aa8ea3d` (changelog) | Corpus lock, inventory, function catalogue |
| DF Phase 2 freeze | milestone `ac2669c` (changelog) | Coding system, 55-unit template, 33-unit pilot manifest |
| `v0.2.0` software release | 2026-07-23 | Framework transition; canonical DOI `21500899` |
| Phase 3 pipeline + pilot launch ops | commits on `main` after `v0.2.0` tip | Cite commit if used; may require newer archive than tag `v0.2.0` |

### Conceptual incompatibility (from CHANGELOG)

v0.2.0 active measurement target = **schema disclosure affordance (Disclosure Functions v1)**.  
It is **not** governance readiness / GRB maturity scoring. Historical materials remain labelled rather than deleted.

## Figures

None.

## Limitations

1. Changelog entries may lag documentation of operational packages added after the 0.2.0 narrative was drafted.  
2. Runtime `__version__` inside `localgovbench/__init__.py` may not match `pyproject.toml` on all commits — prefer metadata files and Git tags for citation (Supplement I/G).  
3. This supplement does **not** invent release notes for unpublished journal revisions.

## Cross references

| Topic | See |
|-------|-----|
| Citation | [Supplement I](I_software_citation.md) |
| Reproducibility | [Supplement G](G_reproducibility.md) |
| Full changelog | `CHANGELOG.md` |
| Public positioning | `docs/releases/public_positioning_v0.2.0.md` |
| Master index | [README.md](README.md) |
