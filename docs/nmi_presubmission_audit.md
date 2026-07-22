# Nature Machine Intelligence — pre-submission repository audit

**Audit date:** 2026-07-23  
**Repository tip audited:** `2174f85` (`main`)  
**Cited software tag:** `v0.2.0` → `ff85e82`  
**Canonical active DOI:** `10.5281/zenodo.21500899`  
**Historical DOI:** `10.5281/zenodo.20543779`  
**Scope:** software engineering, reproducibility, documentation, structure, scientific methodology, metadata/citations, release management, validation, experiments, paper consistency  
**Constraint:** fixes are **proposed only** — none applied in this audit pass  

**Assumed NMI submission model:** research paper + peer-reviewable code/data artefact. NMI expects tip-aligned archives, third-party reproducibility, and claims that do not exceed deposited evidence.

---

## Executive verdict

| Question | Answer |
|----------|--------|
| Is the repository **submission-ready for NMI** as support for **completed empirical Disclosure Functions results**? | **No** |
| Is it closer to ready as an **instrument / methods / research-software** companion with tightly scoped claims? | **Not yet** — blocked by Critical items below |
| Overall readiness class | **Not submission-ready** |

**One-line judgment:** Strong DF v1 instrument engineering on `main`, undermined by DOI/tag drift, missing public corpus distribution, release-metadata contradictions, dual-construct contamination risk, and absence of empirical coding Results in the deposit.

---

## What is in scope as “current evidence”

Present on `main` (`2174f85`):

- Disclosure Functions v1 specification + corpus lock + schema inventory  
- Human coding system (55-unit template, 33-unit pilot, blank packets)  
- Phase 3 experiment pipeline + tests (64 affordance-tree tests passing at audit)  
- Supplements A–J, `paper_assets/` Methods scaffolds, prior `repository_audit.md`  

**Not present as study Results:** completed dual coding, IRR coefficients, adjudicated affordance matrix as findings, realization rates, affordance–realization gaps.

**Tag `v0.2.0` / Zenodo tip:** does **not** include Phase 3 CLI or pilot launch package.

---

## Critical issues

### C1 — Cited archive tip ≠ documented experimental/pilot capability

| | |
|--|--|
| **Evidence** | `v0.2.0` @ `ff85e82` lacks `scripts/run_affordance_experiment_pipeline.py` and `coding/pilot_round_01/`; both exist on `main` after `7d50b8b` / pilot commits |
| **Why it matters (NMI)** | Reviewers reproduce from DOI/tag. Docs on `main` describe workflows absent from the citeable tip → failed artefact evaluation |
| **Proposed fix** | Mint **v0.2.1** (or later) from a frozen `main` including Phase 3 + pilot + supplements + `paper_assets`, update CITATION/Zenodo/README; **or** demote all Phase 3/pilot docs to “post-v0.2.0 development only” until re-archived. Do not silently move `v0.2.0` if Zenodo already bound |

### C2 — Canonical corpus not third-party obtainable from git

| | |
|--|--|
| **Evidence** | `pilot_programme_records.csv` (~27 MB) present locally but **gitignored** (`*.csv`); lock SHA `12ea6282…c8d693`, *n*=7434 |
| **Why it matters** | NMI reproducibility requires regenerative or deposited data. Frozen inventory alone is not a substitute for corpus bytes + verification |
| **Proposed fix** | Zenodo/Git-LFS data deposit **or** `scripts/fetch_pilot_corpus.py` with official URLs + SHA check; document in root README + Supplement A; add `.gitignore` exception or explicit “data-not-in-git” policy with mandatory fetch |

### C3 — Release documentation asserts incompatible publication states

| | |
|--|--|
| **Evidence** | `docs/releases/release_readiness_v0.2.0.md` mixes DOI **Published** with **Not yet / no tag / no version DOI**; `docs/releases/README.md` still “forthcoming”; positioning docs say Published |
| **Why it matters** | Metadata untrustworthy; NMI editors treat this as process failure |
| **Proposed fix** | Single authoritative status document; mark superseded drafts; re-run active-documentation claim tests against unified truth |

### C4 — Runtime package version contradicts release metadata

| | |
|--|--|
| **Evidence** | `localgovbench.__version__ == "0.1.0"` vs `pyproject.toml` / `CITATION.cff` / `.zenodo.json` = `0.2.0` |
| **Why it matters** | Import-time identity used by users/logs/citation helpers lies |
| **Proposed fix** | Align `__version__` or `importlib.metadata.version("localgovbench")`; update package docstring to DF framing |

### C5 — Paper–repository claim risk (Results absent)

| | |
|--|--|
| **Evidence** | `paper_assets` T09–T13 / F05–F08 are empty placeholders; no completed coding sheets in deposit; pilot packets intentionally blank |
| **Why it matters** | NMI will reject overclaiming. Repo cannot support measured affordance/IRR/realization/gap findings |
| **Proposed fix** | Scope paper as **instrument + protocol + infrastructure** until coding Results are deposited at a new version; keep placeholders labelled non-Results; never fill with synthetic judgments |

---

## High issues

### H1 — Dual-construct contamination (GRB / shortfall vs DF)

| | |
|--|--|
| **Evidence** | Active DF path coexists with `localgovbench/grb/`, shortfall outputs/figures under `pilot_public_satisfiability/`, legacy docs, `paper_data_policy` v0.1 framing |
| **Why it matters** | Reviewers/policy readers may cite wrong construct as “LocalGovBench results” |
| **Proposed fix** | Stronger banners at every results-looking directory; Zenodo “software-only / DF-focused” file set; rename or quarantine shortfall figures from default browse path; clarify precursor role of public-satisfiability pilot |

### H2 — No CI

| | |
|--|--|
| **Evidence** | No `.github/workflows` |
| **Why it matters** | NMI artefact review expects automated tests on the cited tip |
| **Proposed fix** | GHA: `pip install -e ".[dev]"`, affordance/coding/experiments pytest, `validate_repository.py` (after H4) |

### H3 — Runtime dependency gap (PyYAML)

| | |
|--|--|
| **Evidence** | `dependencies = []`; PyYAML only in `[dev]`; active path imports `yaml` |
| **Proposed fix** | Move `pyyaml` to core dependencies |

### H4 — Structure validator ignores DF surface

| | |
|--|--|
| **Evidence** | `scripts/validate_repository.py` ~147 legacy-oriented required paths; passes without DF pilot/pipeline |
| **Proposed fix** | Require locks, DF configs, coding templates, pilot packets, `docs/releases/public_positioning_v0.2.0.md`, supplements index |

### H5 — Absolute machine paths in frozen artefacts

| | |
|--|--|
| **Evidence** | `corpus_lock_v1.json` `absolute_path`; pilot `SHA256SUMS` mixes `/home/cesar/...` |
| **Proposed fix** | Repo-relative paths only; drop or ignore `absolute_path` in public deposit |

### H6 — Broken onboarding link to pilot package

| | |
|--|--|
| **Evidence** | `affordance/README.md` links `pilot_round_01/README.md` (missing `coding/`) |
| **Proposed fix** | `coding/pilot_round_01/README.md` |

### H7 — Adjudication semantics vs coder instructions

| | |
|--|--|
| **Evidence** | Merge `JUDGMENT_FIELDS` includes `coder_confidence` / `coder_rationale`; instructions treat them as non-decisive metadata |
| **Proposed fix** | Align code with codebook **or** document that any confidence/rationale mismatch forces adjudication; fix pilot command ordering docs |

### H8 — CHANGELOG / release notes lag and still say “provisional”

| | |
|--|--|
| **Evidence** | CHANGELOG “provisional 0.2.0”; understates Phase 3 + pilot + supplements + `paper_assets` |
| **Proposed fix** | Add 0.2.1 section or expand 0.2.0 honestly; remove provisional if DOI is canonical |

---

## Medium issues

| ID | Issue | Proposed fix |
|----|-------|--------------|
| M1 | Software `0.2.0` vs spec/coding/pipeline `1.0.0` under-explained | Root README version-plane subsection |
| M2 | Title variants (Affordances vs Affordance Framework) | One-line cite rule in README + CITATION message |
| M3 | CLI flags undocumented (`--output-root`, dry-run `--keep`) | Document in EXPERIMENT_PIPELINE / affordance README |
| M4 | Legacy citation docs deep-link live `CITATION.cff` | Point to tag `v0.1.0` / historical DOI only |
| M5 | No `codemeta.json`; root `.zenodo.json` lacks top-level `doi` field | Generate Codemeta; align Zenodo JSON with deposit |
| M6 | Concept DOI unconfirmed | Confirm in Zenodo UI or mark N/A |
| M7 | Aggressive `*.csv` gitignore vs incomplete allowlist | Directory-scoped policy; allow research CSVs intentionally |
| M8 | Duplicate IRR/sensitivity script names (legacy) | Index table: script → instrument → allowed claims |
| M9 | Broken relative Markdown links (synthetic READMEs, some figures) | Fix paths |
| M10 | No coverage gates | `pytest-cov` on affordance/coding/experiments |
| M11 | No console entry points | `[project.scripts]` for build/validate/pipeline |
| M12 | `paper_data_policy` PLACEHOLDER study DOI co-shipped | Exclude from Zenodo software set or banner “manuscript draft” |
| M13 | Large GRB result CSVs inflate archive | Slim DF-focused Zenodo upload |
| M14 | Python launcher inconsistency (`python` vs `python3.12`) | Standardize docs on 3.12 / enforce `requires-python` |

---

## Low issues

| ID | Issue | Proposed fix |
|----|-------|--------------|
| L1 | Nested `localgovbench/localgovbench` naming | Clarify repo root vs package in README |
| L2 | Pilot “readiness” filenames collide with GRB vocabulary | Rename to checklist/status |
| L3 | Dual DOI badges skim-misread risk | Shrink historical badge / footnote |
| L4 | LICENSE “contributors” vs named CFF author | Align if required by institution |
| L5 | TODO/FIXME surface clean; good cache hygiene | Maintain |
| L6 | Prior audits (`repository_audit.md`) already flag many items | Treat this NMI audit as submission gate; close Criticals first |

---

## Dimension assessments (NMI lens)

### Software engineering

**Grade: B− (DF core) / D (release engineering).** Modular affordance package, validators, tests (64 passed). Missing CI, version skew, dependency declaration gap, absolute paths.

### Reproducibility

**Grade: D+ regenerative / B− protocol.** Protocols, templates, tests, checksums exist. Corpus not distributed; DOI tip incomplete; Results placeholders empty by design.

### Documentation

**Grade: B positioning / D release consistency.** Excellent non-claims at root; supplements and `paper_assets` help Methods. Contradictory release pack and legacy bleed hurt NMI trust.

### Repository structure

**Grade: C.** Intentional dual stack is documented but hazardous. Active path under `affordance/` is clear; legacy GRB/shortfall still too discoverable as “results.”

### Scientific methodology

**Grade: A− design / N/A evaluation.** Schema×function unit, anti-over-credit, affordance≠realization, double-coding/adjudication plans are strong. **No completed human evaluation in deposit** → cannot claim measured affordance.

### Metadata and citations

**Grade: B−.** Dual DOI design correct in CFF/README when consistent; undermined by `__version__`, provisional language, release contradictions, concept DOI TBD.

### Release management

**Grade: D.** Tag behind `main`; docs disagree on publish state; CHANGELOG incomplete relative to tip.

### Validation

**Grade: B for DF unit tests; C for repo-wide gates.** Pilot pre/post validators good; structure validator legacy-centric; no CI.

### Experiments

**Grade: B infrastructure / F results.** Phase 3 pipeline appropriate and tested; forbids realization/IRR calculation (correct for stage). Not in `v0.2.0` tip. No real experiment outputs as findings.

### Paper consistency

**Grade: C−.** Supplements/`paper_assets` align with DF Methods if paper stays instrument-scoped. High risk if manuscript imports shortfall claims or invents Results. Companion paper DOI unset (acceptable if stated). Private `paper/` tree is separate—ensure submitted PDF claims ⊆ cited software tip.

---

## Prioritized remediation roadmap (do not implement in this pass)

### Gate 0 — decide submission type (1 day)

1. **Type A:** Instrument / research-software / protocol paper → still must clear C1–C4.  
2. **Type B:** Empirical DF results paper → also need completed coding+IRR (+ realization if claimed) in a new DOI. **Not ready now.**

### Gate 1 — Critical (before any NMI upload)

1. C1 archive alignment  
2. C2 corpus distribution  
3. C3 release truth  
4. C4 `__version__`  
5. C5 claim freeze matching deposit  

### Gate 2 — High (before review)

H1–H8 (misuse barriers, CI, deps, validator, paths, pilot link, adjudication, changelog)

### Gate 3 — Medium/Low

Polish for camera-ready artefact evaluation.

### Verification script (post-fix, clean room)

```text
clone cited tag/DOI tip → install → fetch/verify corpus SHA →
build_affordance_specification --validate-only →
pytest affordance/coding/experiments →
regenerate paper_assets F01–F04 →
confirm blank pilot judgments →
confirm paper claims ⊆ deposit
```

---

## Explicit non-fixes (do not “solve” by fabrication)

- Do not invent coder judgments, IRR, realization rates, or gaps to appear Results-ready.  
- Do not treat `NON_SUBSTANTIVE_TEST_FIXTURE` dry-runs as study data.  
- Do not relabel shortfall/GRB outputs as Disclosure Functions Results.

---

## Final submission-readiness statement

**The repository is not submission-ready for Nature Machine Intelligence** under either:

1. **Empirical results** framing — missing coded Results and tip-complete evaluation artefacts; or  
2. **Instrument/software** framing — still blocked by **Critical** release integrity and corpus reproducibility defects (C1–C4), plus high misuse risk from the legacy surface (H1).

**Conditional path to readiness (instrument paper):** clear all Criticals + H1–H4, freeze claims to protocols/instruments only, deposit a tip-aligned version DOI, pass clean-room reproduction.  
**Conditional path to readiness (empirical paper):** above, plus completed dual coding, adjudication, IRR, and any claimed realization/gap analyses deposited and cited.

**Audited tip:** `2174f85`  
**Fixes applied in this pass:** none  
