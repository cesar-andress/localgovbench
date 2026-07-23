# Next release candidate — LocalGovBench **0.2.1** (UNRELEASED)

**Status:** Release candidate documentation only.  
**Do not** treat this file as a published deposit.  
**Do not** invent a DOI.

## Proposed version

| Item | Value |
|------|-------|
| Proposed software version | **0.2.1** |
| Rationale | Patch release: Phase 3 pipeline + pilot launch + supplements/`paper_assets` already on `main` after tag `v0.2.0`, plus release-engineering/reproducibility fixes. No methodology redesign. |
| Specification / coding / pipeline versions | Remain **1.0.0** |
| Future DOI placeholder | `10.5281/zenodo.NEXT_DOI_TBD` |
| Published citation (unchanged) | v0.2.0 — DOI `10.5281/zenodo.21500899` |

**Exact statement:** Published software **v0.2.0** (tag `v0.2.0`, DOI `10.5281/zenodo.21500899`) **remains historical and unchanged**. It does **not** contain Phase 3 or the pilot launch package. This document prepares a **future** release from current `main`; publication requires a human tag + Zenodo deposit.

## Scope since v0.2.0

- Phase 3 experiment pipeline (`affordance/experiments/`, `scripts/run_affordance_experiment_pipeline.py`)
- Pilot Round 01 launch package (blank coder packets A/B, admin docs, validators)
- Supplements A–J (`docs/supplements/`)
- Manuscript `paper_assets/` Methods scaffolds (no fabricated Results)
- Release-readiness remediation (version sync, docs truth, CI, corpus verification, legacy notices)

## Known limitations

- Human pilot coding not executed for publication Results  
- No IRR / realization / affordance–realization gap figures  
- Aggregated corpus CSV not in git by default (see `docs/reproducibility/corpus_acquisition.md`)  
- Next Zenodo DOI not minted (`NEXT_DOI_TBD`)

## Corpus distribution status

**BLOCKED — HUMAN DECISION / EXTERNAL DATA** for committing or publishing the aggregate CSV. Verification script: `scripts/verify_pilot_corpus.py`. Reconstruction may be attempted via `scripts/build_pilot_corpus.py` when network/licensing allow; frozen SHA must match.

## Absent scientific results (do not claim)

Completed dual coding, IRR coefficients, realization rates, gap analyses.

## Migration notes

- Runtime/`pyproject.toml` version on `main` may read **0.2.1** while `CITATION.cff` continues to cite **published 0.2.0** until the next deposit.  
- Prefer portable corpus paths (`canonical_path` / `portable_path`) over historical `absolute_path` in the lock.  
- Adjudication merge requires disagreement only on substantive judgment fields (not confidence/rationale alone).

## Validation commands

```bash
pip install -e ".[dev]"
python3.12 scripts/validate_repository.py
python3.12 scripts/verify_pilot_corpus.py --lock-only
pytest localgovbench_measurement_validation/affordance tests/test_version_consistency.py tests/test_active_documentation_claims.py tests/test_legacy_notices.py -q
python3.12 scripts/run_clean_room_check.py
```

## Release checklist (human)

- [ ] Confirm corpus redistribution decision (commit / Zenodo data / verify-only)  
- [ ] Update `CITATION.cff` + `.zenodo.json` for 0.2.1 **only at publish time**  
- [ ] Replace `NEXT_DOI_TBD` with the real version DOI after minting  
- [ ] Create annotated tag `v0.2.1` on the freeze commit  
- [ ] Push tag; create GitHub Release; upload Zenodo version  
- [ ] Do **not** modify or overwrite the v0.2.0 Zenodo record  

## Validation of this document

This file is required by `scripts/validate_repository.py` and must retain the `NEXT_DOI_TBD` placeholder until a real DOI exists.
