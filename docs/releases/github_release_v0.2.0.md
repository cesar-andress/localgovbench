# GitHub release notes draft — v0.2.0

**Status:** published tag `v0.2.0` — canonical DOI https://doi.org/10.5281/zenodo.21500899

## Summary

LocalGovBench **v0.2.0** is a **framework transition** release. The active research software path measures **schema disclosure affordance** for public AI and algorithm registers via **Disclosure Functions v1**, with a reproducible specification layer and human schema-coding system.

This is **not** a completed empirical-results release.

## Conceptual transition

v0.1.0 centred on a **Governance Readiness Benchmark** for sovereign LLM deployments (maturity/readiness scoring). That design remains archived for provenance ([DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)) and is **not** the active analytical framework.

See [`public_positioning_v0.2.0.md`](public_positioning_v0.2.0.md).

## New active framework

- Schema disclosure affordance  
- Disclosure Functions v1  
- Applicability-aware comparison  
- Structured human schema coding  
- Planned record-level realization and affordance–realization gap  
- No jurisdiction rankings, readiness/maturity scores, shortfall scores, compliance scores, or composite indices  

## Additions since v0.1.0

Major implementation milestones (not an exhaustive commit list):

- **`aa8ea3d`** — Implement Disclosure Functions v1 specification layer  
- **`ac2669c`** — Implement Disclosure Functions v1 schema coding layer  

Additional supporting work (Delphi package sync, manuscript scaffolds, documentation) may also appear in history since v0.1.0.

## Specification layer

- `disclosure_functions_v1.yaml`  
- Field normalization, candidates, applicability, realization rules, linkage types  
- Corpus lock over **7,434** records + observed-field schema inventory generators  

## Schema-coding layer

- Codebook, coder instructions, worked examples  
- Coding template (**55** units) + pilot manifest (**33** units)  
- Validation utilities, double-coding + adjudication protocols  
- IRR **plan** only (no calculated IRR)  

## Reproducibility

```bash
pip install -e ".[dev]"
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_coding_layer.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests -q
```

## Compatibility note

- v0.1.0 / GRB workflows remain in-tree as **legacy** (labelled documentation).  
- Do not mix GRB readiness scores with Disclosure Functions coding outputs.  
- Cite v0.1.0 DOI only when referring to the historical instrument.  
- **Conceptual incompatibility:** v0.2.0’s active measurement interpretation is not interchangeable with v0.1.0 readiness scoring.

## Deprecated and legacy components

Retained for provenance: `localgovbench/framework`, `localgovbench/grb`, most of `docs/`, `validation/`, `examples/`, `data/benchmark/` (all labelled **LEGACY — v0.1.0**).

## Known limitations

- Human coding not executed for publication  
- Realization / gap analysis not completed  

## Citation instructions

Cite **LocalGovBench v0.2.0: Disclosure Affordance Framework for Public AI and Algorithm Registers** at https://doi.org/10.5281/zenodo.21500899.  
Preserve historical DOI `10.5281/zenodo.20543779` for v0.1.0 only. See `CITATION.cff` and root `README.md`.

## Historical v0.1.0 DOI

https://doi.org/10.5281/zenodo.20543779 — **version DOI for v0.1.0 only**. Do not reuse as the v0.2.0 DOI.

## Zenodo

Published version DOI: https://doi.org/10.5281/zenodo.21500899 (`isNewVersionOf` 10.5281/zenodo.20543779).

## Full change summary since v0.1.0

See `CHANGELOG.md` section `[0.2.0]`.
