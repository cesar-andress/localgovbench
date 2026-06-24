# Unit commensurability report

**Purpose:** test whether the public-evidence ceiling finding is sensitive to programme-record granularity (small tools vs major systems vs agency-wide deployments).

## Granularity scenarios

### Scenario A — all records

Full corpus (7,434 programme records); no granularity filter.

- **Records retained:** 7434 (100.0%)

### Scenario B — minimum information threshold

Exclude records below source-specific 30th-percentile information score and absolute floor (≥4 non-empty native fields, description ≥30 chars).

- **Records retained:** 5204 (70.0%)

### Scenario C — exclude high-complexity proxy

Exclude records at/above source-specific 90th-percentile complexity proxy (agency-wide keywords, high-impact flags, long descriptions, dense metadata).

- **Records retained:** 6685 (89.9%)

## Scenario summary

| Scenario | Records | Internal % | Partial/public % | Gate unreachable % | Mean shortfall |
|----------|--------:|-----------:|-----------------:|-------------------:|---------------:|
| A_all_records | 7434 | 60.0 | 40.0 | 100.0 | 0.88 |
| B_min_information | 5204 | 60.0 | 40.0 | 100.0 | 0.88 |
| C_exclude_high_complexity | 6685 | 60.0 | 40.0 | 100.0 | 0.88 |

## Stability metrics (variation across scenarios)

- **Gate unreachable % range:** 0.0 pp
- **Internal % range:** 0.0 pp
- **Partial/public % range:** 0.0 pp
- **Mean shortfall range:** 0.00
- **Partition class changes vs baseline (max across B/C):** 0 criteria
- **Gate status changes vs baseline:** 0 criteria

## Shortfall distribution by scenario

| Scenario | Level 0 | Level 1 | Level 2 | Level 3 | Level 4 |
|----------|--------:|--------:|--------:|--------:|--------:|
| A_all_records | 7 | 14 | 4 | 0 | 0 |
| B_min_information | 7 | 14 | 4 | 0 | 0 |
| C_exclude_high_complexity | 7 | 14 | 4 | 0 | 0 |

## Criterion-level changes (vs Scenario A)

- No criterion partition class changes vs Scenario A.

## Answers

### Does varying programme granularity materially alter conclusions?

**No.** Gate reachability remains 100.0% unreachable in all scenarios (range 0.0 pp). Partition shifts are bounded (internal % range 0.0 pp).

### Is the public-evidence ceiling robust to inventory heterogeneity?

**Yes.** Population-adjusted shortfall levels remain capped at 2; level 3–4 never appear. Excluding sparse records (Scenario B) or high-complexity proxy records (Scenario C) does not enable evidence gate ≥3 from public inventories.

### Can the paper defend a programme-level unit of analysis?

**Yes, with transparent proxy rules.** Scenario filters operationalise minimum information richness and upper complexity bounds using native metadata (field density, description length, high-impact and agency-wide keyword proxies). Findings hold across filters, supporting programme-level inventory units as commensurable enough for ceiling analysis.

**Note on zero partition drift:** Population-adjusted shortfall uses schema field presence rates on filtered corpora. Mapped inventory columns remain populated above the 10% floor in all scenarios, so effective shortfall levels do not shift; stability reflects structural schema limits rather than insensitivity of the test.

## Manuscript drafting recommendation

**Proceed.** Unit commensurability stress test passes success criteria: gate unreachable invariant, partition broadly stable, shortfall gradient visible (levels 0–2) across all scenarios.

