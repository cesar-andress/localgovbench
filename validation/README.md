# LocalGovBench Empirical Validation Package (v0.1)

**Instrument frozen** — empirical studies validate the existing 25-criterion instrument without modifying dimensions, scales, or definitions.

## Package map

| # | Component | Location |
|---|-----------|----------|
| 1 | **Content validity** | `content_validity/` |
| 2 | **Inter-rater reliability** | `inter_rater/`, `ratings/`, `localgovbench/validation/reliability.py` |
| 3 | **Synthetic benchmark cases** | `benchmark_cases/` |
| 4 | **Discriminant validity** | `scripts/run_discriminant_validity.py` |
| 5 | **Reports** | `reports/` |

## Quick commands

```bash
# Content validity (I-CVI, CVR)
python scripts/run_content_validity_analysis.py \
  --input validation/content_validity/indicator_relevance_survey_results.example.yaml

# Inter-rater reliability (κ, α)
python scripts/run_inter_rater_analysis.py

# Discriminant validity (synthetic cases)
python scripts/run_discriminant_validity.py

# Integrated validation report
python scripts/generate_validation_report.py
```

## Protocol

Authoritative document: **[docs/validation_protocol.md](../docs/validation_protocol.md)**

## Legacy paths

- `validation/cases/` + `validation/ratings/` — IRR training (3 cases, 2 raters)
- `validation/templates/` — earlier templates (superseded by `content_validity/` and `inter_rater/` where duplicated)

## Synthetic data warning

All bundled scores and expert examples are **synthetic** until field studies replace them.
