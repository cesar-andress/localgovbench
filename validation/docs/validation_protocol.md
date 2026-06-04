# Validation Protocol — LocalGovBench v0.1

## Objective

Establish **content validity** and **inter-rater reliability** for the LocalGovBench governance readiness instrument before field deployment and journal publication.

## Phases

| Phase | Method | Output |
|-------|--------|--------|
| 1 | Content validity study | Revised criteria, CV metrics |
| 2 | Expert review | Qualitative instrument feedback |
| 3 | Pilot IRR on synthetic/real cases | κ, α per case |
| 4 | Field cases (municipalities) | Benchmark dataset (separate Zenodo deposit) |

## Phase 1 — Content validity

- **Panel:** 6–8 experts across public administration, law/DPO, IT security.
- **Instrument:** `validation/templates/content_validity_study.yaml`
- **Metrics:** Item-level relevance/clarity; optional I-CVI / S-CVI / CV ratio.
- **Decision rule:** Criteria below threshold are revised or removed (document in changelog).

## Phase 2 — Expert review

- **Instrument:** `validation/templates/expert_review_questionnaire.yaml`
- **Focus:** Sovereign on-premise LLM fit, overlap between criteria, regulatory mapping clarity.

## Phase 3 — Inter-rater reliability

- **Cases:** `validation/cases/*.yaml`
- **Ratings:** two independent coders per case.
- **Metrics:**
  - **Cohen's Kappa (κ)** — pairwise agreement (two raters).
  - **Krippendorff's Alpha (α)** — ordinal agreement with disagreement distance.
- **Adjudication:** differences ≥2 points (`adjudication_record.yaml`).

## Reporting standards

Report per case and pooled:

- κ, α with 95% CI (bootstrap in field studies)
- Disagreement matrix (criterion × rater pair)
- Evidence gate compliance rate

## Ethics

- No identifiable municipal data in public repository.
- Ethics approval and lawful basis for field documents.

## Version control

Tag instrument version in all YAML (`instrument: localgovbench-v0.1`). Increment minor version when criteria change after validity study.
