> **Status: LEGACY — v0.1.0**  
> This document describes the historical Governance Readiness Benchmark / v0.1 instrument design.  
> It is retained for provenance and is **not** the active analytical framework.  
> **Active framework:** Disclosure Functions v1 — see [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and the root [`README.md`](../README.md).


# Synthetic municipality corpus — generation assumptions

## Purpose

The corpus under `data/synthetic/municipality_corpus/` provides **fictional municipal governance documents** for:

- GRB / v0.1 workflow demos (`run_assessment_workflow.py`)
- Ollama evidence-extraction experiments
- Pilot coding exercises without real organizational data

It is **not** empirical validation data and must not be presented as real municipalities.

## Generation

```bash
python scripts/generate_municipality_corpus.py
# optional: --count 50 --seed 42 --output-dir data/synthetic/municipality_corpus
```

| Parameter | Default | Notes |
|-----------|---------|-------|
| `--count` | 50 | Max 50 unique fictional names |
| `--seed` | 42 | Reproducible tier and field assignment |
| Output | `data/synthetic/municipality_corpus/` | Regenerating overwrites documents |

## Layout

```
data/synthetic/municipality_corpus/
  metadata.json
  municipalities/
    mun_001_<slug>/
      governance_policy.md
      ai_strategy.md
      oversight_procedure.md
      risk_register.md
      procurement_note.md
      architecture_note.md
```

## Assumptions

### Fictional identities

- Municipality **display names** are invented (e.g. “Municipality of Nordvale”).
- **No** mapping to real cities, regions, or officials.
- Each record has a stable `municipality_id` (`mun_NNN_slug`).

### Maturity tiers

Each municipality is assigned one generator tier (`low`, `emerging`, `managed`) that controls **wording strength** in templates, not empirically measured readiness:

| Tier | Policy status (template) | Oversight cadence (template) |
|------|--------------------------|----------------------------|
| `low` | Draft / pending adoption | Ad hoc |
| `emerging` | Approved with conditions | Monthly 5% sampling |
| `managed` | Approved, annual review | Weekly 10% + quarterly audit |

Tiers are **uniformly random** per municipality (independent of population band).

### Population and region

- `population_band` is a fictional bracket (15k–450k).
- `region` is one of five invented regional labels.
- These fields support narrative variety only; they are not census data.

### Document set (six per municipality)

| Document | Role |
|----------|------|
| `governance_policy.md` | Accountability, GDPR themes, human oversight |
| `ai_strategy.md` | Sovereign LLM vision, use case, roadmap |
| `oversight_procedure.md` | Review tiers, escalation, sampling |
| `risk_register.md` | Five synthetic risks with 1–16 scores |
| `procurement_note.md` | Fictional vendor, exit/portability clauses |
| `architecture_note.md` | On-prem deployment, logging, CAB |

All files include a **SYNTHETIC** banner and municipality ID in the header.

### Primary use case

One use case per municipality is drawn from a fixed list (e.g. policy drafting, enquiry triage). Secondary pilots are mentioned in the AI strategy template only.

### What is not generated

- Real personal data, case numbers, or contract values
- Scores tied to GRB indicators (coding is a separate step)
- Translations; documents are English for v0.1.0
- PDF or scanned images (Markdown only)

## Metadata file

`metadata.json` records:

- `corpus_version`, `synthetic: true`, `seed`, `generated_on`
- `maturity_tier_distribution`
- Per-municipality record: IDs, tier, region, population band, document list

## Ethics and reuse

- Safe for public repositories and classroom use
- Do not infer municipal performance from tier labels
- For field studies, replace with ethics-approved real corpora and set `metadata.synthetic: false` in a new dataset manifest

## Related paths

| Path | Description |
|------|-------------|
| `data/synthetic/workflow_demo/` | Single five-document demo set |
| `localgovbench/synthetic/municipality_corpus.py` | Generator implementation |
| `tests/test_municipality_corpus.py` | Structure and reproducibility tests |
