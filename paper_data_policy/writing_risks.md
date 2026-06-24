# Writing risks and mitigation strategies

Ten reviewer risks most likely for a Data & Policy submission, with **exact wording strategies** to neutralize each.

---

## Risk 1 — “The 0/25 gate result is tautological / definitional.”

**Mitigation wording:**
> “We treat tautology as an empirical question. The graded **evidence shortfall** scale (levels 0–2 observed; 3–4 never observed) shows heterogeneous partial signals across requirements and sources. Conservative and liberal partition scenarios shift internal/public counts (84%–28% internal) while **gate reachability remains 0/25**, indicating the gate finding is not fixed by classification alone.”

**Cite:** T4, F2, F3.

---

## Risk 2 — “You are secretly measuring readiness.”

**Mitigation wording:**
> “**No readiness scores were assigned.** Programmes and jurisdictions were not ranked. Analysis maps inventory schema fields to **evidence requirement satisfiability** and **gate reachability** only.”

**Cite:** claims_and_nonclaims.md; no score columns in outputs.

---

## Risk 3 — “Absent public evidence = no governance.”

**Mitigation wording:**
> “Non-availability of gate-level **public evidence** does not imply absence of **internal governance artefacts**. We specify a **minimum internal evidence set** (25/25 criteria) precisely because inventories cannot substitute for dossier evidence.”

**Cite:** F5, T2 internal floor column.

---

## Risk 4 — “Single jurisdiction / US-dominated corpus.”

**Mitigation wording:**
> “The corpus spans five official sources (7,434 records): US federal (48.6%), EU PSTW AI-primary (24.1%), Dutch national register (20.0%), Canada (5.5%), UK ATRS (1.8%). Findings are **replicated across sources** at gate level (0/25 each).”

**Cite:** T1; avoid ranking language when citing shares.

---

## Risk 5 — “Programme inventories ≠ municipal sovereign LLM programmes.”

**Mitigation wording:**
> “Scope is **programme-level public-sector AI inventories** as policy transparency instruments. We do not generalise to municipal sovereign LLM deployments; we test whether **programme-level evidence gates** are satisfiable from **programme-level public fields**—a necessary but not sufficient condition for narrower municipal claims.”

**Cite:** Limitations section.

---

## Risk 6 — “Mapping rules are subjective expert judgment.”

**Mitigation wording:**
> “Mapping rules are **documented, rule-based, and frozen** (`mapping_rules.py`). Dual-classifier partition agreement is **92%**; disagreements affect two criteria and **do not change gate status**.”

**Cite:** T5; partition_validation_agreement.csv.

---

## Risk 7 — “Extraction / automation artefacts drive results.”

**Mitigation wording:**
> “Hide-field detector evaluation shows **precision = 1.000** (no false-positive field recovery). Errors are **false negatives** (mean F1 = 0.414), which would **under-estimate** partial signals—not fabricate gate reachability.”

**Cite:** T5; detector report.

---

## Risk 8 — “Small tools vs major systems — unit heterogeneity.”

**Mitigation wording:**
> “Unit **commensurability** filters (minimum information threshold; exclude high-complexity proxy) retain 5,204–7,434 records. **Gate unreachable remains 100%**; shortfall distribution unchanged (L0=7, L1=10, L2=8).”

**Cite:** T4 Panel B; unit commensurability report.

---

## Risk 9 — “Overlap with Paper 2 / duplicate publication.”

**Mitigation wording:**
> “This study uses **national/EU programme inventory schemas**, not the municipal documentary corpus analysed elsewhere. We do not analyse document genres, vendor stewardship as central claim, or Documentary Accountability Architecture.”

**Cite:** contribution_statement.md Paper 2 table.

---

## Risk 10 — “So what for policy?”

**Mitigation wording:**
> “Policy implication: align **transparency publication** with **assessment evidence tiers**. Inventories should continue publishing **partial signals** (lifecycle, oversight narratives) while assessment protocols must specify an **internal evidence floor** for gate-level requirements—listed explicitly in our minimum internal evidence set.”

**Cite:** Discussion; F5.

---

## Global phrasing substitutions (search-replace before submission)

| Replace | With |
|---------|------|
| readiness | public-evidence ceiling / evidence requirement satisfiability |
| observability | public-evidence ceiling |
| disclosure (as noun of finding) | published inventory metadata |
| benchmark (verb/noun of performance) | evidence requirement catalogue / satisfiability analysis |
| rank / ranking | describe / compare sources without ordinality |
| maturity | shortfall level / gate reachability |
| validate the instrument | specify requirements / test public ceiling |
| compliance | alignment with policy themes (non-legal) |
