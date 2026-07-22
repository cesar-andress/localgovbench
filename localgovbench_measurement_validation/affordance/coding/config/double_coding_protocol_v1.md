# Double-coding protocol v1

**Specification version:** 1.0.0  
**Purpose:** Independent human schema coding with reproducible disagreement handling.

## 1. Coder training sequence

1. Read `coder_instructions_v1.md`.
2. Read `codebook_affordance_v1.md` (full).
3. Study `worked_examples_v1.md`.
4. Review Phase 1 artefacts locations (candidates, applicability, inventory) — do not memorize inventory rates.
5. Complete the **pilot** set in `pilot_coding_manifest_v1.csv` independently.

## 2. Pilot coding round

- Use only units listed in the pilot manifest.
- Two coders, fully independent.
- No discussion of cases before pilot freeze.
- Submit validated CSVs (enumerations + impossible-combination checks).

## 3. Independent coding requirement

- Separate files per coder (`coder_id` required).
- No shared working notes on disputed units until adjudication.
- Do not look at the other coder’s sheet.

## 4. No coder discussion before pilot freeze

Pilot freeze occurs only after:

- both pilot sheets validate,
- disagreements are exported,
- adjudication for pilot is complete **or** specification contradictions are escalated.

## 5. Minimum pilot unit set

Use the frozen `pilot_coding_manifest_v1.csv` (all five sources; clear/ambiguous/conditional/generic/linkage/conflict cases).  
Do not shrink the manifest without a coding-layer version bump.

## 6. Stratification

The pilot manifest already stratifies across:

- sources (US, CA, NL, PSTW, UK),
- core and module functions,
- dedicated / indirect / absent / catalogue-inapplicable / conditional traps.

## 7. Disagreement export

```bash
python3.12 - <<'PY'
from pathlib import Path
from localgovbench_measurement_validation.affordance.coding.validate import (
    export_disagreements, create_adjudication_input
)
export_disagreements(Path('coder_A.csv'), Path('coder_B.csv'), Path('disagreements.csv'))
create_adjudication_input(Path('disagreements.csv'), Path('adjudication_input.csv'))
PY
```

## 8. Adjudication sequence

1. Classify disagreement type (support / applicability / encoding / linkage).
2. Apply codebook rule cited in adjudication sheet.
3. Decide: coder error vs ambiguous semantics vs codebook ambiguity vs specification contradiction vs missing documentation.
4. **Specification contradictions must not be silently adjudicated** — escalate and pause the round.
5. Record adjudicator decision and rationale; set resolution status.

## 9. Codebook amendment rules

- Editorial clarifications that do not change labels → patch note; no full restart if pilot not yet locked.
- Changes to support definitions, applicability, or frozen candidate meanings → **version bump** and restart of affected units.
- Amendments must cite the disagreement id that triggered them.

## 10. Versioning after amendments

- Update `coding_layer_version` / codebook header.
- Regenerate templates if prepopulated caveats change.
- Record amendment in coding round metadata.

## 11. When a coding round must be restarted

Restart if any of the following occur after coding began:

- Phase 1 specification version changes,
- candidate map PRIMARY/REJECTED changes for coded units,
- applicability overrides change for coded units,
- more than a trivial fraction of pilot units are invalidated by a codebook fix (**TO BE DETERMINED AFTER PILOT REVIEW** for exact fraction),
- specification contradiction is confirmed.

## Statistical thresholds

Agreement cutoffs for proceeding from pilot to full coding:

**TO BE DETERMINED AFTER PILOT REVIEW**

Do not invent a universal κ ≥ x gate in this protocol.
