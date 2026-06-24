# Table plan — five main tables

All tables export from frozen pipeline outputs. Final formatting: LaTeX `booktabs` for Data & Policy submission.

---

## T1 — Corpus composition

**Purpose:** Document reproducible multi-source corpus for policy readers.

**Source files**
- `data/source_registry_expanded.csv`
- `data/pilot_programme_records.csv` (counts)

**Columns**
| Column | Content |
|--------|---------|
| Source ID | US-OMB-2025, CA-GC-AI-REG, NL-ALGO-REG, EU-PSTW, UK-ATRS |
| Jurisdiction | Federal / national / multi-country |
| Official access method | Direct CSV, API bulk, Search API |
| Collection date | 2026-06-24 |
| Records (n) | 3611 / 412 / 1484 / 1794 / 133 |
| Programme unit | Use case / system / algorithm / case / transparency record |
| Filter applied | None / AI-primary / ATRS document type |
| Overlap with Paper 2 | Low / medium (flag only) |

**Footnote:** Total n = 7,434. PSTW filtered to Primary Technology = Artificial Intelligence. No Paper 2 municipal corpus included.

**Status:** Ready from registry; needs journal formatting + one-line policy relevance per source.

---

## T2 — LocalGovBench evidence requirements and public/internal partition

**Purpose:** Present the 25 requirements and baseline satisfiability classes.

**Source files**
- `config/localgovbench_criteria_v0.yaml`
- `outputs/criterion_satisfiability_summary.csv`
- `outputs/minimum_internal_evidence_set.csv`

**Columns**
| Column | Content |
|--------|---------|
| Criterion ID | Short name |
| Dimension | 5 governance dimensions |
| Evidence hint (abbrev.) | One line |
| Expected artefact type | Gate ≥3 target |
| Partition class | structurally_internal / partially_public / public_satisfiable |
| Max shortfall level | 0–2 |
| Gate reachable (public)? | No for all 25 |
| Internal evidence floor | Required artefact type (from minimum set) |

**Summary row:** 15 internal (60%), 9 partial + 1 public (40%), 0 gate-reachable.

**Status:** Ready; consolidate YAML + CSV into single submission table.

---

## T3 — Evidence shortfall level per criterion and jurisdiction (source)

**Purpose:** Show heterogeneous ceiling across sources—not a ranking.

**Source file:** `outputs/field_criterion_coverage_matrix.csv`

**Format:** 25 rows (criteria) × 5 columns (sources) + row/column marginals.

**Cell values:** Shortfall level 0–4 (colour-coded in figure; numeric in table).

**Marginals**
- Per criterion: max shortfall across sources
- Per source: mean and max shortfall (not a league table—descriptive only)

**Highlight cells:** NL lawful_basis, human_intervention; US/CA/NL lifecycle; level-2 partial signals.

**Status:** Ready from matrix CSV; consider supplemental heatmap (F2) as visual counterpart.

---

## T4 — Sensitivity and unit-commensurability results

**Purpose:** Demonstrate main finding survives partition and granularity perturbation.

**Source files**
- `outputs/sensitivity_main_results.csv`
- `outputs/unit_commensurability_summary.csv`

**Panel A — Partition sensitivity**
| Scenario | Internal % | Partial/public % | Gate unreachable % | n criteria gate reachable |
|----------|----------:|-----------------:|-------------------:|----------------------------:|
| Baseline | 60.0 | 40.0 | 100.0 | 0 |
| Conservative | 84.0 | 16.0 | 100.0 | 0 |
| Liberal | 28.0 | 72.0 | 100.0 | 0 |

**Panel B — Unit commensurability**
| Scenario | Records | Retained % | Internal % | Gate unreachable % | Shortfall L0/L1/L2/L3/L4 |
|----------|--------:|-----------:|-----------:|-------------------:|---------------------------|
| A all | 7434 | 100 | 60.0 | 100 | 7/10/8/0/0 |
| B min info | 5204 | 70.0 | 60.0 | 100 | 7/10/8/0/0 |
| C excl complex | 6685 | 89.9 | 60.0 | 100 | 7/10/8/0/0 |

**Footnote:** Partition varies; gate invariant.

**Status:** Ready from frozen CSVs.

---

## T5 — Detector and classification reliability

**Purpose:** Show findings are not extraction artefacts; partition is robust.

**Source files**
- `outputs/detector_reliability_by_source.csv`
- `outputs/partition_sensitivity_summary.csv`

**Panel A — Hide-field detector (by source)**
| Source | Mean precision | Mean recall | Mean F1 | Weighted F1 |
|--------|---------------:|------------:|--------:|------------:|
| US OMB | 1.000 | 0.242 | 0.322 | 0.249 |
| Canada | 1.000 | 0.390 | 0.481 | 0.464 |
| Netherlands | 1.000 | 0.251 | 0.356 | 0.361 |
| EU PSTW | 1.000 | 0.316 | 0.560 | 0.420 |
| UK ATRS | 1.000 | 0.338 | 0.525 | 0.350 |
| **Global** | **1.000** | — | **0.414** | — |

**Panel B — Partition classifier agreement**
| Metric | Value |
|--------|------:|
| Deterministic vs heuristic agreement | 92.0% |
| Disagreement criteria | 2 (role definition; data sovereignty) |
| Gate status changes | 0 |

**Status:** Ready; add one-sentence interpretation row (errors = false negatives).

---

## Table production order

1. T1 (corpus) — simplest, sets context
2. T2 (requirements) — defines instrument slice
3. T3 (shortfall matrix) — core result
4. T4 (robustness) — answers definitional-risk reviewers
5. T5 (reliability) — answers extraction-risk reviewers
