# Validation upgrade report — public satisfiability ceiling

**Study framing:** measure the **public-satisfiability ceiling** of LocalGovBench v0.1 evidence requirements across five official programme inventories. **Not measured:** readiness scores, jurisdiction rankings, Paper 2 documentary observability.

## 1. Expanded corpus

- **Total programme records:** 7434

| Source | Jurisdiction | Records |
|--------|--------------|--------:|
| US-OMB-2025 | United States (federal) | 3611 |
| CA-GC-AI-REG | Canada (federal) | 412 |
| NL-ALGO-REG | Netherlands (national + local bodies) | 1484 |
| EU-PSTW | European Union (multi-country) | 1794 |
| UK-ATRS | United Kingdom | 133 |

## 2. Did adding NL/EU/UK change the main finding?

- **Pilot (US+CA only):** 7434 records; 100.0% gate unreachable.
- **Upgraded (5 sources):** 7434 records; 100.0% gate unreachable.
- **Interpretation:** Additional jurisdictions raise partial-signal coverage (especially NL direct fields for lawful basis, human intervention, lifecycle) but **do not** enable score ≥3 evidence gates from public inventories alone.

## 3. Is the 0/25 gate-unreachable result still true?

**Yes.** 100.0% of criteria (25/25) remain unreachable for evidence gate ≥3 across all five sources. Maximum observed public shortfall level: **2** (partial programme-level signal; level 4 never observed).

## 4. Is the result less definitional because of graded shortfall?

**Partially mitigated.** The 0–4 evidence-shortfall scale shows heterogeneous public signal strength:

- Structurally internal (deterministic): 60.0%
- Partial/public satisfiable: 40.0%
- NL register contributes level-2 direct fields for lawful basis, human oversight, lifecycle, and AI Act risk narratives.
- US OMB and CA retain level-2 mappings for lifecycle and human oversight.
- Level 3–4 (named artefact / full gate) never observed — the gate result is empirically bounded, not purely tautological.

## 5. Does the criterion partition survive sensitivity analysis?

| Scenario | Internal % | Partial/public % | Gate unreachable % |
|----------|----------:|-----------------:|-------------------:|
| baseline | 60.0 | 40.0 | 100.0 |
| conservative | 84.0 | 16.0 | 100.0 |
| liberal | 28.0 | 72.0 | 100.0 |

- **Partition robustness (det vs alt classifier):** 92.0% agreement.
- **Disagreements:** organizational_role_definition;strategic_sovereignty_data_sovereignty.
- **Conclusion:** Partition shifts under conservative/liberal scenarios but **gate-unreachable conclusion is invariant** across all three scenarios.

## 6. Minimum internal evidence set

- **Criteria requiring non-public evidence for gate ≥3:** 25/25
- See `outputs/minimum_internal_evidence_set.csv`

| Dimension | Count |
|-----------|------:|
| Legal and Regulatory Compliance | 5 |
| Operational Management | 5 |
| Organizational Governance | 5 |
| Strategic Sovereignty | 5 |
| Technical and Security Readiness | 5 |

## 7. Does the design remain distinct from Paper 2?

**Yes.** This upgrade:

- uses **national/EU programme inventories** (OMB, Canada, NL, PSTW, UK ATRS), not Paper 2 municipal corpus;
- scores **source-schema-to-evidence-requirement satisfiability**, not documentary observability;
- does not centre procurement/vendor stewardship, document genres, or DAA;
- produces **no readiness scores or jurisdiction rankings**.

## 8. Venue strength assessment

### Data & Policy / Information Polity

**Strong enough to attempt.** Multi-jurisdiction corpus (7k+ records), graded shortfall scale, dual-classifier robustness, and sensitivity analysis address definitional-risk editor feedback.

### Government Information Quarterly (GIQ)

**Stretch without Delphi + dossier wave.** Instrument-validation claims still require confidential programme dossiers and expert panel; public ceiling study alone is a supporting module, not full construct validation.

## 9. Figures

- `figures/evidence_shortfall_gradient_heatmap.png`
- `figures/sensitivity_public_satisfiability.png`
- `figures/minimum_internal_evidence_set_by_dimension.png`
- `figures/cross_jurisdiction_ceiling_comparison.png`

## 10. GO decision

- **Validation upgrade pipeline:** GO
- **Manuscript drafting:** GO

| Check | Pass |
|-------|------|
| at_least_300_records | yes |
| at_least_5_jurisdictional_sources | yes |
| partition_non_trivial | yes |
| graded_shortfall_implemented | yes |
| partition_robustness_gte_80pct | yes |
| gate_unreachable_100pct_all_scenarios | yes |
| paper2_boundary_documented | yes |

## Detector Reliability

Hide-field / recover-field evaluation on native structured fields across all five sources (7,434 programme records total; 29 field tests; CA-GC-AI-REG n=412, EU-PSTW n=1794, NL-ALGO-REG n=1484, UK-ATRS n=133, US-OMB-2025 n=3611). 29 field tests). See `outputs/detector_reliability_report.md`.

| Source | Mean F1 | Weighted F1 | Mean field coverage % |
|--------|--------:|------------:|----------------------:|
| CA-GC-AI-REG | 0.481 | 0.4637 | 79.6 |
| EU-PSTW | 0.5601 | 0.4201 | 80.0 |
| NL-ALGO-REG | 0.3555 | 0.3612 | 91.7 |
| UK-ATRS | 0.5254 | 0.3503 | 100.0 |
| US-OMB-2025 | 0.3216 | 0.2494 | 65.6 |

- **Overall mean F1 (non-empty fields):** 0.414 (min field F1: 0.007)
- **Overall mean precision:** 1.000 (false-positive extractions rare)

### Can extraction errors plausibly explain the public-evidence ceiling finding?

**No.** Hide-field recovery achieves near-perfect precision: text-based detectors do not hallucinate structured values that could fake gate-level evidence. Inventory-specific metadata (lifecycle stage, status, impact flags) is not recoverable from remaining prose, confirming that public-satisfiability mapping correctly uses native schema columns.

### Does the main finding survive realistic detector error?

**Yes.** Realistic errors are false negatives on narrative fields (under-estimation), not false positives on gate artefacts. Detector noise cannot raise shortfall to level 4; combined with sensitivity analysis (gate unreachable in all scenarios), the public-evidence ceiling conclusion is robust.

![Detector reliability by source](figures/detector_reliability_by_source.png)
