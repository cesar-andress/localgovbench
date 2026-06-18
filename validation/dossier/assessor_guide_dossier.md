# Assessor guide — dossier-based LocalGovBench v0.1 validation

## Scope

This guide applies to **confidential programme dossier** assessments for the LocalGovBench **instrument-development and validation** study.

It does **not** authorise use of:

- public AI registers or transparency portals as primary evidence
- public-document observability metrics
- `open_pilot` materials as validation evidence

Vendor Stewardship in the Public Record is a **separate submitted paper**; public-record assets in the monorepo remain for that work's reproducibility only.

## Unit of assessment

One **bounded municipal LLM/AI programme** documented in a confidential dossier (`programme_manifest.yaml` + `documents/`).

## Evidence rules

1. **Quote before score** — every scored criterion requires a verbatim span from a dossier artefact.
2. **No inference from absence** — missing dossier material → `withheld_no_evidence`, not score 0.
3. **Evidence gates** — score ≥ 3 requires `evidence_gate_status: pass` with a named artefact in the span.
4. **Blind coding** — assessors do not see partner identity or the other assessor's scores until adjudication.

## Rubric

Use the frozen 0–4 maturity scale in `validation/content_validity/scoring_rubric.md`.

## Workflow

1. Read `programme_manifest.yaml` and confirm programme boundary.
2. Review dossier documents listed in the manifest.
3. Complete `evidence_log.yaml` entries per criterion.
4. Complete `assessor_{id}_scores.yaml` from the assessment template.
5. Flag discrepancies for adjudication per `adjudication_schema.yaml`.

## Training vignettes

Assessor training may use composite vignettes under `data/vignettes/`. Vignettes are **training only** and must **never** be presented as field validation evidence.

## Synthetic fixtures

Synthetic IRR, synthetic municipality profiles, and demo outputs under `examples/` or `outputs/` are **not** field validation. Do not cite them in `exports/validation/`.

## Outputs

Publishable aggregates go to `exports/validation/` only after `python scripts/validate_redevelopment_scope.py` passes.
