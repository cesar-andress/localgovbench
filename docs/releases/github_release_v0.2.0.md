# GitHub release notes draft — v0.2.0

**Status:** draft — **do not create the GitHub Release or tag yet**

## Summary

LocalGovBench **v0.2.0** is a **framework transition** release. The active research software path measures **schema disclosure affordance** for public AI and algorithm registers via **Disclosure Functions v1**, with a reproducible specification layer and human schema-coding system.

This is **not** a completed empirical-results release.

## Major conceptual change

v0.1.0 centred on a **Governance Readiness Benchmark** for sovereign LLM deployments (maturity/readiness scoring). That design remains archived for provenance ([DOI 10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)) and is **not** the active analytical framework.

## New active framework

- Schema disclosure affordance  
- Disclosure Functions v1  
- Applicability-aware comparison  
- Structured human schema coding  
- Planned record-level realization and affordance–realization gap  
- No jurisdiction rankings, readiness/maturity scores, shortfall scores, compliance scores, or composite indices  

## Implemented specification artefacts

- `disclosure_functions_v1.yaml`  
- field normalization, candidates, applicability, realization rules, linkage types  
- corpus lock + observed-field schema inventory generators  

## Implemented coding artefacts

- codebook, coder instructions, worked examples  
- coding template (55 units) + pilot manifest  
- validation utilities, double-coding + adjudication protocols  
- IRR **plan** only (no calculated IRR)  

## Compatibility / migration

- v0.1.0 / GRB workflows remain in-tree as **legacy** (labelled documentation).  
- Do not mix GRB readiness scores with Disclosure Functions coding outputs.  
- Cite v0.1.0 DOI only when referring to the historical instrument.

## Legacy status of v0.1.0 components

Retained for provenance: `localgovbench/framework`, `localgovbench/grb`, most of `docs/`, `validation/`, `examples/`, `data/benchmark/`.

## Known limitations

- Human coding not executed for publication  
- Realization / gap analysis not completed  
- No v0.2.0 Zenodo DOI yet  

## Reproducibility commands

```bash
pip install -e ".[dev]"
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_coding_layer.py
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests -q
```

## Citation notice

Until a Zenodo version DOI for v0.2.0 is minted, cite the Git tag/commit. Preserve historical DOI `10.5281/zenodo.20543779` for v0.1.0 only. See `CITATION.cff` and root `README.md`.

## Zenodo note

Publish a **new version** linked as `isNewVersionOf` 10.5281/zenodo.20543779. See `docs/releases/zenodo_metadata_v0.2.0.md`.

## Full change summary since v0.1.0

See `CHANGELOG.md` section `[0.2.0]`.
