# Affordance specification layer (Disclosure Functions v1)

## Purpose

This directory is the **canonical specification layer** for measuring
**schema disclosure affordance** and preparing the
**affordance–realization gap** analysis of official public AI inventories.

It replaces the conceptual role previously played by
`pilot_public_satisfiability/config/localgovbench_criteria_v0.yaml` for the
inventory paper. LocalGovBench is **not** the analytical framework of this
paper path.

This layer does **not** measure readiness, maturity, shortfall, compliance,
governance quality, or jurisdiction rankings.

## Canonical input

Frozen corpus:

`localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv`

Observed fields are derived **only** from `raw_fields_json`.
`SOURCE_SCHEMAS` is not evidence of field existence.

## Hand-authored artefacts (`config/`)

| File | Role |
|------|------|
| `disclosure_functions_v1.yaml` | Normative function catalogue (v1.0.0) |
| `field_normalization_rules_v1.yaml` | Explicit normalization rules |
| `field_function_candidates_v1.csv` | PRIMARY/SECONDARY/INDIRECT/REJECTED maps |
| `applicability_overrides_v1.yaml` | Applicability labels and predicates |
| `realization_rules_v1.yaml` | Realization principles (no rates) |
| `linkage_field_types_v1.csv` | Documentary linkage typing |

## Generated artefacts

| File | Role |
|------|------|
| `locks/corpus_lock_v1.json` | Corpus checksum and counts |
| `locks/corpus_lock_v1.md` | Human-readable lock |
| `outputs/schema_inventory_v1.csv` | Observed field inventory |
| `outputs/schema_inventory_v1.json` | Same inventory as JSON |

**Do not edit generated inventory or lock files by hand.** Regenerate them.

## Regeneration

From the `localgovbench` repository root:

```bash
python3.12 scripts/build_affordance_specification.py
```

Validate hand-authored specs only:

```bash
python3.12 scripts/build_affordance_specification.py --validate-only
```

## Tests

```bash
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests -q
```

## Versioning

- Specification artefacts use semantic versions starting at **1.0.0**.
- Core disclosure functions are locked in 1.0.x.
- Schema inventory and corpus lock reference the corpus SHA-256.
- Changing the corpus requires regenerating lock + inventory and reviewing
  candidate mappings.

## Schema support vs record realization

- **Schema support / affordance** asks whether a schema provides fields capable
  of hosting a disclosure function (coding layer; not implemented in this stage
  beyond candidate maps).
- **Record realization** asks how often those fields are populated in records
  (rules frozen here; rates not computed in this stage).

Population is never a composite score and must not be used to rank jurisdictions.

## Out of scope for this stage

- Human coding
- Realization rate tables
- Affordance–realization gap outputs
- Figures / paper tables
- Manuscript rewriting
- Legacy file moves
