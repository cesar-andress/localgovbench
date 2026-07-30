# Results freeze — Paper 1 empirical package

**Freeze date:** 2026-06-24  
**Pipeline:** `python3.12 scripts/run_validation_upgrade.py` (+ `evaluate_detector_reliability.py`, `analyze_unit_commensurability.py`)  
**Rule:** Numbers below are authoritative for manuscript drafting unless the pipeline is re-run and this file is updated.

---

## Corpus (T1)

| Source | Records |
|--------|--------:|
| US-OMB-2025 | 3,611 |
| CA-GC-AI-REG | 412 |
| NL-ALGO-REG | 1,484 |
| EU-PSTW (AI-primary) | 1,794 |
| UK-ATRS | 133 |
| **Total** | **7,434** |

Collection date: 2026-06-24. PSTW filter: Primary Technology = Artificial Intelligence.

---

## Evidence requirements (T2)

| Metric | Value |
|--------|------:|
| Criteria (LocalGovBench v0.1) | 25 |
| Dimensions | 5 |
| Baseline structurally internal | 15 (60.0%) |
| Baseline partially/publicly satisfiable | 10 (40.0%) |
| — partially public | 9 |
| — public satisfiable | 1 (`operational_lifecycle_management`) |
| Evidence gate ≥3 reachable (public) | **0 (0.0%)** |
| Gate unreachable | **25 (100.0%)** |
| Maximum observed shortfall level | **2** |
| Minimum internal evidence set size | **25/25** |

---

## Shortfall distribution (baseline)

| Level | Label | Criteria count |
|------:|-------|---------------:|
| 0 | no_public_field | 7 |
| 1 | weak_metadata_proxy | 14 |
| 2 | partial_programme_level_signal | 4 |
| 3 | named_public_artefact_possible | 0 |
| 4 | full_evidence_gate_reachable | 0 |

---

## Dimension ceilings (baseline)

| Dimension | Partial/public ceiling % | Gate unreachable % |
|-----------|-------------------------:|-------------------:|
| Legal and Regulatory Compliance | 40.0 | 100.0 |
| Technical and Security Readiness | 0.0 | 100.0 |
| Organizational Governance | 60.0 | 100.0 |
| Operational Management | 60.0 | 100.0 |
| Strategic Sovereignty | 40.0 | 100.0 |

---

## Sensitivity analysis (T4 Panel A)

| Scenario | Internal % | Partial/public % | Gate unreachable % |
|----------|----------:|-----------------:|-------------------:|
| Baseline | 60.0 | 40.0 | 100.0 |
| Conservative | 84.0 | 16.0 | 100.0 |
| Liberal | 28.0 | 72.0 | 100.0 |

---

## Unit commensurability (T4 Panel B)

| Scenario | Records | Retained % | Internal % | Gate unreachable % | Shortfall L0/L1/L2/L3/L4 |
|----------|--------:|-----------:|-----------:|-------------------:|----------------------------|
| A all records | 7,434 | 100.0 | 60.0 | 100.0 | 7 / 14 / 4 / 0 / 0 |
| B min information | 5,204 | 70.0 | 60.0 | 100.0 | 7 / 14 / 4 / 0 / 0 |
| C exclude high complexity | 6,685 | 89.9 | 60.0 | 100.0 | 7 / 14 / 4 / 0 / 0 |

Partition changes vs A: **0 criteria**. Gate changes: **0**.

---

## Partition robustness (T5)

| Metric | Value |
|--------|------:|
| Deterministic vs heuristic class agreement | 92.0% |
| Disagreement criteria | `organizational_role_definition`, `strategic_sovereignty_data_sovereignty` |
| Gate status changes | 0 |

---

## Detector reliability (T5)

| Metric | Value |
|--------|------:|
| Global mean precision (non-empty fields) | 1.000 |
| Global mean F1 (non-empty fields) | 0.414 |

### By source (mean F1)

| Source | Mean F1 | Weighted F1 |
|--------|--------:|------------:|
| US-OMB-2025 | 0.322 | 0.249 |
| CA-GC-AI-REG | 0.481 | 0.464 |
| NL-ALGO-REG | 0.356 | 0.361 |
| EU-PSTW | 0.560 | 0.420 |
| UK-ATRS | 0.525 | 0.350 |

---

## Manuscript GO decision

Validation upgrade: **GO** | Manuscript drafting: **GO** | Primary venue: **Information Polity**

Source: `outputs/pilot_go_decision.json`

---

## Frozen output files (regenerate, do not hand-edit)

See `localgovbench_measurement_validation/pilot_public_satisfiability/outputs/` and `figures/` — full list in `next_steps_to_draft.md`.
