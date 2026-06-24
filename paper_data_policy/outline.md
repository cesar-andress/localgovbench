# Manuscript outline — Paper 1 (Data & Policy)

**Working framing:** The paper measures the **public-evidence ceiling** of LocalGovBench evidence requirements. It does **not** measure AI governance readiness.

**Target:** Data & Policy (primary); Information Polity (fallback).

---

## 1. Introduction

**Purpose:** Establish the policy problem, define the unit of analysis, and state the bounded contribution.

**Key claims**
- Public-sector AI programme inventories are expanding rapidly as transparency instruments.
- Policy evaluators increasingly ask whether public registers can support evidence-based governance assessment.
- LocalGovBench v0.1 specifies 25 programme-level **evidence requirements** with score ≥3 **evidence gates** tied to named primary artefacts.
- This paper asks: **how far can official public inventories satisfy those requirements?** — not whether programmes are “ready.”

**Evidence / results to cite**
- Corpus scale: 7,434 programme records across five official sources (US, Canada, Netherlands, EU PSTW, UK).
- Headline result: 0/25 criteria **gate-reachable** from public inventories; max **evidence shortfall** level = 2.

**Tables / figures**
- None in introduction; forward-reference F2 and T1.

**Non-claims to state**
- We do not assess governance quality, legal compliance, or readiness.
- We do not rank jurisdictions or programmes.
- Absence of public evidence is not evidence of absent internal governance.

---

## 2. Background and policy context

**Purpose:** Situate programme inventories in AI transparency policy without collapsing into Paper 2 documentary analysis.

**Key claims**
- National and supranational AI use-case registers (OMB, Algoritmeregister, GC AI Register, PSTW, ATRS) are policy instruments for **programme-level transparency**.
- Transparency metadata ≠ governance dossier; registers expose schema fields, not primary control artefacts.
- Evidence-gated assessment protocols (named artefacts for score ≥3) create a testable **ceiling** question for public data.

**Evidence / results to cite**
- Source registry metadata (`source_registry_expanded.csv`).
- Examples of native fields vs required artefacts (lifecycle status vs IR plan).

**Tables / figures**
- Optional small box: “Inventory field vs evidence requirement” (may reuse T3 row examples in text).

**Non-claims**
- Do not claim inventories are failures or useless.
- Do not centre vendor stewardship, procurement clauses, or document genres (Paper 2 firewall).

---

## 3. LocalGovBench evidence requirements (instrument slice)

**Purpose:** Present the 25 criteria as **evidence requirements**, not a readiness scorecard.

**Key claims**
- LocalGovBench v0.1 organises 25 criteria across five governance dimensions.
- Each criterion specifies an **evidence hint**, expected artefact type, and score ≥3 **gate** (primary named artefact).
- The paper uses the instrument as a **requirement catalogue** for public-evidence mapping — not to produce maturity scores.

**Evidence / results to cite**
- `config/localgovbench_criteria_v0.yaml`
- Dimension structure (5×5 criteria).

**Tables / figures**
- **T2** — evidence requirements and public/internal partition.

**Non-claims**
- Do not describe LocalGovBench as a validated readiness benchmark.
- Do not report 0–4 maturity scores for programmes.

---

## 4. Methods

**Purpose:** Make the pipeline auditable and reproducible for Data & Policy readers.

### 4.1 Corpus construction
**Key claims:** Five official sources; machine-readable acquisition; normalised programme records; no Paper 2 corpus.

**Cite:** T1; `build_pilot_corpus.py`; collection dates in `source_registry_expanded.csv`.

### 4.2 Source-schema to evidence-requirement mapping
**Key claims:** Native inventory fields mapped to criteria; coverage classes; **evidence shortfall** scale 0–4.

**Cite:** `mapping_rules.py`; T3; F2.

### 4.3 Public / internal partition
**Key claims:** Deterministic rules from shortfall + evidence hints; dual-classifier robustness (92% agreement).

**Cite:** `validate_partition_robustness.py`; T5.

### 4.4 Sensitivity and commensurability
**Key claims:** Conservative/liberal partition scenarios; unit commensurability filters (Scenarios A/B/C).

**Cite:** T4; F3.

### 4.5 Detector reliability
**Key claims:** Hide-field / recover-field evaluation; precision = 1.0; errors are false negatives.

**Cite:** T5; detector report.

**Non-claims**
- No readiness scoring; no jurisdiction ranking; no municipal documentary observability.

---

## 5. Results

**Purpose:** Present frozen empirical package in policy-relevant order.

### 5.1 Corpus composition
**Cite:** T1.

### 5.2 Public-evidence ceiling and shortfall gradient
**Key claims**
- 60% structurally internal / 40% partial-public (baseline partition).
- Shortfall distribution: L0=7, L1=10, L2=8, L3=0, L4=0.
- 0/25 gate-reachable.

**Cite:** T2, T3, F1, F2.

### 5.3 Cross-jurisdiction comparison
**Key claims:** NL adds level-2 direct fields (lawful basis, human intervention); none reach gate.

**Cite:** F4; T3.

### 5.4 Robustness
**Key claims:** Gate 100% unreachable under conservative (84% internal) and liberal (72% partial) scenarios; unit commensurability invariant.

**Cite:** T4, F3.

### 5.5 Minimum internal evidence floor
**Key claims:** All 25 criteria require non-public artefacts for gate ≥3; dimension-balanced internal evidence set.

**Cite:** T2 (internal column); F5; `minimum_internal_evidence_set.csv`.

**Non-claims**
- Do not interpret partial signals as sufficient governance evidence.

---

## 6. Discussion

**Purpose:** Interpret ceiling findings for policy designers and assessment practitioners.

**Key claims**
- Public inventories provide **partial signals** (metadata, lifecycle, risk narratives) but not **gate-reachable** evidence.
- Policy implication: transparency registers and assessment protocols serve different functions; aligning them requires explicit **internal evidence floor** specifications.
- Multi-jurisdiction replication strengthens external validity vs single-register studies.
- Shortfall gradient shows heterogeneity — the 0/25 gate result is empirically bounded, not purely definitional.

**Evidence:** Sensitivity, commensurability, detector reliability summaries.

**Non-claims**
- Inventories are not “bad”; they are the wrong layer for primary artefact gates.
- No claim that governments lack internal governance when public evidence is absent.

---

## 7. Limitations

**Purpose:** Pre-empt reviewer attacks.

**Key claims**
- Programme-level inventories ≠ municipal sovereign LLM programmes (scope boundary).
- PSTW is curated, not statutory; UK ATRS n=133.
- Mapping rules are expert-structured, not Delphi-calibrated (future work).
- Hide-field test uses deterministic recovery, not production NLP.
- Paper reports **ceiling** only; dossier/Delphi validation is separate track.

---

## 8. Conclusion

**Purpose:** One-paragraph policy takeaway + research agenda.

**Key claims**
- Public-evidence ceiling is low for gate-level requirements across 7,434 records and five sources.
- Minimum internal evidence set is complete (25/25).
- Contribution: reproducible method + corpus + bounded claims for Data & Policy.

**Non-claims:** No readiness verdict; no ranking; no compliance certification.

---

## 9. Data and code availability

**Purpose:** Data & Policy artifact statement.

**Cite:** Repository path; Zenodo deposit plan (`next_steps_to_draft.md`); pipeline `run_validation_upgrade.py`.

---

## Appendices (optional for journal; required for OSF)

- A1: Full criterion catalogue
- A2: Per-source field schemas
- A3: Partition disagreement cases (2 criteria)
- A4: Granularity proxy rules (Scenarios B/C)
