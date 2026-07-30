# Detector reliability report

**Purpose:** test whether automated structured-field detection could plausibly distort public-satisfiability ceiling findings via extraction error.

## Method

Hide-field / recover-field evaluation on native structured fields per source:

1. Remove one structured field from each record.
2. Build context from remaining schema fields (no derived normalised columns).
3. Attempt deterministic recovery (substring, categorical, token-set, boolean).
4. Compare recovered vs original; compute precision, recall, F1, exact-match rate.

## Source-level averages

| Source | Fields | Mean F1 | Weighted F1 | Mean coverage % | Mean exact-match % |
|--------|-------:|--------:|------------:|----------------:|-------------------:|
| CA-GC-AI-REG | 6 | 0.481 | 0.4637 | 79.6 | 50.5 |
| EU-PSTW | 5 | 0.5601 | 0.4201 | 80.0 | 45.3 |
| NL-ALGO-REG | 7 | 0.3555 | 0.3612 | 91.7 | 32.0 |
| UK-ATRS | 3 | 0.5254 | 0.3503 | 100.0 | 33.8 |
| US-OMB-2025 | 8 | 0.3216 | 0.2494 | 65.6 | 46.0 |

**Overall mean F1 (non-empty fields):** 0.414
**Overall mean precision (non-empty fields):** 1.000

**Interpretation:** Precision near 1.0 across sources indicates hide-field recovery does not hallucinate structured values (no false-positive extractions). Low recall on non-redundant schema fields (e.g. lifecycle stage, status) confirms those values exist only as structured columns—not recoverable prose—matching the native-field mapping used in public-satisfiability analysis.

## Field-level results

| Source | Field | Coverage % | Precision | Recall | F1 | Exact-match % | Failure mode |
|--------|-------|----------:|----------:|-------:|---:|--------------:|--------------|
| CA-GC-AI-REG | ai_system_status_en | 89.8 | 1.0 | 0.0297 | 0.0577 | 12.9 | — |
| CA-GC-AI-REG | data_sources_en | 71.4 | 1.0 | 0.1735 | 0.2957 | 41.0 | long_narrative |
| CA-GC-AI-REG | government_organization | 100.0 | 1.0 | 0.1019 | 0.185 | 10.2 | — |
| CA-GC-AI-REG | involves_personal_information | 75.7 | 1.0 | 1.0 | 1.0 | 100.0 | cross_field_redundancy |
| CA-GC-AI-REG | name_ai_system_en | 100.0 | 1.0 | 0.6359 | 0.7774 | 63.6 | — |
| CA-GC-AI-REG | vendor_information | 40.8 | 1.0 | 0.3988 | 0.5702 | 75.5 | — |
| EU-PSTW | Application type | 100.0 |  | 0.0 |  | 0.0 | — |
| EU-PSTW | Name | 100.0 | 1.0 | 0.6243 | 0.7687 | 62.4 | — |
| EU-PSTW | Primary Technology | 100.0 | 1.0 | 0.1416 | 0.248 | 14.2 | — |
| EU-PSTW | Responsible organisation | 100.0 | 1.0 | 0.4967 | 0.6637 | 49.7 | — |
| EU-PSTW | Status | 0.0 |  |  |  | 100.0 | empty_field_high |
| NL-ALGO-REG | human_intervention | 97.6 | 1.0 | 0.0787 | 0.1459 | 10.0 | long_narrative |
| NL-ALGO-REG | lawful_basis | 75.4 | 1.0 | 0.1671 | 0.2864 | 37.2 | long_narrative |
| NL-ALGO-REG | name | 100.0 | 1.0 | 0.6429 | 0.7826 | 64.3 | — |
| NL-ALGO-REG | organization | 100.0 | 1.0 | 0.5229 | 0.6867 | 52.3 | — |
| NL-ALGO-REG | provider | 77.6 | 1.0 | 0.2493 | 0.3992 | 41.8 | — |
| NL-ALGO-REG | risks | 91.2 | 1.0 | 0.0399 | 0.0768 | 12.5 | long_narrative |
| NL-ALGO-REG | status | 100.0 | 1.0 | 0.0586 | 0.1108 | 5.9 | — |
| UK-ATRS | description | 100.0 |  | 0.0 |  | 0.0 | long_narrative |
| UK-ATRS | organisation_title | 100.0 | 1.0 | 0.0301 | 0.0584 | 3.0 | search_metadata_only |
| UK-ATRS | title | 100.0 | 1.0 | 0.985 | 0.9924 | 98.5 | search_metadata_only |
| US-OMB-2025 | agency_name | 100.0 | 1.0 | 0.1008 | 0.1831 | 10.1 | — |
| US-OMB-2025 | classification | 81.7 | 1.0 | 0.0627 | 0.1181 | 23.5 | — |
| US-OMB-2025 | development_stage | 90.6 | 1.0 | 0.0235 | 0.046 | 11.5 | — |
| US-OMB-2025 | have_ato | 42.7 | 1.0 | 0.8586 | 0.9239 | 94.0 | — |
| US-OMB-2025 | human_roles | 0.0 |  |  |  | 100.0 | empty_field_high |
| US-OMB-2025 | is_high_impact | 88.2 | 1.0 | 0.0035 | 0.0069 | 12.1 | — |
| US-OMB-2025 | use_case_name | 100.0 | 1.0 | 0.3155 | 0.4797 | 31.6 | — |
| US-OMB-2025 | vendor_name | 21.9 | 1.0 | 0.3278 | 0.4938 | 85.3 | — |

## Uncertainty notes

- Hide-field evaluation uses deterministic substring/categorical heuristics as a conservative proxy for automated extraction; no generative LLM recovery is applied unless configured.
- Context excludes the hidden field and empty values only; derived normalised columns (programme_title, agency_or_owner) are not used to avoid label leakage.
- Boolean and categorical fields use corpus-derived allowed values where applicable.
- UK ATRS sample (n=133) yields wider confidence intervals than US/NL/EU sources.
- High recovery F1 indicates structured access is reliable; low F1 on narrative fields does not inflate public-satisfiability ceilings because mapping uses native schema fields.

## Failure modes observed

- **cross_field_redundancy:** Structured inventories duplicate key values across fields (conservative F1).
- **empty_field_high:** High empty rate: recovery metrics dominated by absence, not extraction noise.
- **long_narrative:** Long free-text field: token-set recovery misses paraphrases.
- **search_metadata_only:** UK ATRS evaluation uses Search API metadata, not full HTML record body.

## Robustness conclusion

**Can extraction errors plausibly explain the public-evidence ceiling finding?** **No.** Text-recovery precision is ~1.0 (no false-positive field detections), so extraction noise cannot fabricate gate-level evidence. Non-redundant inventory metadata is structurally encoded; hide-field recall is low for those columns, confirming the satisfiability pipeline correctly relies on native schema fields rather than narrative mining.

**Does the main finding survive realistic detector error?** **Yes.** Realistic error modes are false negatives (missed narrative paraphrases), which would **under-estimate** partial public signal—not create spurious gate reachability. Sensitivity analysis already shows 100% gate-unreachable under partition perturbation; detector noise cannot elevate shortfall level to 4.

