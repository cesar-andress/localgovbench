# LocalGovBench Scientific Validation Package

Research-grade materials to move LocalGovBench v0.1 from a **conceptual instrument** to an **empirically validated** benchmark.

> Bundled inter-rater files under `ratings/` are **synthetic** for pipeline testing. Replace with field data for publication.

## Components

| # | Component | Location |
|---|-----------|----------|
| 1 | Content validity study templates | `templates/content_validity_study.yaml` |
| 2 | Expert review questionnaires | `templates/expert_review_questionnaire.yaml` |
| 3 | Inter-rater package (codebook, rating sheets, adjudication) | `templates/inter_rater_*.yaml` |
| 4 | Synthetic benchmark cases | `cases/` |
| 5 | Reliability metrics (κ, α) | `localgovbench/validation/reliability.py` |
| 6 | Benchmark reports | `reports/` (generated) |

## Workflow

### Content validity

1. Recruit expert panel (see `docs/content_validity_guide.md`).
2. Complete `templates/content_validity_study.yaml` (one row per criterion).
3. Aggregate scores; revise instrument; version bump.

### Inter-rater reliability

1. Select cases from `cases/`.
2. Two independent raters complete copies of `inter_rater_rating_sheet.yaml` per case.
3. Run analysis:

```bash
python scripts/run_inter_rater_analysis.py
python scripts/generate_validation_report.py
```

### Full validation report

```bash
python scripts/generate_validation_report.py
# → validation/reports/validation_benchmark_report.md
```

## Instrument

- **ID:** `localgovbench-v0.1`
- **Criteria:** 25 (five dimensions — unchanged)
- **No automated scoring** from LLMs in validation workflow

See [docs/validation_protocol.md](docs/validation_protocol.md).
