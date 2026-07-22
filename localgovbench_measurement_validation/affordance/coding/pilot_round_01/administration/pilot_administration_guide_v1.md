# Pilot administration guide — Disclosure Functions v1 (`pilot_round_01`)

## 1. Purpose of the pilot

Independent human coding of **33** `schema_object × disclosure_function` units
to stress-test the codebook, anti-over-credit rules, and applicability handling
before any full-template coding.

## 2. What the pilot is intended to detect

- Ambiguous codebook language
- Difficult PRIMARY / INDIRECT / REJECTED distinctions
- Applicability edge cases (conditional, jurisdiction-specific, catalogue_inapplicable)
- Procedural issues (file handling, validation, handoff)

It is **not** intended to produce publication IRR, realization rates, or gap results.

## 3. Independent-coding requirement

Coder A and Coder B must code independently. Each receives an identical unit
universe with frozen context only.

## 4. Prohibition on coder discussion before freeze

Coders must **not** compare answers, share rationales, or discuss units until
**both** completed files are frozen and checksummed.

## 5. Permitted reference materials

Only materials listed in `locked_reference/pilot_reference_manifest_v1.json`:

- codebook
- coder instructions
- worked examples
- coding labels / record schema
- Disclosure Functions v1 specification artefacts
- corpus lock / pilot manifest (context)

## 6. Prohibited external inference

Do not:

- use record-population rates or inventory browsing to “improve” affordance codes
- invent fields not in the observed candidate list
- treat generic URLs as function-specific documentary linkage
- copy answers from worked examples for the same unit
- consult the other coder

## 7. How to record unresolved issues

Use `unresolved_issue` and set applicability to `unknown` when required by the
codebook. Prefer flagging over guessing.

## 8. How to save and return files

Save as CSV UTF-8. Do not change column order, delete rows, or rename
`coding_unit_id` / `coding_record_id`.

## 9. File-naming rules

Blank packets:

- `pilot_round_01_coder_A.csv`
- `pilot_round_01_coder_B.csv`

Completed returns:

- `pilot_round_01_coder_A_completed.csv`
- `pilot_round_01_coder_B_completed.csv`

## 10. Freeze procedure

1. Coder finishes sheet.
2. Run post-coding validation (see `import_commands/`).
3. Compute SHA-256 of the completed file.
4. Place under `completed_inputs/` (or a secure intake location if VC-excluded).
5. Record checksum beside the file name.
6. Do not silently overwrite; version corrections as `_v2`, `_v3`, etc.

## 11. Import procedure

Validate each coder independently, then run the Phase 3 pipeline with
`--allow-partial` (33 of 55 units). See `import_commands/pilot_round_01_commands.md`.

## 12. Disagreement export procedure

Use `export_disagreements` from the coding validation module on the two
completed sheets.

## 13. Adjudication sequence

1. Export disagreements.
2. Create adjudication input worksheet.
3. Adjudicate under `adjudication_protocol_v1.md`.
4. Re-run Phase 3 pipeline with adjudication file.
5. Escalate specification contradictions; do not silently rewrite the codebook.

## 14. Codebook-amendment procedure

If adjudication reveals a specification/codebook contradiction:

1. Freeze current pilot files.
2. Document the issue.
3. Amend codebook/specification only via an explicit version bump.
4. Restart affected coding units under the new version.

## 15. Restart conditions

Restart (full or partial) if:

- blank packets were edited after distribution
- frozen context columns changed
- wrong corpus lock / specification version used
- codebook amended mid-round without version bump

## 16. Data protection and backup

- Keep local backups of completed sheets.
- Do not commit personal names/emails into packets.
- Prefer anonymous slots `coder_A` / `coder_B` in `coder_id` when submitting.
- Follow repository policy before committing any completed research inputs.
