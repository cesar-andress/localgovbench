# Supplement E — Validation rules

## Purpose

Summarise the **validation and label constraints** that protect coding integrity and experiment imports: frozen enumerations, coding-sheet validation, pilot packet validation (pre/post), and experiment-matrix validation. Full rule logic remains in code and schemas.

## Inputs

| Input | Path |
|-------|------|
| Coding labels | `affordance/coding/config/coding_labels_v1.yaml` |
| Coding record JSON Schema | `affordance/coding/config/schema_coding_record_v1.schema.json` |
| Coding validators | `affordance/coding/validate.py` |
| Pilot validators | `scripts/validate_pilot_packet.py`; `affordance/coding/pilot_launch.py` |
| Experiment validators | `affordance/experiments/validate_experiment.py` |
| Spec validators | `affordance/validate_specs.py` |

## Outputs

Validation does not produce scientific findings. It produces **pass/fail diagnostics** (and, in the experiment pipeline, validation report JSON under `affordance/experiments/validation/` when a run is executed).

### Table E1 — Principal frozen enumerations (coding labels v1.0.0)

| Dimension | Allowed values (abbreviated) |
|-----------|------------------------------|
| `support_level` | `dedicated`, `indirect`, `absent` |
| `applicability_label` | `universal`, `conditional`, `jurisdiction_specific`, `object_specific`, `catalogue_inapplicable`, `unknown` |
| `encoding_type` | `free_text`, `structured`, `mixed`, `other`, `not_applicable` |
| `documentary_linkage_layer` | `generic_url`, `record_locator`, `function_specific`, `none`, `not_applicable` |
| `function_specific_link_type` | impact assessment, dataset documentation, source code, legal/policy, procurement, appeal process, … (see YAML) |
| `coder_confidence` | (see YAML; metadata — must not alter support) |

Authoritative list: `coding_labels_v1.yaml`.

### Table E2 — Validation surfaces

| Surface | What is checked | Entry point |
|---------|-----------------|-------------|
| Hand-authored DF specs | Catalogue / candidates / overrides consistency | `build_affordance_specification.py --validate-only` or `validate_specs` |
| Coding CSV | Schema, enums, impossible combinations, unit identity | `affordance.coding.validate.validate_coding_csv` |
| Pilot packet (pre) | 33 rows, IDs, empty judgment fields, frozen refs | `scripts/validate_pilot_packet.py --mode pre` |
| Pilot packet (post) | Required judgments, enums, frozen context unchanged, no A↔B comparison | `scripts/validate_pilot_packet.py --mode post` |
| Experiment matrix | Unit coverage, merge log consistency, forbidden result keys | `affordance/experiments/validate_experiment.py` |

Impossible-combination examples (illustrative; full logic in validators/codebook): e.g. `catalogue_inapplicable` paired with dedicated support; missing indirect fields when `support_level=indirect`; adjudicated values present on independent coder sheets before adjudication.

## Figures

None.

## Limitations

1. Validators enforce **instrument integrity**, not substantive correctness of a coder’s theoretical interpretation beyond coded rules.  
2. Post-coding pilot validation **must not compare** Coder A vs Coder B (by design).  
3. Experiment validation may reject incomplete universes unless `--allow-partial` is used (pilot subsets).  
4. Disagreement export / adjudication-input helpers are procedural (Supplement D/F), not automatic “truth.”

## Cross references

| Topic | See |
|-------|-----|
| Coding instruments | [Supplement D](D_coding_framework.md) |
| Pipeline validation reports | [Supplement F](F_experimental_pipeline.md) |
| Labels YAML | `affordance/coding/config/coding_labels_v1.yaml` |
| Codebook consistency rules | `affordance/coding/config/codebook_affordance_v1.md` |
