# Public documentation audit — v0.2.0 preparation

**Date:** 2026-07-23  
**Scope:** Active public surface vs historical v0.1.0 artefacts  
**Rule:** Do not delete historical material; label, update, or demote from active navigation.

Allowed actions: `update` | `label_legacy` | `label_deprecated` | `retain_historical` | `remove_from_active_navigation` | `no_change`

| File | Outdated claim or terminology | Active / historical | Action | Rationale | Replacement / active reference |
|------|------------------------------|---------------------|--------|-----------|--------------------------------|
| `README.md` | Prior primary framing as GRB / readiness | Active | `update` | Visitor entrypoint must state DF v1 | This README (Disclosure Functions) |
| `CITATION.cff` | Formerly 0.1.0 readiness abstract / current DOI misuse risk | Active | `update` | Cite provisional 0.2.0 positioning; keep v0.1.0 DOI as historical only | Root README citation section |
| `pyproject.toml` | Formerly 0.1.0 / governance-generic description | Active | `update` | Package metadata must match active framework | Affordance README |
| `CHANGELOG.md` | Needed 0.2.0 transition section | Active | `update` | Keep a Changelog; do not rewrite 0.1.0 | — |
| `CONTRIBUTING.md` | Scope listed framework scoring / dimensions as primary | Active | `update` | Align contribution scope with DF v1 | Root README |
| `docs/author_identity.md` | Identity still valid; citation pointer was v0.1-centric | Active | `update` | Point active citation to root README; keep historical DOI note | Root README / CITATION.cff |
| `docs/benchmark_specification.md` | Governance readiness / sovereign LLM | Historical | `label_legacy` | Provenance of v0.1.0 instrument | `localgovbench_measurement_validation/affordance/README.md` |
| `docs/demo_walkthrough.md` | GRB readiness workflow | Historical | `label_legacy` | Legacy demo | Affordance README + root README |
| `docs/framework.md` | v0.1 dimensions/criteria | Historical | `label_legacy` | Superseded as active framework | Affordance DF v1 catalogue |
| `docs/methodology.md` | Readiness methodology | Historical | `label_legacy` | Not active measurement path | Affordance README |
| `docs/governance_dimensions.md` | Maturity dimensions | Historical | `label_legacy` | Not DF v1 | Affordance README |
| `docs/construct_traceability.md` | 25 criteria literature map | Historical | `label_legacy` | Historical construct map | Affordance coding codebook |
| `docs/validation_protocol.md` | Validate readiness instrument | Historical | `label_legacy` | Historical validation | Affordance coding validation docs |
| `docs/inter_rater_reliability_protocol.md` | GRB IRR | Historical | `label_legacy` | Historical IRR protocol | Affordance coding IRR plan |
| `docs/llm_benchmark_experiment.md` | Ollama GRB extraction | Historical | `label_legacy` | Historical LLM experiment | Affordance README |
| `docs/manuscript_positioning.md` | GIQ/readiness positioning | Historical | `label_legacy` | Superseded positioning | `public_positioning_v0.2.0.md` |
| `docs/synthetic_municipality_corpus.md` | Municipal dossier corpus | Historical | `label_legacy` | Historical synthetic dossiers | Pilot corpus lock (affordance) |
| `docs/artifact_description.md` | v0.1.0 artifact description | Historical | `label_legacy` | Keep for Zenodo provenance | `docs/releases/*` |
| `docs/zenodo_release.md` | v0.1.0 Zenodo steps | Historical | `label_legacy` | Supplemented by v0.2.0 drafts | `zenodo_metadata_v0.2.0.md` |
| `docs/release_v0_1_checklist.md` | v0.1.0 checklist | Historical | `retain_historical` | Do not rewrite frozen checklist | `release_readiness_v0.2.0.md` |
| `docs/ai_act_mapping.md` | Mapped to v0.1 criteria | Historical | `label_legacy` | Indicative only | Affordance DF catalogue (not legal mapping) |
| `docs/gdpr_mapping.md` | Mapped to v0.1 criteria | Historical | `label_legacy` | Indicative only | Affordance DF catalogue |
| `docs/citation.md` | Cite v0.1.0 as current | Historical | `label_legacy` | Historical citation instructions | Root README + CITATION.cff |
| `docs/reproducibility.md` | v0.1/GRB commands as primary | Historical | `label_legacy` | Active commands live under affordance | Affordance README |
| `docs/redevelopment_scope.md` | Redevelopment as readiness instrument | Historical | `label_legacy` | Outdated redevelopment framing | `public_positioning_v0.2.0.md` |
| `data/benchmark/README.md` | GRB Ollama tasks | Historical | `label_legacy` | Historical benchmark tasks | Affordance coding templates |
| `validation/README.md` | Validate 25-criterion / GRB | Historical | `label_legacy` | Historical validation package | Affordance coding protocols |
| `validation/docs/*` | v0.1 validation guides | Historical | `label_legacy` | Historical coder guides | Affordance coding docs |
| `examples/README.md` | GRB examples | Historical | `label_legacy` | Synthetic GRB examples | Affordance coding examples |
| `localgovbench_measurement_validation/affordance/README.md` | Current DF v1 SoT | Active | `no_change` | Already active | — |
| `localgovbench/` (`framework/`, `grb/`, …) | Readiness/GRB software | Legacy software | `retain_historical` | Do not delete; demote in navigation | Affordance package path |
| `.zenodo.json` / `codemeta.json` | Absent at repo root | — | `no_change` | Drafts live under `docs/releases/` until publish | `zenodo_v0.2.0.draft.json` |
| Badges in README | Risk of presenting v0.1.0 DOI as sole current version | Active | `update` | Provisional 0.2.0 badge + historical DOI labelled | — |
| `notebooks/` | Directory absent | — | `no_change` | Nothing to label | — |
| `paper_data_policy/` | Manuscript scaffold / methods (not public software SoT) | Development / manuscript | `remove_from_active_navigation` | Not the software entrypoint; exclude from Zenodo software narrative unless user confirms | Affordance README |
| GitHub About / topics (remote UI) | May still say readiness | External | `update` | User must update GitHub UI description after review | `public_positioning_v0.2.0.md` short description |

## Search terms covered

Governance Readiness Benchmark; GRB; governance readiness; governance maturity; sovereign LLM deployments; shortfall; maturity levels; readiness scores; jurisdiction rankings; compliance scores; composite index; municipal readiness; LocalGovBench criteria.
