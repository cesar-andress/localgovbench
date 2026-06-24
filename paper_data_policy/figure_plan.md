# Figure plan — five main figures

All figures exist in `localgovbench_measurement_validation/pilot_public_satisfiability/figures/` unless noted. Final submission: 300 dpi PNG or vector PDF; accessible colour palette; no jurisdiction ranking visual language.

---

## F1 — Public/internal criterion partition map

**Purpose:** Visual overview of how 25 evidence requirements split between structurally internal and partially/publicly satisfiable classes.

**Recommended form:** Horizontal bar or tile map grouped by five dimensions; colour = partition class (internal / partial / public).

**Source data:** `outputs/criterion_satisfiability_summary.csv`

**Existing asset:** Adapt from `criterion_satisfiability_heatmap.png` OR create new partition strip chart (preferred for clarity).

**Caption must state:** Classification reflects **public-evidence satisfiability**, not governance quality; no readiness scores.

**Production note:** New matplotlib script `figures/make_f1_partition_map.py` (to draft) — cleaner than coverage heatmap for Paper 1 narrative.

---

## F2 — Evidence shortfall gradient

**Purpose:** Core empirical figure — heterogeneous shortfall across criteria and sources.

**Existing asset:** `figures/evidence_shortfall_gradient_heatmap.png` ✓

**Source data:** `outputs/field_criterion_coverage_matrix.csv`

**Y-axis:** 25 criteria (grouped by dimension)  
**X-axis:** 5 sources (not ranked)  
**Colour scale:** Shortfall 0–4 (levels 3–4 empty by design)

**Caption highlights:** Max observed level = 2; gate level 4 never observed; NL contributes level-2 cells.

**Status:** Ready; may refine labels for journal font size.

---

## F3 — Gate reachability under sensitivity scenarios

**Purpose:** Show partition shifts but **gate invariant** under conservative/liberal rules.

**Existing asset:** `figures/sensitivity_public_satisfiability.png` ✓

**Source data:** `outputs/sensitivity_main_results.csv`

**Panels:** Grouped bars — internal %, partial/public %, gate unreachable % — for baseline / conservative / liberal.

**Caption:** Emphasise gate unreachable = 100% in all three scenarios.

**Optional enhancement:** Add thin reference line at 100% for gate panel.

**Status:** Ready.

---

## F4 — Cross-jurisdiction ceiling comparison

**Purpose:** Compare mean/max shortfall by source — descriptive, not a league table.

**Existing asset:** `figures/cross_jurisdiction_ceiling_comparison.png` ✓

**Source data:** `outputs/field_criterion_coverage_matrix.csv`

**Caption wording:** “Source-level public-evidence ceiling descriptors; higher values indicate richer partial signals in inventory schema, not superior governance.”

**Status:** Ready.

---

## F5 — Minimum internal evidence set by dimension

**Purpose:** Policy-facing visual of **internal evidence floor** — all 25 criteria require non-public artefacts for gate ≥3.

**Existing asset:** `figures/minimum_internal_evidence_set_by_dimension.png` ✓

**Source data:** `outputs/minimum_internal_evidence_set.csv`

**Bars:** 5 criteria per dimension (balanced).

**Caption:** Complete internal evidence floor (25/25); illustrative of dossier requirements beyond inventories.

**Status:** Ready.

---

## Figures NOT in main five (supplement only)

| Asset | Use |
|-------|-----|
| `detector_reliability_by_source.png` | Supplement or T5 companion |
| `unit_commensurability_stability.png` | Supplement for commensurability |
| `unit_commensurability_partition_comparison.png` | Supplement |
| `gate_reachability_by_dimension.png` | Redundant with F3/T4 |
| `dimension_public_ceiling_barplot.png` | Optional supplement |

---

## Figure production order

1. **F2** — centrepiece; already polished
2. **F3** — robustness story for reviewers
3. **F5** — policy takeaway (internal evidence floor)
4. **F4** — multi-source credibility
5. **F1** — new partition map (draft last once T2 final)

## Data & Policy formatting notes

- Single column width: max 85 mm; double column: 178 mm
- Use colourblind-safe palette (avoid red-green only)
- Figure + table caps must repeat **no ranking / no readiness scores**
