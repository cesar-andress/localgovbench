# Readiness Weighting Robustness (Synthetic Benchmark Cases)

> Evaluates whether **v0.1 readiness rankings** over five synthetic municipality profiles are stable when dimension weights depart from the default uniform scheme.

**Instrument:** Local AI Governance Framework v0.1 (`compute_maturity_score`).
**Baseline:** `uniform` (weight 1.0 per dimension).

## Predefined weight schemes

| Scheme | Emphasis |
|--------|----------|
| `uniform` | Equal weights (baseline) |
| `oversight_heavy` | Operational ×3, organizational ×2 |
| `data_governance_heavy` | Legal/regulatory ×3 |
| `sovereignty_heavy` | Strategic sovereignty ×3, technical security ×2 |
| `random` | 1000 Dirichlet samples (seed 42) |

## Case scores and ranks (uniform baseline)

| Case | Maturity (0–4) | Readiness | Rank |
|------|----------------|-----------|------|
| `municipality_compliance_gap` | 2.56 | 64.0 | 3 |
| `municipality_high_readiness` | 3.64 | 91.0 | 2 |
| `municipality_low_readiness` | 0.2 | 5.0 | 5 |
| `municipality_medium_readiness` | 2.0 | 50.0 | 4 |
| `municipality_sovereign_ready` | 3.88 | 97.0 | 1 |

## Rank correlation vs uniform

| Alternate | Spearman ρ | Kendall τ | Cases re-ranked | Total rank shift |
|-----------|------------|-----------|-----------------|------------------|
| `oversight_heavy` | 1.0000 | 1.0000 | 0 | 0 |
| `data_governance_heavy` | 1.0000 | 1.0000 | 0 | 0 |
| `sovereignty_heavy` | 1.0000 | 1.0000 | 0 | 0 |

### Per-case rank shifts (predefined alternates)

- **oversight_heavy:** `municipality_compliance_gap`: +0, `municipality_high_readiness`: +0, `municipality_low_readiness`: +0, `municipality_medium_readiness`: +0, `municipality_sovereign_ready`: +0
- **data_governance_heavy:** `municipality_compliance_gap`: +0, `municipality_high_readiness`: +0, `municipality_low_readiness`: +0, `municipality_medium_readiness`: +0, `municipality_sovereign_ready`: +0
- **sovereignty_heavy:** `municipality_compliance_gap`: +0, `municipality_high_readiness`: +0, `municipality_low_readiness`: +0, `municipality_medium_readiness`: +0, `municipality_sovereign_ready`: +0

## Random weight ensembles

- Samples: **1000**
- Spearman ρ — mean 0.9850, min 0.9000, std 0.0357
- Kendall τ — mean 0.9700, min 0.8000, std 0.0715
- Fraction with perfect Spearman (ρ = 1): 85.0%
- Mean cases re-ranked vs uniform: 0.30

---
*Synthetic benchmark cases — structural robustness only; not municipal validation.*