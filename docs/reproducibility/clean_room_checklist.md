# Clean-room reproducibility checklist

**Purpose:** Verify what a third party can reproduce from the current tip without inventing Results.

## Distinctions

| Class | Meaning |
|-------|---------|
| **Reproducible from git alone** | Passes without corpus CSV or network |
| **Reproducible with external corpus** | Needs verified `pilot_programme_records.csv` |
| **Not yet reproducible** | Blocked (e.g. unpublished next DOI tip alignment) |
| **Intentionally unavailable** | Human coding / IRR / realization / gap Results |

## Automated check

```bash
python3.12 scripts/run_clean_room_check.py
```

Optional flags:

- `--skip-tests` — structure/install only  
- `--require-corpus` — fail if corpus missing (default: warn/skip corpus-dependent steps)

## Manual sequence (mirror of the script)

1. Fresh clone / clean worktree of the intended commit.  
2. `python3.12 -m venv .venv && source .venv/bin/activate`  
3. `pip install -e ".[dev]"`  
4. `python -c "import localgovbench; print(localgovbench.__version__)"` — must match `pyproject.toml`  
5. `python3.12 scripts/validate_repository.py`  
6. `python3.12 scripts/verify_pilot_corpus.py` — expect fail/warn if CSV absent  
7. `pytest localgovbench_measurement_validation/affordance -q`  
8. `python3.12 scripts/validate_pilot_packet.py .../pilot_round_01_coder_A.csv --mode pre`  
9. `python3.12 scripts/dry_run_pilot_round_01.py`  
10. `python3.12 paper_assets/scripts/generate_all_paper_assets.py` (Methods assets only)  
11. Confirm blank pilot judgment fields remain empty  

## Expected outcomes at current tip

| Step | Without corpus | With verified corpus |
|------|----------------|----------------------|
| Install / import / version | Pass | Pass |
| `validate_repository.py` | Pass | Pass |
| Affordance/coding/experiment tests | Pass | Pass |
| Corpus verify | Fail (expected) | Pass |
| Spec rebuild (`build_affordance_specification.py`) | Should not claim success without corpus | Pass if hash matches |
| Empirical Results tables T09–T13 | Intentionally empty | Still empty until human coding |

## Non-goals

Do not treat dry-run fixtures or empty Results placeholders as study findings.
