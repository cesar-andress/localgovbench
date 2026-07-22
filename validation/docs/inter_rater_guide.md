> **Status: LEGACY — v0.1.0**  
> Retained for provenance of historical inter-rater guidance.  
> **Do not use this document as the current analytical specification.**  
> **Active framework:** [`../../localgovbench_measurement_validation/affordance/coding/`](../../localgovbench_measurement_validation/affordance/coding/).

# Inter-Rater Assessment Guide

## Design

- **Cases:** 3+ municipal LLM programmes (`validation/cases/`).
- **Raters:** 2 independent assessors per case (extend to 3 for α robustness).
- **Unit of coding:** One maturity score (0–4) per criterion (25 per case).

## Steps

1. Read case description and linked documents.
2. Apply codebook: `validation/templates/inter_rater_codebook.yaml`.
3. Complete `inter_rater_rating_sheet.yaml` with evidence log.
4. Run `python scripts/run_inter_rater_analysis.py`.
5. Adjudicate large gaps using `adjudication_record.yaml`.
6. Recompute reliability after adjudication (report both pre- and post-adjudication in papers).

## Reliability metrics

| Metric | Function | Interpretation |
|--------|----------|----------------|
| Cohen's κ | `cohens_kappa()` | Pairwise categorical agreement |
| Krippendorff's α | `krippendorff_alpha()` | Ordinal agreement, handles missing (extension) |

Landis & Koch labels for κ and α≥0.667 guidance are **heuristic** — report confidence intervals in empirical work.

## Synthetic pilot data

Files in `validation/ratings/` demonstrate the analysis pipeline. **Replace** with blinded field ratings before claiming validated IRR.
