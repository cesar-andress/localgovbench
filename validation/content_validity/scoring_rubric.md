# LocalGovBench v0.1 — Assessor scoring rubric (frozen instrument)

> **Instrument frozen:** dimensions, criteria, and 0–4 scale are fixed for v0.1 empirical validation.

## Maturity scale (per criterion)

| Score | Label | Assessor guidance |
|-------|-------|-------------------|
| 0 | Absent | No observable practice or documentation |
| 1 | Ad hoc | Informal practice; fragmented or oral evidence only |
| 2 | Partially defined | Documented practice; uneven application |
| 3 | Managed | Named owner; periodic review; coherent artefacts |
| 4 | Optimized | Evidence-informed improvement cycle |

## Evidence gates

| Score | Evidence requirement |
|-------|---------------------|
| 0–2 | Assessor notes; artefacts optional |
| 3 | ≥1 primary artefact cited |
| 4 | ≥2 artefacts; one reviewed within 12 months |

## Prohibited

- Do **not** infer legal compliance from maturity scores.
- Do **not** use model performance metrics (accuracy, F1) as criterion scores.
- Do **not** let an LLM assign final scores without human verification.

## Aggregation (computed by tooling)

- Dimension score = mean of five criteria in dimension
- Readiness index = (mean of five dimension scores ÷ 4) × 100

See `localgovbench/framework/scoring.py` and `docs/benchmark_specification.md`.
