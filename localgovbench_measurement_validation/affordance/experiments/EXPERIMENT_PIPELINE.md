# Experiment pipeline — Phase 3

**Status:** ACTIVE  
**Pipeline version:** 1.0.0  
**Does not:** calculate realization, affordance–realization gaps, IRR, or publication tables.

## Purpose

Transform **completed human schema coding** into reproducible analytical datasets
for schema disclosure affordance, with validation, adjudication merge, provenance,
and experiment manifests.

Frozen Phase 1 (specification) and Phase 2 (coding) artefacts are **inputs only**.

## Directory layout

```
affordance/experiments/
  config/          pipeline config + matrix schema
  inputs/          optional staged imports; archives under inputs/archive/<id>/
  outputs/         matrix, finalized coding, realization templates
  manifests/       experiment + realization manifests
  provenance/      provenance JSON + merge logs
  validation/      validation reports
  fixtures/        test builders
  tests/           automated tests
```

## Inputs

| Artefact | Role |
|----------|------|
| Disclosure Functions v1 | Function IDs |
| Corpus lock | SHA-256 binding |
| Schema inventory | Object layer / inventory version |
| Coding labels + record schema | Enum validation |
| Completed coder sheets (CSV/JSON; Parquet if available) | Judgments |
| Adjudication sheet (when A≠B) | Resolutions |
| Pilot manifest / full template | Expected unit universe |

## Execution order

1. **Import** coder sheets → reject malformed / duplicate / missing / unknown IDs.  
2. **Archive** original inputs (never overwrite).  
3. **Merge** coder A + B + adjudication → finalized coding.  
4. **Build** schema-affordance matrix (`schema_object × disclosure_function`).  
5. **Export** CSV + JSON (+ Parquet when available).  
6. **Write** experiment manifest + provenance + merge log.  
7. **Validate** matrix / manifest / provenance.  
8. **Prepare** realization input template + realization manifest (**placeholders only**).

### CLI

```bash
# Double-coding + adjudication
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id pilot_affordance_001 \
  --coder-a path/to/coder_a.csv \
  --coder-b path/to/coder_b.csv \
  --adjudication path/to/adjudication.csv \
  --operator researcher \
  --output-root path/to/output_dir

# Single finalized sheet
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id solo_001 \
  --single-coder path/to/final.csv

# Pilot subset (not full 55 units)
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id pilot_subset \
  --coder-a a.csv --coder-b b.csv \
  --allow-partial
```

Optional: `--output-root` redirects manifests/outputs/provenance away from the default experiment directories.

## Outputs

| Output | Description |
|--------|-------------|
| `*_schema_affordance_matrix.{csv,json[,parquet]}` | Canonical affordance matrix |
| `*_finalized_coding.*` | Merged coding rows |
| `*_realization_input_template.*` | Blank realization placeholders |
| `*_experiment_manifest.json` | Experiment metadata |
| `*_realization_manifest.json` | Declares realization **not** calculated |
| `*_provenance.json` | Software/git/spec/coding/corpus/generator/timestamp |
| `*_merge_log.json` | Per-unit merge provenance |
| `*_validation_report.json` | Automated validation result |

### Matrix columns

`schema_object_id`, `source_name`, `schema_object_type`, `disclosure_function_id`,
`support_level`, `applicability_label`, `encoding_type`, `documentary_linkage_layer`,
`function_specific_link_type`, `coder_confidence`, `adjudication_status`,
`adjudicated_from`, `coding_round_id`, `specification_version`, `coding_version`,
`corpus_lock_sha256`, `schema_inventory_version`, `experiment_id`, `pipeline_version`.

**No realization variables.**

## Provenance fields

Every run records: `software_version`, `git_commit`, `specification_version`,
`coding_version`, `corpus_lock_sha256`, `generator_script`, `creation_timestamp_utc`,
`pipeline_version`, `operator`, input/output paths.

## Validation rules

- Unknown sources / function IDs rejected  
- Duplicate coding units rejected  
- Missing expected units rejected (unless `--allow-partial`)  
- Invalid enums / specification version / corpus lock rejected  
- Orphan adjudications rejected  
- Unresolved disagreements without adjudication rejected  
- Matrix must not contain realization/gap/IRR result fields  
- Manifests and provenance must include required metadata fields  

## Determinism

Repeated runs with identical coding inputs produce **byte-identical** matrix CSV/JSON
content (same rows, columns, sort order). Provenance timestamps differ by design.

## Experiment lifecycle

```
coding complete → import/validate → merge/adjudicate → matrix export
  → (future) realization fill-in → (future) gap analysis → (future) tables
```

## Future phases (not implemented here)

| Phase | Work |
|-------|------|
| Realization | Fill `realization_status` from record-level rules; compute rates |
| Gap analysis | Affordance–realization gaps; figures |
| IRR | Calculate agreement statistics from double-coding |

## Tests

```bash
python3.12 -m pytest \
  localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests \
  localgovbench_measurement_validation/affordance/experiments/tests -q
```
