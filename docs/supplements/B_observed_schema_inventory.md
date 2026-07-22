# Supplement B — Observed schema inventory

## Purpose

Document the **observed-field schema inventory** derived from the locked corpus: which raw field names appear under each source’s `raw_fields_json`, how they are normalised, and which inventory columns are published for downstream candidate mapping and coding.

This supplement describes a **generated Phase 1 artefact**. It does not assign disclosure-function support labels.

## Inputs

| Input | Path / role |
|-------|-------------|
| Frozen corpus | Supplement A; SHA-256 in corpus lock |
| Field normalization rules | `affordance/config/field_normalization_rules_v1.yaml` |
| Builder | `affordance/schema_inventory.py` via `scripts/build_affordance_specification.py` |

## Outputs

| Output | Path |
|--------|------|
| Inventory (CSV) | `affordance/outputs/schema_inventory_v1.csv` |
| Inventory (JSON) | `affordance/outputs/schema_inventory_v1.json` |
| Inventory version | `1.0.0` (field `schema_inventory_version`) |
| Corpus lock reference | SHA-256 of the locked corpus (column `corpus_lock_reference`) |

**Do not hand-edit** generated inventory files; regenerate with the specification builder.

### Table B1 — Inventory columns

| Column | Meaning |
|--------|---------|
| `source_name` | Inventory source identifier |
| `raw_field_name` | Key as observed in `raw_fields_json` |
| `normalized_field_name` | Name after normalization rules |
| `observed_record_count` | Records in which the key was observed |
| `source_record_count` | Total records for the source |
| `presence_rate` | Observation presence among source records |
| `nonempty_count` / `nonempty_rate` | Non-empty value statistics (population helper; not affordance coding) |
| `inferred_data_type` | Inferred type hint |
| `object_layer` | Schema object layer for the source |
| `normalization_rule_applied` / `normalization_rule_type` | Rule provenance |
| `value_class_counts_json` | Value-class histogram (JSON) |
| `schema_inventory_version` | Inventory schema version |
| `corpus_lock_reference` | Corpus SHA-256 |

### Table B2 — Observed field counts by source (inventory rows)

Counts are **numbers of distinct observed raw fields** in the frozen inventory CSV (155 rows total), not coding units.

| Source | Object layer | Observed fields (rows) |
|--------|--------------|----------------------:|
| CA-GC-AI-REG | `ai_system_register` | 24 |
| EU-PSTW | `case_catalogue` | 56 |
| NL-ALGO-REG | `algorithm_register` | 32 |
| UK-ATRS | `search_api_slim` | 7 |
| US-OMB-2025 | `use_case_inventory` | 36 |
| **Total** | | **155** |

**Source:** `affordance/outputs/schema_inventory_v1.csv` as frozen in the repository.

## Figures

None in this supplement. Optional heatmaps of presence/nonempty rates are **not** included here to avoid implying affordance or realization findings.

## Limitations

1. Inventory statistics (`presence_rate`, `nonempty_rate`) describe **field observation / population patterns**, not whether a field is dedicated support for a disclosure function.  
2. Normalization can preserve awkward raw names (e.g. leading spaces) when rules say so; raw names remain the observational ground truth.  
3. Candidate mappings to functions are a **separate** config (`field_function_candidates_v1.csv`); see Supplement C.  
4. Regenerating the inventory without the exact corpus bytes will fail SHA checks (Supplement A / G).

## Cross references

| Topic | See |
|-------|-----|
| Corpus lock | [Supplement A](A_corpus.md) |
| Function catalogue & candidates | [Supplement C](C_disclosure_functions_v1.md) |
| Coding units built on inventory + candidates | [Supplement D](D_coding_framework.md) |
| Affordance README | `affordance/README.md` |
| Normalization config | `affordance/config/field_normalization_rules_v1.yaml` |
