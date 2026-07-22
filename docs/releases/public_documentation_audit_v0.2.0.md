# Public documentation audit — v0.2.0 preparation

**Date:** 2026-07-23  
**Scope:** Active public surface vs historical v0.1.0 artefacts  
**Rule:** Do not delete historical material; label or update.

| File | Outdated text/concept | Surface | Action | Rationale |
|------|----------------------|---------|--------|-----------|
| `README.md` | Presents v0.1.0 GRB/readiness as primary project | Active | **update** | Primary visitor entrypoint |
| `CITATION.cff` | version 0.1.0; readiness/GRB abstract; DOI points only to v0.1.0 as current | Active | **update** | Cite forthcoming v0.2.0 positioning; keep v0.1.0 DOI as historical identifier |
| `pyproject.toml` | version 0.1.0; generic governance description | Active | **update** | Package metadata must match active framework |
| `CHANGELOG.md` | Ends at 0.1.0 | Active | **update** | Add 0.2.0 draft section |
| `docs/benchmark_specification.md` | Governance readiness / sovereign LLM | Historical | **archive-label** | Provenance of v0.1.0 instrument |
| `docs/demo_walkthrough.md` | GRB readiness workflow | Historical | **archive-label** | Legacy demo |
| `docs/framework.md` | v0.1 dimensions/criteria | Historical | **archive-label** | Superseded as active framework |
| `docs/methodology.md` | Readiness methodology | Historical | **archive-label** | |
| `docs/governance_dimensions.md` | Maturity dimensions | Historical | **archive-label** | |
| `docs/construct_traceability.md` | 25 criteria literature map | Historical | **archive-label** | |
| `docs/validation_protocol.md` | Validate readiness instrument | Historical | **archive-label** | |
| `docs/inter_rater_reliability_protocol.md` | GRB IRR | Historical | **archive-label** | |
| `docs/llm_benchmark_experiment.md` | Ollama GRB extraction | Historical | **archive-label** | |
| `docs/manuscript_positioning.md` | GIQ/readiness positioning | Historical | **archive-label** | |
| `docs/synthetic_municipality_corpus.md` | Municipal dossier corpus | Historical | **archive-label** | |
| `docs/artifact_description.md` | v0.1.0 artifact description | Historical | **archive-label** | Keep for Zenodo provenance |
| `docs/zenodo_release.md` | v0.1.0 Zenodo steps | Historical | **archive-label** / supplement with v0.2.0 drafts | New drafts under `docs/releases/` |
| `docs/release_v0_1_checklist.md` | v0.1.0 checklist | Historical | **retain-history** + label | Do not rewrite |
| `docs/ai_act_mapping.md` / `gdpr_mapping.md` | Mapped to v0.1 criteria | Historical | **archive-label** | Indicative only; not active DF path |
| `docs/citation.md` | Cite v0.1.0 only | Historical | **archive-label** + point to root README | Update root README citation |
| `docs/reproducibility.md` | v0.1/GRB commands as primary | Historical | **archive-label** | Active commands in affordance README |
| `docs/redevelopment_scope.md` | Redevelopment of instrument | Historical | **archive-label** | |
| `docs/author_identity.md` | Still valid identity | Active | **retain** / minor note | Canonical author metadata |
| `data/benchmark/README.md` | GRB Ollama tasks | Historical | **archive-label** | |
| `validation/README.md` | Validate 25-criterion instrument | Historical | **archive-label** | |
| `validation/docs/*` | v0.1 validation guides | Historical | **archive-label** | |
| `examples/README.md` | GRB examples | Historical | **archive-label** | |
| `localgovbench_measurement_validation/affordance/README.md` | Current | Active | **retain** | Active SoT |
| `localgovbench/` package (framework/grb) | Code for v0.1/GRB | Included legacy software | **retain** + README clarifies legacy | Do not delete code |
| `.zenodo.json` / `codemeta.json` | Absent | — | **create drafts in docs/releases** | Not inventing live Zenodo DOI |
| Badges in README | version 0.1.0 / Zenodo v0.1.0 as only badge | Active | **update** | Show provisional 0.2.0; keep historical DOI note |

## Positioning statement (frozen for v0.2.0 docs)

LocalGovBench is a reproducible research repository for studying **disclosure affordances** and **record-level realization** in public AI and algorithm registers, using **Disclosure Functions v1**. The historical v0.1.0 Governance Readiness Benchmark remains archived (DOI 10.5281/zenodo.20543779) for provenance and is not the active analytical framework. Specification and schema-coding layers are implemented; full realization rates, IRR results, gap analysis figures, and the companion manuscript are **not** claimed complete in this release preparation.
