# Inter-rater assessor guide — LocalGovBench v0.1

## Purpose

Independent coders score **25 criteria** (five dimensions) for municipal **sovereign LLM** governance readiness using documentary evidence.

## Before you start

1. Read `validation/content_validity/scoring_rubric.md` (frozen 0–4 scale).
2. Review the case file in `validation/benchmark_cases/` or field materials.
3. Use `validation/inter_rater/scoring_template.yaml` (one file per rater × case).

## Procedure

1. **Evidence log** — List artefact IDs before assigning scores ≥3.
2. **Blind coding** — Do not discuss scores until reconciliation.
3. **Score each criterion** — Integer 0–4 only.
4. **Adjudication** — Resolve |rater_a − rater_b| ≥ 2 using `validation/templates/adjudication_record.yaml`.
5. **Export** — Save completed YAML to `validation/ratings/`.

## Reliability analysis

```bash
python scripts/run_inter_rater_analysis.py
```

Reports Cohen's κ and Krippendorff's α (see `localgovbench/validation/reliability.py`).

## Ethics

- Synthetic training cases are in `validation/benchmark_cases/`.
- Field documents stay outside the public repository unless anonymised and approved.
