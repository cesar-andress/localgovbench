# Supplement I — Software citation

## Purpose

Provide **authoritative citation guidance** for the LocalGovBench software artefact used in the Disclosure Functions v1 paper path, including the dual-DOI rule (active vs historical).

## Inputs

| Input | Path |
|-------|------|
| Citation File Format | `CITATION.cff` |
| Zenodo metadata (root) | `.zenodo.json` |
| Public positioning | `docs/releases/public_positioning_v0.2.0.md` |
| Author identity | `docs/author_identity.md` |

## Outputs

### Preferred software citation (active)

**Release title (prose):** LocalGovBench v0.2.0: Disclosure Affordance Framework for Public AI and Algorithm Registers  

**Zenodo record title:** LocalGovBench: Disclosure Affordances in Public AI and Algorithm Registers  

**Version:** 0.2.0  
**DOI:** https://doi.org/10.5281/zenodo.21500899  
**License:** MIT  

### BibTeX (active)

```bibtex
@software{localgovbench_v020,
  author  = {Andrés, César},
  title   = {{LocalGovBench}: Disclosure Affordances in Public AI and Algorithm Registers},
  year    = {2026},
  version = {0.2.0},
  doi     = {10.5281/zenodo.21500899},
  url     = {https://doi.org/10.5281/zenodo.21500899},
  note    = {Disclosure Affordance Framework; Disclosure Functions v1}
}
```

### Historical archive only (not the active analytical framework)

**DOI:** https://doi.org/10.5281/zenodo.20543779  
**Tag:** `v0.1.0` (Governance Readiness Benchmark provenance)

Do **not** cite v0.1.0 as the active measurement framework for Disclosure Functions analyses.

### Table I1 — Identifier roles

| Identifier | Role |
|------------|------|
| `10.5281/zenodo.21500899` | Canonical active software version DOI (v0.2.0) |
| `10.5281/zenodo.20543779` | Historical v0.1.0 only |
| `https://github.com/cesar-andress/localgovbench` | Source repository |
| ORCID `0009-0001-8968-3404` | Author identifier (`CITATION.cff`) |

Companion **peer-reviewed paper DOI** is not set in `CITATION.cff` (explicitly left unset to avoid invention). Concept DOI, if distinct, requires confirmation from the Zenodo record UI.

## Figures

None.

## Limitations

1. Title variants (“Affordances” vs “Affordance Framework”) are intentional (record title vs release prose); use Table I1 + BibTeX above for bibliographies.  
2. Legacy files under `docs/citation.md` / `docs/zenodo_release.md` are **v0.1-oriented**; do not override `CITATION.cff`.  
3. Cite the **Git commit** when using features (e.g. Phase 3 pipeline, pilot launch) that post-date the frozen Zenodo tip you downloaded.

## Cross references

| Topic | See |
|-------|-----|
| Version timeline | [Supplement J](J_version_history.md) |
| Reproducibility | [Supplement G](G_reproducibility.md) |
| `CITATION.cff` | repository root |
| Root README citation section | `README.md` |
