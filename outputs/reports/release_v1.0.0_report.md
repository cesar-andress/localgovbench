# Release report — LocalGovBench v1.0.0

**Role:** Release Manager / Research Software Engineer  
**Repository:** `~/papers/localgovbench/localgovbench`  
**Remote:** `git@github.com-ucjc:cesar-andress/localgovbench.git`  
**Date:** 2026-07-30  
**Scope:** Repository curation and release engineering only. **No** empirical re-runs, mapping changes, benchmark redesign, or dataset mutation.

---

## Decision summary

| Action | Count / note |
|--------|----------------|
| **DELETE** (tracked) | 0 scientific files |
| **DELETE** (local only) | `__pycache__` / `*.pyc` trees (already gitignored) |
| **ARCHIVE** | `repository_audit.md` → `docs/audits/repository_audit_pre_v1.md` |
| **KEEP** | All scientific code, DF artefacts, GRB/legacy packages, validation, supplements, paper_assets |
| **ADD (track frozen)** | Pilot `outputs/*` + `source_registry_expanded.csv` (pre-existing freeze; not regenerated) |
| **VERSION** | Software metadata → **1.0.0**; annotated tag `v1.0.0` |

---

## Phase 1 — Repository audit (KEEP / ARCHIVE / DELETE)

### KEEP (required for reproducibility / manuscript / Zenodo)

| Path | Why |
|------|-----|
| `localgovbench/` package | Runtime library + legacy GRB/framework |
| `localgovbench_measurement_validation/affordance/` | Disclosure Functions v1 (specification, coding, experiments) |
| `localgovbench_measurement_validation/pilot_public_satisfiability/` | Manuscript empirical freeze (rules, figures, reports, now tracked outputs) |
| `scripts/` (all) | DF builders, pilot pipeline, GRB/validation utilities — uncertain → keep |
| `docs/`, `docs/supplements/`, `docs/releases/`, `docs/reproducibility/` | Public documentation |
| `paper_assets/`, `paper_data_policy/` | Manuscript scaffolds + freeze notes |
| `data/` templates, synthetic, benchmark, traceability | Reproducibility fixtures |
| `validation/`, `examples/`, `prompts/`, `tests/` | Historical + active tests |
| `results/`, `reports/` (tracked allowlists) | Legacy GRB outputs with notices |
| `LICENSE`, `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.zenodo.json`, `.github/` | Release quality |
| `pyproject.toml`, `README.md` | Install + entrypoint |

### ARCHIVE

| Path | Why |
|------|-----|
| `repository_audit.md` → `docs/audits/repository_audit_pre_v1.md` | Pre-v1 audit trail; not an active entrypoint |

### DELETE

| Path | Why |
|------|-----|
| Local `__pycache__/` / `*.pyc` | Build artefacts only; already ignored; removed from working tree |
| **No tracked scientific/obsolete experiment deletions** | Uncertainty rule: keep GRB scripts, Delphi exports tooling, LLM benchmarks |

### Explicitly not deleted (uncertain / still referenced)

- All `scripts/run_grb_*.py`, Delphi, IRR, Monte Carlo scripts  
- `exports/`, `figures/grb_monte_carlo/`, synthetic municipality corpora  
- Root-level historical docs with LEGACY banners  

### Ignored / not redistributed (documented warnings)

| Path | Status |
|------|--------|
| `.venv/`, `.pytest_cache/`, `localgovbench.egg-info/` | Local only (gitignore) |
| `data/pilot_programme_records.csv` (~27 MB) | Ignored by `*.csv`; reconstruct via `build_pilot_corpus.py` |
| Generic `outputs/` (workflow demos) | Ignored except this release report path |
| Untracked `data/corpus_candidates_day1.csv` | Ignored candidate dump — leave local |

---

## Phase 2 — Clean-up performed

1. Removed local `__pycache__` directories (not committed).  
2. Archived root `repository_audit.md` under `docs/audits/`.  
3. Extended `.gitignore` to **allow** frozen pilot outputs + source registry + this report.  
4. **Force-added** existing freeze files under `pilot_public_satisfiability/outputs/` (no regeneration).  

---

## Phase 3 — Repository quality

| Artefact | Status |
|----------|--------|
| `README.md` | Updated for v1.0.0 + manuscript freeze section |
| `LICENSE` | MIT present |
| `CITATION.cff` | version **1.0.0**; prior DOIs under identifiers |
| `CHANGELOG.md` | **[1.0.0] — 2026-07-30** entry |
| `CONTRIBUTING.md` | Present |
| `.zenodo.json` | version **1.0.0**; related_identifiers to v0.2.0 / v0.1.0 |
| GitHub | `origin` configured; CI workflow retained |
| Structure | Documented in README §5 |
| `pyproject.toml` | **1.0.0**, Production/Stable classifier |
| Requirements | `pyyaml` runtime; `pytest`/`matplotlib` in `[dev]` |

---

## Phase 4 — Reproducibility audit

| Check | Result |
|-------|--------|
| External researcher can locate DF path | Yes — `affordance/README.md` |
| External researcher can locate manuscript freeze | Yes — `pilot_public_satisfiability/` + `paper_data_policy/results_freeze.md` |
| Execution order documented | Yes — README §§6–8; pilot README reproduce blocks |
| Inputs/outputs clear | Yes — tables in pilot README; DF README |
| Folder notices | Legacy/non-DF notices retained where required |
| Validator | `scripts/validate_repository.py` **PASS** |
| Tests | `245 passed, 2 deselected` (`pytest -m "not integration"`) |

---

## Phase 5 — Versioning

- Software version **1.0.0** across `pyproject.toml`, `localgovbench/__init__.py` fallback, `CITATION.cff`, `.zenodo.json`, README, CHANGELOG.  
- `docs/releases/NEXT_RELEASE.md` retargeted to post-v1.0.0 with `NEXT_DOI_TBD` retained.  
- **No invented Zenodo version DOI** for v1.0.0 (minted on deposit).

---

## Phase 6–7 — Git / tag

| Item | Value |
|------|-------|
| Commit | `97eeeb46d64e277851eede90cff4b3751b46f33f` |
| Tag | `v1.0.0` (annotated) |
| Tag object | `5465aea56780985fadeaeecd0cea92a2a39aea24` |
| Tag message | Version 1.0.0 / First stable public release accompanying the submitted manuscript. |
| Remote | Pushed `main` and `v1.0.0` to `origin` (`cesar-andress/localgovbench`) |

---

## Reproducibility issues / remaining warnings

1. **Aggregate corpus CSV not in git** — `pilot_programme_records.csv` still local/ignored; verify with `scripts/verify_pilot_corpus.py`.  
2. **v1.0.0 Zenodo version DOI pending** — update `CITATION.cff` primary `doi:` after Zenodo publishes the deposit (follow-up commit OK).  
3. **Dual construct surface** — DF v1 is the “active” software narrative; manuscript empirics use the frozen public-satisfiability pilot. Both are present; README separates them. Do not conflate in citations.  
4. **CRLF warnings** on newly tracked CSVs — Git may normalize LF on commit; scientific values unchanged.  
5. **Large ignored local tree** — `.venv` (~211 MB) must never be uploaded.

---

## Confirmation

**Ready for Zenodo archival via GitHub tag `v1.0.0`:** YES, pending successful `git push` of commit + tag and Zenodo webhook/deposit.

Scientific content (mapping rules, freeze numbers, DF specs) was **not** modified or regenerated.
