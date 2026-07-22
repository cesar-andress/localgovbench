# Supplement D — Coding framework

## Purpose

Document the **human schema-coding framework** for Disclosure Functions v1: codebook, label system, record schema, full template (55 units), pilot manifest (33 units), double-coding / adjudication protocols, worked examples, and the operational pilot launch package.

This supplement describes **instruments and procedures**. It does **not** contain completed coder judgments, IRR results, or adjudicated study matrices.

## Inputs

| Input | Path |
|-------|------|
| Disclosure Functions v1 + candidates + applicability | Supplement C / `affordance/config/` |
| Schema inventory | Supplement B |
| Corpus lock reference | Supplement A |
| Builder | `scripts/build_affordance_coding_layer.py` |
| Pilot packet generator | `python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate` |

## Outputs

### Table D1 — Coding artefacts index

| Artefact | Path | Role |
|----------|------|------|
| Codebook | `affordance/coding/config/codebook_affordance_v1.md` | Operational coding rules |
| Coder instructions | `affordance/coding/config/coder_instructions_v1.md` | Session procedure |
| Coding labels | `affordance/coding/config/coding_labels_v1.yaml` | Frozen enumerations |
| Coding record schema | `affordance/coding/config/schema_coding_record_v1.schema.json` | Row schema |
| Double-coding protocol | `affordance/coding/config/double_coding_protocol_v1.md` | Independence & freeze rules |
| IRR analysis plan | `affordance/coding/config/irr_analysis_plan_v1.md` | Plan only (no coefficients) |
| Worked examples | `affordance/coding/examples/worked_examples_v1.md` | Training examples |
| Full blank template | `affordance/coding/templates/schema_coding_template_v1.csv` | 55 coding units |
| Pilot manifest | `affordance/coding/templates/pilot_coding_manifest_v1.csv` | 33-unit pilot selection |
| Adjudication protocol | `affordance/coding/adjudication/adjudication_protocol_v1.md` | Resolution rules |
| Adjudication template | `affordance/coding/adjudication/adjudication_template_v1.csv` | Adjudication sheet |
| Pilot launch package | `affordance/coding/pilot_round_01/` | Blank packets A/B + admin docs |

### Table D2 — Coding unit design

| Quantity | Value | Notes |
|----------|------:|-------|
| Schema objects (sources) | 5 | Same five sources as corpus |
| Disclosure functions | 11 | Supplement C |
| Full template units | 55 | \(5 \times 11\) |
| Pilot units | 33 | Subset with selection rationales in pilot manifest |
| Independent coder slots | 2 | Anonymous `coder_A`, `coder_B` |

### Support labels (frozen)

`dedicated` | `indirect` | `absent`  
(plus applicability, encoding, documentary linkage, and confidence enumerations — Supplement E)

### Pilot launch (operational)

Blank packets (judgment fields empty; frozen context prepopulated):

- `affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv`  
- `affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_B.csv`  

Administration: `pilot_round_01/administration/`  
Readiness: `pilot_round_01/validation/pilot_launch_readiness_v1.md`  
Commands: `pilot_round_01/import_commands/pilot_round_01_commands.md`

**Critical boundary:** do not prefill `support_level`, encoding/linkage judgments, confidence, rationales, or adjudicated values. Coders must not compare answers before both completed sheets are frozen.

## Figures

None. Worked examples are textual (`worked_examples_v1.md`).

## Limitations

1. Templates and blank packets are **instruments**, not results.  
2. IRR plan exists; **no IRR coefficients** are computed in this repository stage.  
3. Adjudication resolves coder disagreement; it must **not** silently rewrite the specification (see adjudication protocol).  
4. Pilot is a subset of the full 55-unit design; full-template coding is a later operational decision.  
5. Link path note: from `affordance/README.md`, the pilot directory is under `coding/pilot_round_01/` (not `affordance/pilot_round_01/`).

## Cross references

| Topic | See |
|-------|-----|
| Functions | [Supplement C](C_disclosure_functions_v1.md) |
| Validation / enums | [Supplement E](E_validation_rules.md) |
| Post-coding pipeline | [Supplement F](F_experimental_pipeline.md) |
| Affordance coding README section | `affordance/README.md` |
| Codebook (authoritative) | `affordance/coding/config/codebook_affordance_v1.md` |
