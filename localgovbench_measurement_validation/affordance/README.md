# Affordance package (Disclosure Functions v1)

## Purpose

Canonical artefacts for measuring **schema disclosure affordance** and preparing
the **affordance–realization gap** analysis of official public AI inventories.

Paper supplementary index (A–J): [`docs/supplements/README.md`](../../../docs/supplements/README.md).

LocalGovBench is **not** the analytical framework of this paper path.

This package does **not** measure readiness, maturity, shortfall, compliance,
governance quality, or jurisdiction rankings.

## Layers

| Layer | Location | Status |
|-------|----------|--------|
| Specification (Phase 1) | `config/`, `locks/`, `outputs/` | Frozen |
| Schema coding (Phase 2) | `coding/` | Frozen artefacts; human coding execution separate |
| Experiment pipeline (Phase 3) | `experiments/` | Active — dataset generation infrastructure |
| Realization / gap analysis | — | Later |
| Manuscript | `paper/` repo | Out of scope here |

## Canonical input

`pilot_public_satisfiability/data/pilot_programme_records.csv`  
Observed fields only from `raw_fields_json`.

## Phase 1 — specification artefacts

Hand-authored in `config/`; generated locks/inventory in `locks/` and `outputs/`.

```bash
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_specification.py --validate-only
```

**Do not edit generated inventory/lock files manually.**

## Phase 2 — schema coding layer (`coding/`)

### Purpose

Human coding of each `schema_object × disclosure_function` using frozen
support labels (`dedicated` | `indirect` | `absent`), with double-coding,
validation, disagreement export, and adjudication — **without** producing
study results, IRR numbers, or realization rates.

### Key files

| File | Role |
|------|------|
| `coding/config/codebook_affordance_v1.md` | Full operational codebook |
| `coding/config/coder_instructions_v1.md` | Session checklist |
| `coding/config/coding_labels_v1.yaml` | Frozen enumerations |
| `coding/config/schema_coding_record_v1.schema.json` | Row schema |
| `coding/config/double_coding_protocol_v1.md` | Double-coding rules |
| `coding/config/irr_analysis_plan_v1.md` | IRR plan only (no calculations) |
| `coding/examples/worked_examples_v1.md` | Worked examples |
| `coding/templates/schema_coding_template_v1.csv` | Full blank template (55 units) |
| `coding/templates/pilot_coding_manifest_v1.csv` | Pilot unit set |
| `coding/adjudication/adjudication_protocol_v1.md` | Adjudication rules |
| `coding/adjudication/adjudication_template_v1.csv` | Adjudication sheet |

**Do not edit generated templates manually** — regenerate them.

### Regeneration

```bash
python3.12 scripts/build_affordance_coding_layer.py
```

This regenerates the coding template, pilot manifest, and codebook from Phase 1.

### Validation commands

```bash
python3.12 - <<'PY'
from pathlib import Path
from localgovbench_measurement_validation.affordance.coding.validate import validate_coding_csv
print(validate_coding_csv(Path('path/to/coder_sheet.csv')))
PY
```

### Pilot Round 01 launch package

Operational packets and administration for the 33-unit human pilot:

[`pilot_round_01/`](pilot_round_01/README.md)

```bash
python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate
python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv \
  --mode pre
python3.12 scripts/dry_run_pilot_round_01.py
```

Do **not** place synthetic completed judgments in `pilot_round_01/completed_inputs/`.

### Double-coding workflow

1. Train on codebook + worked examples.  
2. Independently code pilot units.  
3. Validate each sheet.  
4. Export disagreements → adjudication input.  
5. Adjudicate; escalate specification contradictions.  
6. Only then consider full-template coding.

### Adjudication workflow

See `coding/adjudication/adjudication_protocol_v1.md`.  
Specification contradictions must not be silently “fixed” by adjudication.

## Tests

```bash
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests \
  localgovbench_measurement_validation/affordance/experiments/tests -q
```

## Phase 3 — experiment pipeline (`experiments/`)

See [`experiments/EXPERIMENT_PIPELINE.md`](experiments/EXPERIMENT_PIPELINE.md).

```bash
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id EXAMPLE \
  --coder-a path/to/coder_a.csv \
  --coder-b path/to/coder_b.csv \
  --adjudication path/to/adjudication.csv
```

Phase 3 produces matrices, manifests, and provenance. It does **not** calculate
realization rates, affordance–realization gaps, or IRR.

## Distinctions

- **Specification:** what functions/fields/applicability mean (Phase 1).  
- **Coding:** human schema support judgments (Phase 2).  
- **Realization:** record population (later).  
- **Analysis:** affordance–realization gap, figures (later).

## Out of scope here

- Human coding execution  
- IRR calculation  
- Realization rates / gap outputs  
- Figures / manuscript edits  
- Legacy moves
