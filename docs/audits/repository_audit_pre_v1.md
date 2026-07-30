# Repository audit — LocalGovBench

**Scope:** `/home/cesar/papers/localgovbench/localgovbench`  
**Audit date:** 2026-07-23  
**HEAD audited:** `fc640ca932342e3f36d75f01a8ac7101f63bf6aa` (`main`)  
**Annotated tag `v0.2.0` → commit:** `ff85e82`  
**Auditor role:** senior software engineer / RSE / reproducibility auditor / top-tier venue reviewer  
**Method:** read-only inspection of tree, metadata, CLIs, tests, docs, tags, and frozen affordance artefacts. **No code or methodological artefacts were modified as part of the audit investigation.** This file is the audit deliverable only.

**Framing assumption:** the Disclosure Functions v1 methodological framework is frozen; findings concern engineering hygiene, release integrity, documentation truthfulness, and third-party reproducibility — not redesign of the measurement construct.

---

## Executive verdict

This repository is **not yet fully publication-clean as a third-party-reproducible software artefact**, despite substantial strengths in the active Disclosure Functions (DF) v1 path.

**Overall readiness class:** *framework-transition software release with unfinished release-truth and reproducibility gaps* — closer to “usable by the authors” than “safe for unguided external reuse at the DOI tip.”

| Area | Assessment |
|------|------------|
| Active DF v1 specification + coding layer | Strong, internally consistent |
| Pilot launch package (Phase 4 ops) | Strong on `main`; **absent from tag `v0.2.0` / Zenodo tip** |
| Phase 3 experiment pipeline | Present on `main`; **absent from tag `v0.2.0`** |
| Citation badges / CITATION.cff DOIs | Largely aligned (active `21500899`, historical `20543779`) |
| Release documentation truthfulness | **Contradictory** (published vs not-yet) |
| Third-party corpus regeneration | **Broken** without external data acquisition |
| Legacy GRB surface | Retained and mostly labelled; still easy to misread as current |

**If everything looked good:** it does **not**. Explicit strengths are listed at the end; they do not cancel the CRITICAL items below.

---

## Architecture overview (as found)

```
localgovbench/                                 # repository root
├── localgovbench/                             # installable package (v0.1 GRB/framework/llm retained)
├── localgovbench_measurement_validation/
│   ├── affordance/                            # ACTIVE DF v1 (spec, coding, experiments, pilot_round_01)
│   └── pilot_public_satisfiability/           # corpus + earlier ceiling/shortfall pilot tooling
├── scripts/                                   # ~45 CLIs (GRB + Delphi + affordance)
├── tests/                                     # package + active-documentation claims
├── docs/ + docs/releases/                     # mostly LEGACY docs + v0.2 release pack
├── validation/, examples/, data/, reports/, results/, prompts/
├── paper_data_policy/                         # manuscript scaffold (mixed framing)
├── CITATION.cff, .zenodo.json, pyproject.toml, README.md
```

Two coexisting research systems share one GitHub/Zenodo product name:

1. **Historical:** Governance Readiness Benchmark (GRB) / v0.1.0  
2. **Active:** Disclosure Functions v1 schema affordance / coding / pipeline / pilot

That coexistence is intentional, but it remains the dominant external-reader risk.

---

## Findings

Severity key:

- **CRITICAL** — blocks trustworthy public release / third-party reproduction / citation integrity  
- **HIGH** — likely to cause incorrect use, failed onboarding, or reviewer rejection  
- **MEDIUM** — maintainability, drift, or secondary reproducibility issues  
- **LOW** — polish, naming, or minor hygiene  

Effort: **S** (<0.5 day), **M** (0.5–2 days), **L** (>2 days).

---

### CRITICAL

#### C1 — Tag / Zenodo `v0.2.0` does not contain Phase 3 or pilot launch artefacts

| Field | Detail |
|-------|--------|
| **Location** | Tag `v0.2.0` → `ff85e82`; missing at tag: `scripts/run_affordance_experiment_pipeline.py`, `.../affordance/experiments/EXPERIMENT_PIPELINE.md`, `.../coding/pilot_round_01/**`. Present on `HEAD` (`7d50b8b`…`fc640ca`). |
| **Problem** | Canonical DOI `10.5281/zenodo.21500899` and tag `v0.2.0` archive a tree **without** the experiment pipeline and pilot packets that current active docs describe. |
| **Why it matters** | External researchers citing the DOI cannot reproduce documented Phase 3 / pilot workflows. This is a classic “docs ahead of deposit” failure mode for Nature MI / ACM artefact evaluation. |
| **Recommended fix** | Either (a) mint **v0.2.1** (or later) from a frozen `main` that includes Phase 3 + pilot launch and update DOI/CITATION, or (b) demote Phase 3/pilot docs to “post-v0.2.0 / development tip only” until re-archived. Do **not** silently retag `v0.2.0` if Zenodo already bound that commit. |
| **Estimated effort** | M |
| **Risk if ignored** | Failed independent reproduction; DOI/doc mismatch; desk-reject risk for software/data claims. |

#### C2 — Canonical pilot corpus CSV not distributed with the repository

| Field | Detail |
|-------|--------|
| **Location** | `localgovbench_measurement_validation/pilot_public_satisfiability/data/pilot_programme_records.csv` (~27 MB, present locally); ignored by `.gitignore` `*.csv` (no allowlist exception). Declared canonical in `affordance/paths.py` and `affordance/README.md`. SHA locked in `affordance/locks/corpus_lock_v1.json` (`12ea6282…c8d693`, *n*=7434). Inventory outputs **are** tracked under `affordance/outputs/`. |
| **Problem** | Fresh clone cannot regenerate corpus lock / schema inventory from source records. Manifest already notes “may be gitignored” without a mandatory fetch path. |
| **Why it matters** | Scientific reproducibility of Phase 1 requires either the corpus bytes or a scripted, checksummed acquisition path. Frozen inventory alone is a *result artefact*, not a regenerative proof. |
| **Recommended fix** | Publish corpus (+ `source_registry_expanded.csv`) as Zenodo/Git-LFS assets **or** add `scripts/fetch_pilot_corpus.py` with official URLs + expected SHA-256; add `.gitignore` exception or document “data not in git by design” in root README with verification steps. |
| **Estimated effort** | M–L (license/size/hosting) |
| **Risk if ignored** | Non-reproducible specification regeneration; reviewers cannot verify lock provenance. |

#### C3 — Release documentation asserts mutually incompatible publication states

| Field | Detail |
|-------|--------|
| **Location** | `docs/releases/release_readiness_v0.2.0.md` (L4 “not performed”; L28 DOI Published; L84–92 “Not yet / no tag / no version DOI”); `docs/releases/public_positioning_v0.2.0.md` (Published); `docs/releases/zenodo_metadata_v0.2.0.md` (Status published **and** pre-publish minting instructions); `docs/releases/README.md` (“forthcoming”; “Do not create the Git tag”); `public_documentation_audit_v0.2.0.md` claims root `.zenodo.json` **Absent** while `.zenodo.json` **exists**. Treated as active surface by `tests/test_active_documentation_claims.py`. |
| **Problem** | Active release pack does not tell a single truth about whether v0.2.0 is published. |
| **Why it matters** | Citation and archival claims become non-auditable. Reviewers treat this as process failure. |
| **Recommended fix** | Freeze one authoritative status document; mark superseded audits; align readiness/README/positioning/Zenodo draft language; re-run claim tests against the unified truth. |
| **Estimated effort** | S–M |
| **Risk if ignored** | Trust collapse on all other metadata, even when DOIs resolve. |

#### C4 — Installable package `__version__` still reports `0.1.0`

| Field | Detail |
|-------|--------|
| **Location** | `localgovbench/__init__.py` (`__version__ = "0.1.0"`; docstring still “local AI governance”); vs `pyproject.toml` / `CITATION.cff` / `.zenodo.json` / dist metadata `0.2.0`. Also present on tag `v0.2.0`. Provenance pipeline reads version from `pyproject.toml` (mitigation only for that path). |
| **Problem** | `import localgovbench; localgovbench.__version__` lies. |
| **Why it matters** | Runtime version is what many users/loggers/citation helpers trust. |
| **Recommended fix** | Set `__version__ = "0.2.0"` or derive via `importlib.metadata.version("localgovbench")`; update package docstring to DF framing. |
| **Estimated effort** | S |
| **Risk if ignored** | Persistent mis-citation and support confusion. |

---

### HIGH

#### H1 — Broken link to pilot launch package from active affordance README

| Field | Detail |
|-------|--------|
| **Location** | `localgovbench_measurement_validation/affordance/README.md` → `[pilot_round_01/](pilot_round_01/README.md)` resolves to non-existent `affordance/pilot_round_01/`. Actual: `affordance/coding/pilot_round_01/README.md`. |
| **Problem** | Primary onboarding link for the human pilot is broken. |
| **Why it matters** | Pilot operators miss the launch package. |
| **Recommended fix** | Point to `coding/pilot_round_01/README.md`. |
| **Estimated effort** | S |
| **Risk if ignored** | Operational friction; looks careless in review. |

#### H2 — Absolute machine paths in frozen public artefacts

| Field | Detail |
|-------|--------|
| **Location** | `affordance/locks/corpus_lock_v1.json` field `absolute_path` = `/home/cesar/papers/...`; `coding/pilot_round_01/checksums/SHA256SUMS` mixes absolute `/home/cesar/...` paths with relative packet paths; `data/synthetic/municipality_corpus/metadata.json` `output_path` = `/home/cesar/papers/giq2026/localgovbench/...` (different project). |
| **Problem** | Environment leakage; `sha256sum -c` / path consumers fail off this machine (unless tools resolve abs paths that happen to exist). |
| **Why it matters** | Portability and privacy/hygiene for a public archive. |
| **Recommended fix** | Prefer repo-relative paths only in checksums and locks; drop or relativize `absolute_path`; scrub `giq2026` path. |
| **Estimated effort** | S |
| **Risk if ignored** | Failed checksum verification elsewhere; unprofessional provenance signals. |

#### H3 — Runtime dependency gap: PyYAML required but not declared

| Field | Detail |
|-------|--------|
| **Location** | `pyproject.toml` `dependencies = []`; `pyyaml` only under `[project.optional-dependencies] dev`. Active imports: `affordance/validate_specs.py`, `normalize.py`, coding/experiment modules, `localgovbench/utils/io.py`, GRB modules. Docs prescribe `pip install -e ".[dev]"`. |
| **Problem** | `pip install localgovbench` (no extras) cannot run the active DF path. |
| **Why it matters** | Packaging contract is false for the advertised research path. |
| **Recommended fix** | Move `pyyaml` (minimum) into core `dependencies`; keep pytest/matplotlib in `dev`. |
| **Estimated effort** | S |
| **Risk if ignored** | Immediate install/run failures for external users. |

#### H4 — Active repository validator does not guard the DF v1 surface

| Field | Detail |
|-------|--------|
| **Location** | `scripts/validate_repository.py` (`REQUIRED_PATHS` ~147 entries focused on v0.1/GRB/LLM/validation tree). Passes while affordance/pilot artefacts can be missing. |
| **Problem** | “Repository structure validation passed” does not mean the active framework is intact. |
| **Why it matters** | False confidence in CI/release checklists. |
| **Recommended fix** | Add required paths for DF configs, locks, coding templates, pilot packets, experiment docs, `docs/releases/public_positioning_v0.2.0.md`. |
| **Estimated effort** | M |
| **Risk if ignored** | Silent deletion/omission of core v0.2 artefacts. |

#### H5 — Framing conflicts outside LEGACY banners

| Field | Detail |
|-------|--------|
| **Location** | Root README: LocalGovBench **is** DF v1. `affordance/README.md`: “LocalGovBench is **not** the analytical framework of this paper path.” `localgovbench_measurement_validation/README.md`: “Paper 1 rescue… v0.1”. `pilot_public_satisfiability/` + `paper_data_policy/` retain shortfall/ceiling/v0.1 language without strong “not active framework” banners. |
| **Problem** | Competing definitions of “what this repo measures.” |
| **Why it matters** | Highest conceptual risk for FAccT/Nature MI readers skimming mid-tree docs. |
| **Recommended fix** | Unify phrasing (“software product LocalGovBench v0.2 hosts DF v1; GRB/shortfall paths are historical/precursor”); banner or relocate `paper_data_policy/` out of software deposit if manuscript-private. |
| **Estimated effort** | M |
| **Risk if ignored** | Mis-citation of readiness/shortfall as current results. |

#### H6 — Adjudication merge fields disagree with coder instructions

| Field | Detail |
|-------|--------|
| **Location** | `coder_instructions_v1.md` (confidence/rationale as metadata, must not change support). `experiments/adjudication_merge.py` `JUDGMENT_FIELDS` includes `coder_confidence` and `coder_rationale`, forcing adjudication on any difference. |
| **Problem** | Operational protocol vs pipeline semantics diverge. |
| **Why it matters** | Pilot admins following docs will hit unexpected pipeline hard-fails (especially with command C in `pilot_round_01_commands.md`). |
| **Recommended fix** | Either remove confidence/rationale from disagreement triggers **or** explicitly document that any confidence/rationale mismatch requires adjudication; make command C secondary to disagreement-export → adjudicate → F. |
| **Estimated effort** | S–M |
| **Risk if ignored** | Pilot pipeline stalls; inconsistent adjudication practice. |

#### H7 — No CI workflow in repository

| Field | Detail |
|-------|--------|
| **Location** | No `.github/workflows/` (or other CI config) tracked. |
| **Problem** | 200+ tests exist but are not gated on push/PR. |
| **Why it matters** | Public research software without CI is a reproducibility red flag. |
| **Recommended fix** | Add GitHub Actions: `pip install -e ".[dev]"`, `pytest -m "not integration"`, `validate_repository.py` (after H4). |
| **Estimated effort** | S–M |
| **Risk if ignored** | Regressions land unnoticed on `main`. |

#### H8 — CHANGELOG / release notes understate Phase 3 + pilot launch; still say “provisional”

| Field | Detail |
|-------|--------|
| **Location** | `CHANGELOG.md` L23 “Package version provisional **0.2.0**”; reproducibility section omits experiment pipeline / pilot launch. `docs/releases/README.md` “forthcoming”. |
| **Problem** | Release narrative lags `main` and contradicts DOI-published positioning elsewhere. |
| **Why it matters** | Changelog is a primary reviewer artefact. |
| **Recommended fix** | Update 0.2.0 notes or add 0.2.1 section covering Phase 3 + pilot launch; remove “provisional” if DOI is canonical. |
| **Estimated effort** | S |
| **Risk if ignored** | Version archaeology becomes unreliable. |

---

### MEDIUM

#### M1 — Duplicate IRR / sensitivity / readiness documentation and scripts

| Field | Detail |
|-------|--------|
| **Location** | Docs: `docs/inter_rater_reliability_protocol.md`, `validation/docs/inter_rater_guide.md`, `affordance/coding/config/irr_analysis_plan_v1.md`. Scripts: `run_inter_rater_analysis.py` vs `run_inter_rater_reliability.py`; `run_sensitivity_analysis.py` vs `run_grb_sensitivity_analysis.py` vs `analyze_sensitivity.py`; reports `sensitivity_analysis.md` + `grb_sensitivity_analysis.md`. |
| **Problem** | Near-duplicate names for distinct instruments (v0.1 dossier IRR vs GRB vs DF pilot plan). |
| **Why it matters** | Wrong script → wrong statistic → wrong paper claim. |
| **Recommended fix** | Index table in root or `docs/releases/`: script → instrument → allowed claims. |
| **Estimated effort** | M |
| **Risk if ignored** | Analytical mix-ups. |

#### M2 — Duplicated helper logic

| Field | Detail |
|-------|--------|
| **Location** | `classify_readiness_band` in `localgovbench/grb/scoring.py` and `localgovbench/validation/discriminant.py` (divergent); `git_commit_hash` in `corpus_lock.py` and `experiments/provenance.py`; repeated CSV/YAML loaders across pilot scripts. |
| **Problem** | Drift-prone duplication. |
| **Why it matters** | Silent inconsistency in legacy analyses. |
| **Recommended fix** | Consolidate utilities (even if legacy-only). |
| **Estimated effort** | M |
| **Risk if ignored** | Maintenance debt; hard-to-spot numeric drift. |

#### M3 — Additional broken relative Markdown links

| Field | Detail |
|-------|--------|
| **Location** | `data/synthetic/README.md` → `../docs/synthetic_municipality_corpus.md` (wrong depth); `data/synthetic/municipality_corpus/README.md` similar; `pilot_public_satisfiability/reports/validation_upgrade_report.md` figure links missing `../`. `coding/pilot_round_01/completed_inputs/README.md` references `../validation/dry_run_fixtures/` (absent). |
| **Problem** | Navigation fails. |
| **Why it matters** | Onboarding and audit trails. |
| **Recommended fix** | Correct relatives; remove or create dry-run fixture pointer. |
| **Estimated effort** | S |
| **Risk if ignored** | Minor but cumulative quality signal. |

#### M4 — Title variants (Affordance vs Affordances vs Affordance Framework)

| Field | Detail |
|-------|--------|
| **Location** | Zenodo/CITATION title uses “Disclosure **Affordances**…”; release prose uses “Disclosure **Affordance Framework**…”. Documented as intentional in `public_positioning_v0.2.0.md`, but easy to conflate in bibliographies. |
| **Problem** | Dual titles without a single “how to cite” hierarchy in every entrypoint. |
| **Why it matters** | Citation inconsistency across papers. |
| **Recommended fix** | Keep dual titles but put a one-line rule in README + CITATION message. |
| **Estimated effort** | S |
| **Risk if ignored** | Bibliographic noise. |

#### M5 — Software `0.2.0` vs specification/coding/pipeline `1.0.0` under-explained

| Field | Detail |
|-------|--------|
| **Location** | `affordance/__init__.py`, coding/experiments paths → `1.0.0`; package/release → `0.2.0`; runtime package still `0.1.0` (C4). |
| **Problem** | Three version planes; only partially documented. |
| **Why it matters** | Users report “wrong version” bugs that are conceptual. |
| **Recommended fix** | Root README subsection: Software × Specification × Coding layer versions. |
| **Estimated effort** | S |
| **Risk if ignored** | Support burden; review confusion. |

#### M6 — CLI documentation incompleteness

| Field | Detail |
|-------|--------|
| **Location** | `run_affordance_experiment_pipeline.py` supports `--output-root` (undocumented in `EXPERIMENT_PIPELINE.md`); `dry_run_pilot_round_01.py` supports `--keep` (undocumented in affordance README). |
| **Problem** | Hidden flags reduce usability. |
| **Why it matters** | Operators reinvent workarounds. |
| **Recommended fix** | Document flags; keep `--help` as source of truth. |
| **Estimated effort** | S |
| **Risk if ignored** | Low–moderate operational friction. |

#### M7 — `paper_data_policy/` tracked with PLACEHOLDER study DOI and v0.1 methods framing

| Field | Detail |
|-------|--------|
| **Location** | `paper_data_policy/04_methods.md` (v0.1 / 25-criteria framing; `10.5281/zenodo.PLACEHOLDER` for study deposit). |
| **Problem** | Manuscript scaffold co-shipped with software can be mistaken for finished methods. |
| **Why it matters** | Reviewers may quote PLACEHOLDER or v0.1 methods as software claims. |
| **Recommended fix** | Exclude from Zenodo software archive **or** banner “manuscript draft — not software API”. |
| **Estimated effort** | S |
| **Risk if ignored** | Mixed paper/software evaluation. |

#### M8 — No coverage tooling / coverage gates

| Field | Detail |
|-------|--------|
| **Location** | `pytest-cov` not installed; no coverage config. Affordance suite: 64 tests collected in affordance tree; whole repo ~232 collected (2 integration deselected). |
| **Problem** | Unknown untested branches in import/merge/validation. |
| **Why it matters** | RSE standard for research software releases. |
| **Recommended fix** | Add `pytest-cov` to `dev`; publish coverage for affordance + coding + experiments. |
| **Estimated effort** | M |
| **Risk if ignored** | Silent gaps in critical validators. |

#### M9 — Aggressive `*.csv` gitignore vs incomplete allowlist

| Field | Detail |
|-------|--------|
| **Location** | `.gitignore` ignores all `*.csv` with selective `!` exceptions (templates/adjudication/affordance config/pilot packets now allowed). Day-1 candidate CSV and pilot corpus still excluded. |
| **Problem** | Easy to omit scientifically necessary tables. |
| **Why it matters** | Couples to C2. |
| **Recommended fix** | Directory-scoped ignore policy (`data/raw/*.csv` ignore; research CSVs allow by folder). |
| **Estimated effort** | M |
| **Risk if ignored** | Recurring “missing data” releases. |

#### M10 — Legacy citation docs still deep-link live `CITATION.cff`

| Field | Detail |
|-------|--------|
| **Location** | `docs/citation.md`, `docs/zenodo_release.md`, `docs/reproducibility.md` (LEGACY banners + v0.1 DOI instructions) link to root `CITATION.cff` which is now v0.2.0 / `21500899`. |
| **Problem** | Banner says historical; link lands on current file. |
| **Why it matters** | Mixed citation instructions. |
| **Recommended fix** | Point legacy guides to tag `v0.1.0` tree / historical DOI only; “do not use root CITATION.cff for v0.1 reproduction.” |
| **Estimated effort** | S |
| **Risk if ignored** | Wrong DOI in secondary citations. |

#### M11 — Missing `codemeta.json` / incomplete root `.zenodo.json` DOI field

| Field | Detail |
|-------|--------|
| **Location** | No `codemeta.json`. Root `.zenodo.json` lacks top-level `doi` field (present in `docs/releases/zenodo_v0.2.0.draft.json`). |
| **Problem** | Indexer/metadata consumers uneven. |
| **Why it matters** | Discoverability and deposit automation. |
| **Recommended fix** | Generate Codemeta from CFF; align `.zenodo.json` with published deposit. |
| **Estimated effort** | S |
| **Risk if ignored** | Minor metadata incompleteness. |

#### M12 — Large legacy result artefacts in tree

| Field | Detail |
|-------|--------|
| **Location** | e.g. `results/grb_monte_carlo.csv` (~1 MB+) and GRB reports under `reports/`. |
| **Problem** | Inflates software archive; foregrounds legacy outputs. |
| **Why it matters** | Zenodo “what is this product?” confusion. |
| **Recommended fix** | Keep for provenance but exclude from slim Zenodo software upload if deposit is DF-focused. |
| **Estimated effort** | S |
| **Risk if ignored** | Diluted release narrative. |

#### M13 — Python launcher inconsistency (`python` / `python3` / `python3.12`)

| Field | Detail |
|-------|--------|
| **Location** | Active docs prefer `python3.12`; legacy docs/scripts often `python`/`python3`. Host `python3` may be far older than 3.11. |
| **Problem** | Onboarding fails with SyntaxError before science starts. |
| **Why it matters** | First-run experience. |
| **Recommended fix** | Standardize on `python3.12` or document `requires-python` enforcement via tox/nox. |
| **Estimated effort** | S |
| **Risk if ignored** | Support noise. |

#### M14 — No console script entry points

| Field | Detail |
|-------|--------|
| **Location** | `pyproject.toml` has no `[project.scripts]`; all UX is `python scripts/...`. |
| **Problem** | Package install does not expose CLIs on PATH. |
| **Why it matters** | Usability for non-repo-cwd workflows. |
| **Recommended fix** | Add entry points for build/validate/pipeline commands. |
| **Estimated effort** | M |
| **Risk if ignored** | Moderate usability gap (scripts still work in-repo). |

---

### LOW

#### L1 — Nested `localgovbench/localgovbench/` naming

| Field | Detail |
|-------|--------|
| **Location** | Repository directory and Python package share the name. |
| **Problem** | Path ambiguity in prose (“cd localgovbench”). |
| **Why it matters** | Minor onboarding confusion. |
| **Recommended fix** | Clarify “repo root vs package dir” in README. |
| **Estimated effort** | S |
| **Risk if ignored** | Low. |

#### L2 — `pilot_launch_readiness_*` naming collisions with GRB “readiness”

| Field | Detail |
|-------|--------|
| **Location** | `coding/pilot_round_01/validation/pilot_launch_readiness_v1.md`. |
| **Problem** | Word “readiness” reserved in this project’s political economy for GRB. |
| **Why it matters** | Search/skimming hazard. |
| **Recommended fix** | Rename to `pilot_launch_checklist_v1.md` (optional). |
| **Estimated effort** | S |
| **Risk if ignored** | Low. |

#### L3 — TODO/FIXME/DEBUG surface is mostly clean

| Field | Detail |
|-------|--------|
| **Location** | Repo-wide search: no meaningful `FIXME`/`DEBUG` backlog; `XXX` mostly template placeholders (`run_XXX.json`, `exp_XXX`, validator check for `zenodo.XXXXXXX`). |
| **Problem** | None material. |
| **Why it matters** | Positive signal. |
| **Recommended fix** | None required. |
| **Estimated effort** | — |
| **Risk if ignored** | — |

#### L4 — Backup/copy/`*.bak` hygiene

| Field | Detail |
|-------|--------|
| **Location** | No tracked `.bak` / `*copy*` / editor junk found. Caches (`.venv`, `.pytest_cache`, `egg-info`) gitignored. |
| **Problem** | None. |
| **Why it matters** | Good git hygiene. |
| **Recommended fix** | Keep as-is. |
| **Estimated effort** | — |
| **Risk if ignored** | — |

#### L5 — Dual DOI badges may still be skim-misread

| Field | Detail |
|-------|--------|
| **Location** | Root README badges for `21500899` and historical `20543779`. |
| **Problem** | Despite labels, badge pairs are often clicked indiscriminately. |
| **Why it matters** | Residual mis-citation. |
| **Recommended fix** | Keep labels; optionally shrink historical badge / move to footnote. |
| **Estimated effort** | S |
| **Risk if ignored** | Low–moderate. |

#### L6 — Concept DOI still USER CONFIRMATION

| Field | Detail |
|-------|--------|
| **Location** | `docs/releases/zenodo_metadata_v0.2.0.md`, `release_readiness_v0.2.0.md`. |
| **Problem** | Unverified concept DOI (correctly not invented). |
| **Why it matters** | Incomplete citation graph for “all versions.” |
| **Recommended fix** | Confirm with Zenodo UI and record or explicitly mark N/A. |
| **Estimated effort** | S |
| **Risk if ignored** | Low. |

#### L7 — LICENSE copyright line is generic

| Field | Detail |
|-------|--------|
| **Location** | `LICENSE`: “Copyright (c) 2026 LocalGovBench contributors” vs named author in CITATION.cff. |
| **Problem** | Mild inconsistency, legally usually fine for MIT. |
| **Why it matters** | Cosmetic. |
| **Recommended fix** | Align if institutional policy requires named copyright holder. |
| **Estimated effort** | S |
| **Risk if ignored** | Low. |

---

## Cross-cutting consistency matrices

### Version planes

| Plane | Declared value | Source of truth today | Consistency |
|-------|----------------|-----------------------|-------------|
| Software release | `0.2.0` | `pyproject.toml`, `CITATION.cff`, `.zenodo.json`, README | OK among metadata files |
| Runtime import | `0.1.0` | `localgovbench/__init__.py` | **FAIL (C4)** |
| DF specification / coding / pipeline | `1.0.0` | affordance package inits + YAML/schemas | Internally OK; under-documented vs software (M5) |
| Git tag archive | `v0.2.0` @ `ff85e82` | Tag | **Behind `main` (C1)** |

### DOI planes

| DOI | Role | Consistency |
|-----|------|-------------|
| `10.5281/zenodo.21500899` | Active v0.2.0 | Present in README/CFF/CHANGELOG/badges |
| `10.5281/zenodo.20543779` | Historical v0.1.0 | Preserved; related_identifiers `isNewVersionOf` in `.zenodo.json` |
| Concept DOI | Unconfirmed | Correctly flagged, not invented |
| Study replication | `zenodo.PLACEHOLDER` in `paper_data_policy` | Must not be confused with software DOI (M7) |

### Affordance scientific surface (spot checks)

| Check | Result |
|-------|--------|
| Corpus lock *n* | 7434 |
| Full coding template units | 55 (5 sources × 11 functions) |
| Pilot units | 33 |
| Blank packets A/B | 33 rows each; judgment fields empty (launch package) |
| Phase 3 realizes realization/gap/IRR? | No (placeholders / forbidden) — consistent with freeze |
| Spec identifiers | Validated by affordance tests (64 passed in affordance tree at audit time) |

---

## Dead code / unused artefacts

**No large orphan Python modules** were identified as never-imported within the active packages (heuristic + script/doc references).

What *is* “dead as a current scientific claim” (but intentionally retained):

- `localgovbench/grb/`, `localgovbench/framework/`, most top-level `validation/`, GRB `scripts/run_grb_*`, GRB `reports/` / `results/`  
- Delphi response YAMLs correctly gitignored; templates tracked  

**Unused relative to active claims but still shipped:** multiple sensitivity/IRR script aliases (M1). Not safe to delete without a deprecation map.

**Temporary/debug code:** dry-run fixture path is properly isolated (`NON_SUBSTANTIVE_TEST_FIXTURE`); no study-result contamination found in `completed_inputs/` (placeholder README only).

---

## Test / validation / logging / error handling (summary)

| Topic | Assessment |
|-------|------------|
| Affordance unit tests | Solid for Phase 1–3 + pilot launch |
| Integration tests | Correctly deselected by default |
| Logging | Minimal structured logging; mostly print/`raise` — acceptable for research CLIs, thin for operators |
| Error handling | Coding import / matrix validation raise explicit errors; adjudication-missing path is strict (see H6) |
| Coverage gates | Absent (M8) |
| CI | Absent (H7) |

---

## Strengths (explicitly good)

1. **Clear public non-claims** in root README / CITATION.cff (no rankings, readiness, shortfall, compliance composites as active outputs).  
2. **DF v1 layer is well-factored**: frozen config, corpus lock, schema inventory, coding schema, codebook, pilot packets, experiment pipeline, provenance hooks.  
3. **Active-documentation claim tests** reduce framing regressions.  
4. **LEGACY banners** on most v0.1 docs and validation package entrypoints.  
5. **Pilot scientific boundary** respected in launch package (blank judgments; no synthetic completed sheets in intake).  
6. **Citation dual-DOI design** (active vs historical) is conceptually correct when docs agree.  
7. **Git hygiene for secrets/caches** is good; Delphi responses excluded.  
8. **Almost no TODO/FIXME debt** or backup junk.  
9. **Keep-a-Changelog**, MIT LICENSE, CONTRIBUTING, CODE_OF_CONDUCT present.  
10. **Internal numeric consistency** of 55/33/7434 on the audited working tree.

---

## Priority remediation sequence (no changes made here)

1. **C1 + C3 + H8** — single release truth; archive contents match docs (likely `v0.2.1`).  
2. **C2 + M9 + H2** — corpus distribution + portable checksums/paths.  
3. **C4 + H3 + H7 + H4** — version, deps, CI, validator coverage of DF surface.  
4. **H1 + H5 + H6 + M1** — links, framing, adjudication semantics, script map.  
5. Polish: M3–M8, M10–M14, LOW items.

---

## Final statement

**Everything does not look good.** The active Disclosure Functions engineering path is substantially stronger than a typical mid-transition research repo, but **CRITICAL release-integrity and corpus-reproducibility defects** remain. Until C1–C4 are resolved, the repository should be described publicly as a **framework-transition codebase with incomplete third-party regenerative guarantees**, not as a fully archival, tip-aligned reproducible experiment stack.

**Audit status:** complete (read-only).  
**Code/methodology modifications:** none (other than creation of this audit deliverable).
