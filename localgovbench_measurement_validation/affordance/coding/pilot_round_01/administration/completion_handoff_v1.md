# Completion and handoff — `pilot_round_01`

## Expected returned filenames

- `pilot_round_01_coder_A_completed.csv`
- `pilot_round_01_coder_B_completed.csv`

## Placement

Preferred intake path (operational):

`localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/`

If repository policy excludes potentially identifying research inputs from
version control, store completed sheets in a secure intake location and keep
only checksums / intake log in git.

## Preserve originals

1. Keep the blank packet unchanged.
2. Never overwrite a completed file in place after freeze.
3. Corrections → new filename with version suffix, e.g.
   `pilot_round_01_coder_A_completed_v2.csv`.

## SHA-256

```bash
sha256sum pilot_round_01_coder_A_completed.csv
sha256sum pilot_round_01_coder_B_completed.csv
```

Record digests in the intake log.

## Freeze

A sheet is frozen when:

- post-coding validation passes
- SHA-256 is recorded
- the file is copied to intake
- no further silent edits are allowed

## Preventing silent edits

- Prefer write-protect / read-only permissions after freeze
- Keep checksums in `checksums/` or intake log
- Re-validate if any byte changes

## Validation failures

- Do not import failing sheets into the Phase 3 pipeline
- Return the validation error list to the coder
- After fix, bump version suffix and re-freeze

## What not to do

- Do not invent completed sheets for testing inside `completed_inputs/`
- Do not compare A vs B before both files are frozen
- Do not adjudicate inside the coder sheet
