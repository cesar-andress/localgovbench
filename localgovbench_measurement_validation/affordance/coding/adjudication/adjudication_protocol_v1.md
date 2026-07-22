# Adjudication protocol v1

## Purpose

Resolve coder disagreements on `schema_object × disclosure_function` without silently rewriting the Phase 1 specification.

## Disagreement classes

| Class | Meaning | Action |
|-------|---------|--------|
| coder_error | Misread of field/map/rule | Correct to codebook; note error |
| ambiguous_field_semantics | Observed field role unclear | Prefer frozen candidate label; else escalate |
| codebook_ambiguity | Codebook text underspecified | Amend codebook (versioned); may restart units |
| specification_contradiction | Phase 1 artefacts conflict | **Do not silently adjudicate**; escalate |
| missing_schema_documentation | Inventory insufficient | Mark `unknown` / unresolved; escalate |

## Process

1. Start from `adjudication_template_v1.csv` (or generated adjudication input).
2. Cite `relevant_codebook_rule` (section or anti-over-credit id).
3. Fill `adjudicator_decision` using the same enumerations as coding labels.
4. Set flags:
   - `codebook_ambiguity_flag` = yes/no
   - `specification_ambiguity_flag` = yes/no
5. If specification contradiction: `resolution_status=escalated_specification_contradiction` and stop the round for that unit family.
6. Otherwise set `resolution_status=resolved` and record date + version.

## Prohibitions

- Do not invent PRIMARY fields absent from the candidate map.
- Do not use realization rates.
- Do not “split the difference” into a new support label.
- Do not fill adjudicated values on independent coding sheets before this protocol runs.
