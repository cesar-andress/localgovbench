# Supplementary materials — master index

**Product:** LocalGovBench (Disclosure Functions v1 / schema disclosure affordance)  
**Software version (active):** 0.2.0 — DOI [10.5281/zenodo.21500899](https://doi.org/10.5281/zenodo.21500899)  
**Specification / coding / pipeline version:** 1.0.0  
**Companion historical archive:** v0.1.0 — DOI [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)  
**Canonical software tree:** [https://github.com/cesar-andress/localgovbench](https://github.com/cesar-andress/localgovbench)  
**Package path in repository:** `docs/supplements/`

## Purpose of this package

This package is the **publication-facing supplementary material index** for the Disclosure Functions v1 paper path. It organises existing repository artefacts into journal-style supplements (**A–J**). It does **not** invent empirical coding results, IRR statistics, realization rates, affordance–realization gaps, rankings, readiness scores, or shortfall scores.

Full normative text lives in the frozen paths cited below; each supplement is a **thin, citable wrapper** (purpose, inputs, outputs, limitations, cross-references, and tables/figures only where already justified by frozen artefacts).

## How to use

1. Read this index for scope and non-claims.  
2. Open the relevant Supplement A–J for the methods subsection being checked.  
3. Follow **cross-references** to the authoritative file in the repository (or Zenodo deposit of the cited software version).  
4. Do not treat blank coding templates or pilot packets as study results.

## Supplement map

| ID | Title | Primary authoritative artefacts |
|----|-------|----------------------------------|
| [A](A_corpus.md) | Corpus | `affordance/locks/corpus_lock_v1.*`, pilot corpus path + SHA-256 |
| [B](B_observed_schema_inventory.md) | Observed schema inventory | `affordance/outputs/schema_inventory_v1.*`, normalization rules |
| [C](C_disclosure_functions_v1.md) | Disclosure Functions v1 | `affordance/config/disclosure_functions_v1.yaml` (+ related config) |
| [D](D_coding_framework.md) | Coding framework | `affordance/coding/config/*`, templates, protocols, pilot launch |
| [E](E_validation_rules.md) | Validation rules | coding validators, label enums, experiment validators |
| [F](F_experimental_pipeline.md) | Experimental pipeline | `affordance/experiments/`, `EXPERIMENT_PIPELINE.md` |
| [G](G_reproducibility.md) | Reproducibility | build scripts, tests, locks, checksums |
| [H](H_repository_structure.md) | Repository structure | root README architecture; active vs legacy surfaces |
| [I](I_software_citation.md) | Software citation | `CITATION.cff`, `.zenodo.json`, dual-DOI rule |
| [J](J_version_history.md) | Version history | `CHANGELOG.md`, tags `v0.1.0` / `v0.2.0`, layer versions |

## Global non-claims (apply to all supplements)

This supplementary package does **not** provide:

- completed human coding judgments or adjudicated matrices as study findings;  
- inter-rater reliability coefficients;  
- record-level realization rates or affordance–realization gap estimates;  
- governance readiness / maturity / shortfall / compliance scores;  
- jurisdiction rankings or composite indices.

Where Phase 3 emits **templates** or **placeholders** for later realization analysis, those are infrastructure only (see Supplement F).

## Recommended reading order (methods reviewers)

A → B → C → D → E → F → G, then I/J for citation and provenance, H for navigation.

## Path prefix convention

Unless noted otherwise, paths are relative to the **software repository root**:

`localgovbench_measurement_validation/affordance/` → abbreviated below as `affordance/`.

## Status note on archive tip vs development tip

Tag **`v0.2.0`** (DOI `10.5281/zenodo.21500899`) archives the Disclosure Functions specification and coding-layer freeze. Later commits on `main` may add experiment-pipeline and pilot-launch operational files. When citing workflows, name the **Git commit or software version** actually used (see Supplements F, G, J).

## Figures and tables

| Supplement | Tables | Figures |
|------------|--------|---------|
| A | Corpus counts by source (from corpus lock) | None (no new graphics) |
| B | Inventory field counts by source; inventory columns | None |
| C | Eleven disclosure functions | None (catalogue is tabular/YAML) |
| D | Coding artefact index; unit counts 55 / 33 | None |
| E | Enumerations summary | None |
| F | Pipeline I/O summary | Optional textual flowchart only |
| G | Command checklist | None |
| H | Directory roles | None |
| I | Citation blocks | None |
| J | Version timeline | None |

## Maintenance

Regenerate scientific artefacts only via documented builders (`scripts/build_affordance_specification.py`, `scripts/build_affordance_coding_layer.py`, pilot launch generator). Update this index when authoritative paths move; do not fork normative definitions into these wrappers.
