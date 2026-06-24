# Next steps to draft — Paper 1 (Data & Policy)

## Drafting order (sections)

| Step | Section | Rationale |
|------|---------|-----------|
| 1 | **Methods (§4)** | Frozen pipeline; easiest to write from scripts + `results_freeze.md` |
| 2 | **Results (§5)** | Insert T1→T5 and F2→F5 directly from outputs |
| 3 | **Tables & figures** | Finalise T1–T5 and F1–F5 while Results fresh |
| 4 | **Introduction (§1)** | Write once headline numbers are fixed in Results |
| 5 | **Background (§2)** | Policy context; minimal citation load |
| 6 | **Instrument slice (§3)** | Trim from `localgovbench_criteria_v0.yaml` + T2 |
| 7 | **Discussion (§6)** | Interpret frozen results; policy implications |
| 8 | **Limitations (§7)** | Pull from `writing_risks.md` |
| 9 | **Conclusion (§8)** | Short; repeat non-claims |
| 10 | **Abstract** | Last — from `title_abstract_keywords.md` template |
| 11 | **Data availability** | Zenodo/OSF text |

**Do not start with Introduction** — risk of drift before numbers are locked.

---

## Tables / figures to finalise first

### Priority 1 (core argument)
1. **F2** — evidence shortfall gradient (exists; label polish)
2. **T3** — shortfall matrix (export from CSV)
3. **T4** — sensitivity + commensurability panels

### Priority 2 (robustness)
4. **F3** — sensitivity bars (exists)
5. **T5** — detector + partition reliability

### Priority 3 (context + policy)
6. **T1** — corpus composition
7. **T2** — 25 requirements + partition
8. **F5** — minimum internal evidence set (exists)
9. **F4** — cross-jurisdiction ceiling (exists)
10. **F1** — **new** partition map script (see `figure_plan.md`)

### Export command
```bash
cd localgovbench
python3.12 scripts/run_validation_upgrade.py
python3.12 scripts/evaluate_detector_reliability.py
python3.12 scripts/analyze_unit_commensurability.py
```

---

## Old LocalGovBench text — REUSE

| Source | Reuse for |
|--------|-----------|
| `localgovbench/framework/dimensions.py` | Dimension names, criterion statements |
| `config/localgovbench_criteria_v0.yaml` | T2, §3 instrument slice |
| `docs/ai_act_mapping.md`, `docs/gdpr_mapping.md` | Background only (non-legal framing) |
| `validation/content_validity/scoring_rubric.md` | Evidence gate ≥3 definition (Methods) |
| `reports/corpus_verification_day1.md` | Methods source verification paragraph |
| `localgovbench_measurement_validation/pilot_public_satisfiability/reports/*.md` | Results paragraph drafts |
| `paper_data_policy/results_freeze.md` | All numeric claims |

---

## Old LocalGovBench text — DELETE or avoid

| Source | Reason |
|--------|--------|
| `docs/manuscript_positioning.md` GIQ-first readiness framing | Wrong venue and claim |
| Readiness index / maturity score language anywhere | Forbidden claim |
| `scripts/run_grb_assessment.py` outputs | Not part of Paper 1 package |
| Municipal ranking / league table examples | Hard exclusion |
| “Observability,” “disclosure,” “documentary” framing | Paper 2 / old pilot |
| DAA constructs | Paper 2 firewall |
| `paper/data/open_pilot/` corpus references | Paper 2 firewall |
| “Validates LocalGovBench as benchmark” | Overclaim |
| GIQ reviewer objection table verbatim | Replace with `writing_risks.md` |

---

## Zenodo / OSF deposit package

### Recommended deposit structure

```
localgovbench-paper1-public-evidence-ceiling-v1/
  README.md                    # One-command reproduction
  CITATION.cff                 # Update with Paper 1 title + authors
  corpus/
    source_registry_expanded.csv
    pilot_programme_records.csv   # OR download scripts only if size limit
  config/
    localgovbench_criteria_v0.yaml
  mapping/
    mapping_rules.py
  outputs/                     # All frozen CSVs from results_freeze.md
  figures/                     # F1–F5 PNG 300 dpi
  scripts/
    run_validation_upgrade.py
    evaluate_detector_reliability.py
    analyze_unit_commensurability.py
    build_pilot_corpus.py
    ...
  reports/
    validation_upgrade_report.md
    unit_commensurability_report.md
    detector_reliability_report.md
```

### Zenodo metadata
- **Resource type:** Dataset + Software
- **Title:** Public-evidence ceiling corpus and pipeline — LocalGovBench Paper 1
- **Related identifier:** LocalGovBench instrument Zenodo DOI (v0.1.2) as **IsSupplementTo** or **IsPartOf**
- **License:** Match repository (check existing Zenodo record)

### OSF (optional)
- Preprint + frozen snapshot + preregistration-style methods summary
- Link Zenodo DOI in Data & Policy data availability statement

### Data availability statement (draft sentence)
> “All code, frozen summary outputs, and figure reproduction scripts are archived at Zenodo [DOI]. Primary source inventories remain at official URLs listed in Table 1; normalised corpus included in deposit.”

---

## Pre-submission checklist

- [ ] Abstract includes all four required non-claim elements
- [ ] No instance of “readiness score,” “rank,” “observability,” “maturity” in main text
- [ ] T4 and T5 in manuscript match `results_freeze.md` exactly
- [ ] Paper 2 firewall paragraph in Methods
- [ ] Internal evidence floor figure (F5) in Discussion
- [ ] Data & Policy author guidelines: word limit, abstract structure, data statement
- [ ] Co-author sign-off on `claims_and_nonclaims.md`

---

## Timeline suggestion (4 weeks to first draft)

| Week | Deliverable |
|------|-------------|
| 1 | Methods + Tables T1–T3 + F2 |
| 2 | Results + T4–T5 + F3–F5 + new F1 |
| 3 | Intro, Background, Discussion, Limitations |
| 4 | Abstract, polish, Zenodo deposit, internal review |
