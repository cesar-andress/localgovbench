# Supplement F — Experimental pipeline

## Purpose

Document the **Phase 3 experiment pipeline**: how completed (and, where required, adjudicated) schema coding is imported into reproducible datasets — schema affordance matrix, manifests, provenance, and realization **input templates** — without calculating realization rates, gaps, or IRR.

Authoritative narrative: `affordance/experiments/EXPERIMENT_PIPELINE.md`.

## Inputs

| Input | Role |
|-------|------|
| Completed coder sheet(s) | CSV/JSON/Parquet coding records |
| Optional adjudication file | Required when A and B disagree on merge fields |
| Frozen Phase 1–2 artefacts | Spec, inventory, labels (read-only) |
| CLI | `scripts/run_affordance_experiment_pipeline.py` |

Typical flags: `--experiment-id`, `--coder-a` / `--coder-b` or `--single-coder`, `--adjudication`, `--allow-partial`, `--operator`, `--output-root`.

Pilot-oriented command recipes: `affordance/coding/pilot_round_01/import_commands/pilot_round_01_commands.md`.

## Outputs

| Output class | Location pattern (under `affordance/experiments/`) |
|--------------|-----------------------------------------------------|
| Affordance matrix | `outputs/` |
| Finalized coding | `outputs/` |
| Realization **input templates** (placeholders) | `outputs/` |
| Experiment / realization manifests | `manifests/` |
| Provenance + merge logs | `provenance/` |
| Validation reports | `validation/` |
| Archived inputs | `inputs/archive/<experiment_id>/` |

### Table F1 — Pipeline responsibilities vs non-responsibilities

| Does | Does **not** |
|------|----------------|
| Import and validate coding | Calculate record-level realization rates |
| Merge A/B with adjudication rules | Calculate affordance–realization gaps |
| Build schema affordance matrix | Calculate IRR coefficients |
| Write provenance and manifests | Emit publication result tables as completed findings |
| Emit realization **templates** for later stages | Treat templates as filled empirical results |

### Textual flowchart (infrastructure only)

```text
Completed coding (A [, B])
        │
        ├─► validate independently (Supplement E)
        │
        ├─► [if dual] export disagreements → adjudication input → adjudicate
        │
        └─► run_affordance_experiment_pipeline.py
                 │
                 ├─► finalized coding + merge log
                 ├─► schema affordance matrix
                 ├─► manifests + provenance
                 └─► realization input templates (empty of study rates)
```

## Figures

No publication result figure. The flowchart above is procedural.

## Limitations

1. **Archive tip vs `main`:** Phase 3 files may be present on development `main` but absent from an older Zenodo/`v0.2.0` tip — cite the commit that contains `EXPERIMENT_PIPELINE.md` when reproducing (see Supplements G/J).  
2. Dual-coder merge is strict when judgment fields disagree; operators should follow disagreement export before assuming a one-shot A+B run succeeds.  
3. `--allow-partial` is required for the 33-unit pilot subset relative to the 55-unit full design.  
4. Fixture dry-runs (`scripts/dry_run_pilot_round_01.py`, `NON_SUBSTANTIVE_TEST_FIXTURE`) are **not** study data.

## Cross references

| Topic | See |
|-------|-----|
| Coding framework | [Supplement D](D_coding_framework.md) |
| Validation | [Supplement E](E_validation_rules.md) |
| Reproducibility commands | [Supplement G](G_reproducibility.md) |
| Pipeline doc (authoritative) | `affordance/experiments/EXPERIMENT_PIPELINE.md` |
| Affordance README (Phase 3) | `affordance/README.md` |
