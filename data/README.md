# Data directory

> **Note.** Bundled `benchmark/` materials are **LEGACY — v0.1.0**.  
> They are **not Disclosure Functions v1 empirical results** and not current readiness/ranking findings.  
> Active DF path: [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md).

This folder holds datasets and instruments for LocalGovBench. **Tracked trees include synthetic/benchmark/traceability assets; `raw/` and `processed/` remain placeholders for future empirical collections.**

## Structure

| Path | Purpose | Status |
|------|---------|--------|
| `raw/` | Primary empirical collections | Empty — reserved for future releases |
| `processed/` | Cleaned, analysis-ready tables | Empty — reserved for future releases |
| `templates/` | Survey/checklist export templates | Placeholders as needed |

## Synthetic data policy

Unless a file header or release note explicitly states otherwise:

- All bundled examples are **synthetic**
- Do not treat demonstration files as empirical benchmark results
- Do not commit identifiable personal or organizational records

## Adding empirical data (future)

1. Document provenance, consent, and anonymization in a `DATASET.md` per release.
2. Use Zenodo for large archives; reference DOIs in `CITATION.cff`.
3. Keep `metadata.synthetic: false` only for vetted real datasets with full documentation.
