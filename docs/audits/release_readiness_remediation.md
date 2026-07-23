# Release-readiness remediation matrix

**Date:** 2026-07-23  
**Tip remediated:** post-remediation `main`  
**Sources:** `repository_audit.md`, `docs/nmi_presubmission_audit.md`

## CRITICAL

| Finding | Original | Action | Files | Tests | Status |
|---------|----------|--------|-------|-------|--------|
| Tag/DOI v0.2.0 lacks Phase 3 / pilot | CRITICAL | Document tip vs published; prepare 0.2.1 candidate; do **not** retag or invent DOI | `docs/releases/NEXT_RELEASE.md`, `docs/releases/README.md`, `docs/releases/release_readiness_v0.2.0.md`, root `README.md`, `CHANGELOG.md` | `test_version_consistency`, active doc tests | **MITIGATED** (publication still **BLOCKED — HUMAN DECISION**) |
| Corpus CSV not in clean clone | CRITICAL | Acquisition/verification docs + verify script; no fake data; no licensing invention | `docs/reproducibility/corpus_acquisition.md`, `scripts/verify_pilot_corpus.py` | lock-only CI step; clean-room warn path | **BLOCKED — EXTERNAL DATA** / **BLOCKED — HUMAN DECISION** (redistribution) |
| Release docs Published vs Not yet | CRITICAL | Reconcile: v0.2.0 published; main unreleased 0.2.1 | release docs above | `test_release_docs_distinguish_published_and_unreleased` | **RESOLVED** |
| `__version__` 0.1.0 vs metadata | CRITICAL | Runtime from package metadata; tip `0.2.1`; CFF stays published `0.2.0` | `localgovbench/__init__.py`, `pyproject.toml` | `test_version_consistency` | **RESOLVED** (tip); published citation unchanged |
| Paper Results overclaim risk | CRITICAL | No Results fabricated; placeholders remain empty; tip notice in README | README, paper_assets unchanged scientifically | legacy/active claim tests | **MITIGATED** (claim discipline; empirical Results still absent) |

## HIGH

| Finding | Original | Action | Files | Tests | Status |
|---------|----------|--------|-------|-------|--------|
| Dual GRB/shortfall misuse | HIGH | Notices on reports/results/pilot_satisfiability/data/prompts | READMEs | `test_legacy_notices` | **RESOLVED** (mitigation; artefacts retained) |
| No CI | HIGH | GitHub Actions workflow | `.github/workflows/ci.yml` | workflow runs suites | **RESOLVED** |
| PyYAML only in `[dev]` | HIGH | Runtime dependency | `pyproject.toml` | install/import in CI | **RESOLVED** |
| `validate_repository` ignores DF | HIGH | DF path set + version/notice checks | `scripts/validate_repository.py` | CI + clean-room | **RESOLVED** |
| Absolute paths in lock/SUMS | HIGH | Keep historical `absolute_path`; add `portable_path`; relative SHA256SUMS | lock JSON; `pilot_launch.write_sha256sums` | validate_repository | **MITIGATED** |
| Broken pilot README link | HIGH | Fix to `coding/pilot_round_01/` | `affordance/README.md` | validate_repository | **RESOLVED** |
| Confidence/rationale force adjudication | HIGH | Align merge with protocols | `adjudication_merge.py`, `validate.export_disagreements` | `test_merge_confidence_only_diff_does_not_require_adjudication` | **RESOLVED** |
| CHANGELOG provisional / lag | HIGH | Unreleased 0.2.1 section; remove provisional wording for 0.2.0 | `CHANGELOG.md` | — | **RESOLVED** |
| Synthetic metadata absolute path | HIGH | Portable path + historical absolute preserved | `data/synthetic/.../metadata.json` | — | **RESOLVED** |
| Import commands `~/papers/...` | HIGH/MED | Portable clone path wording | `pilot_round_01_commands.md` | — | **RESOLVED** |

## Remaining blocked (not fully closed)

1. **Minting / tagging 0.2.1** — human.  
2. **Corpus redistribution** — human + licensing.  
3. **DOI tip ≡ Phase 3/pilot** — requires published 0.2.1 (or later).  

## Remaining risk

Users citing only Zenodo v0.2.0 still lack Phase 3/pilot until the next deposit. Readers who ignore LEGACY notices may still misuse GRB outputs.
