# GRB Sensitivity Analysis

**GRB version:** 0.1-experiment  
**Profiles:** 100 synthetic assessments  
**Baseline:** dimensions D1, D3, D5 at maturity 3 (readiness raw ≈ 75.0)  
**Safeguard G1:** cap at 60.0 when D2 or D4 dimension score < 2.0  

## Design

| Scenario | Profiles | Varied dimension | Fixed dimensions |
|----------|----------|------------------|------------------|
| `d2_sweep` | 34 | D2 Human Oversight (0–4) | D1, D3–D6 at 3 |
| `d4_sweep` | 33 | D4 Data Legitimacy (0–4) | D1–D3, D5–D6 at 3 |
| `d6_sweep` | 33 | D6 Strategic Sovereignty (0–4) | D1–D5 at 3 |

## Table 1 — D2 Human Oversight vs readiness

| D2 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |
|----------------|---|------------------------|----------------------|---------------------------|
| 0 | 7 | 60.0 | 62.5 | 7 |
| 1 | 7 | 60.0 | 66.67 | 7 |
| 2 | 7 | 70.83 | 70.83 | 0 |
| 3 | 7 | 75.0 | 75.0 | 0 |
| 4 | 6 | 79.17 | 79.17 | 0 |

## Table 2 — D4 Data Legitimacy vs readiness

| D4 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |
|----------------|---|------------------------|----------------------|---------------------------|
| 0 | 7 | 60.0 | 62.5 | 7 |
| 1 | 7 | 60.0 | 66.67 | 7 |
| 2 | 7 | 70.83 | 70.83 | 0 |
| 3 | 6 | 75.0 | 75.0 | 0 |
| 4 | 6 | 79.17 | 79.17 | 0 |

## Table 3 — D6 Strategic Sovereignty vs readiness

| D6 input level | N | Mean readiness (final) | Mean readiness (raw) | Safeguard applied (count) |
|----------------|---|------------------------|----------------------|---------------------------|
| 0 | 7 | 62.5 | 62.5 | 0 |
| 1 | 7 | 66.67 | 66.67 | 0 |
| 2 | 7 | 70.83 | 70.83 | 0 |
| 3 | 6 | 75.0 | 75.0 | 0 |
| 4 | 6 | 79.17 | 79.17 | 0 |

## Table 4 — Expected marginal effect per dimension point

Each dimension contributes 9 of 54 indicators (weight 1/6 in overall maturity).

| Dimension | Δ maturity per +1 level | Δ readiness (raw) per +1 level |
|-----------|---------------------------|----------------------------------|
| D2, D4, D6 (non-safeguard) | ≈ 1/6 ≈ 0.167 | ≈ 4.17 |
| D2 or D4 with safeguard binding | ≤ 4.17 (cap may bind) | ≤ 4.17 |

## Interpretation — does the model behave as expected?

- **D2 decrease:** Mean readiness **decreases monotonically** as Human Oversight input level falls (Table 1). Consistent with equal-weight aggregation.
- **D4 decrease:** Mean readiness **decreases monotonically** as Data Legitimacy falls (Table 2). D4 is a safeguard dimension; scores 0–1 trigger G1 when raw > 60.
- **D6 increase:** Mean readiness **increases monotonically** as Strategic Sovereignty rises (Table 3). No safeguard applies to D6; effect is linear in raw score.
- **Safeguard G1:** Applied in 14 D2-sweep profile-groups at level < 2 and 14 D4-sweep groups where raw readiness exceeded 60.0.
- **Overall:** The scoring model responds **directionally as expected** to one-dimensional shifts in D2, D4, and D6 under uniform indicator scoring. Safeguard capping introduces a **ceiling** on final readiness when D2 or D4 are weak but other dimensions are strong — by design for responsible-deployment signalling.
- **Limitation:** This experiment uses **uniform scores within each dimension** and does not vary D1, D3, or D5; it is a structural sensitivity test, not empirical validation.

---
*Synthetic experiment — not field data.*