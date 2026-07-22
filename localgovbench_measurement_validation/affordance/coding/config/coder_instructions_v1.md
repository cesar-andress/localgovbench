# Coder instructions v1 — Schema disclosure affordance

**Use with:** `codebook_affordance_v1.md` and the prepopulated coding template.  
**Specification version:** 1.0.0  
**Unit:** `schema_object × disclosure_function`

## Exact coding order

1. Confirm **schema object** (`source_name`, `schema_object_type`).
2. Confirm **applicability** using defaults/overrides (do this before support).
3. Review **PRIMARY** candidates from `known_field_mapping_labels`.
4. Review **SECONDARY** candidates.
5. Review **INDIRECT** candidates.
6. Review **REJECTED** candidates (must not become primary evidence).
7. Apply **generic-field anti-over-credit** rules.
8. Assign **support_level**: `dedicated` | `indirect` | `absent`.
9. Assign **encoding_type**: `free_text` | `structured` | `mixed` | `other` | `not_applicable`.
10. Assign **documentary_linkage_layer**: `generic_url` | `record_locator` | `function_specific` | `none` | `not_applicable`.
11. Record **coder_rationale** (brief, field-referenced).
12. Record **coder_confidence** (`high` | `medium` | `low`) — metadata only.
13. Flag **unresolved_issue** when needed (`unknown` applicability requires this).

## Quick label reminders

| If applicability is… | Then support must… |
|----------------------|--------------------|
| `catalogue_inapplicable` | not be `dedicated` or `indirect` (use `absent`) |
| `unknown` | include non-empty `unresolved_issue` |

| If support is… | Then fields must… |
|----------------|-------------------|
| `dedicated` | list ≥1 `primary_supporting_fields` |
| `indirect` | list ≥1 `indirect_supporting_fields` |
| `absent` | leave `primary_supporting_fields` empty |

## Hard prohibitions

- Do **not** infer content the schema does not expose.
- Do **not** code from record population rates.
- Do **not** treat a generic URL as function-specific evidence.
- Do **not** treat organisational quality / readiness / maturity as schema support.
- Do **not** use knowledge outside frozen artefacts unless the coding round explicitly authorizes external documentation.
- Do **not** let confidence change support level.
- Do **not** fill `adjudicated_value` before adjudication.

## Frozen traps

- UK `description` → purpose **INDIRECT** only (never dedicated).
- UK `organisation_title` → accountable body **INDIRECT** only (never dedicated).
- PSTW outcome flags (`Improved…`, etc.) → **REJECTED** for risk.
- NL `proportionality` → **REJECTED** for all functions.
- NL `impacttoetsen` → **not PRIMARY** risk.
- Identity (`cf_system_identity`) → **descriptive_only**.

## After each sheet

Run validation before submission (see affordance README). Leave disagreements for export; do not confer with the other coder during independent coding.
