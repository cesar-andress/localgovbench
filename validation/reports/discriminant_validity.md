# Discriminant Validity Report (Synthetic Cases)

> Demonstrates that LocalGovBench v0.1 scoring **differentiates** governance maturity profiles.

| Case | Overall (0–4) | Readiness | Band | Expected band | Match |
|------|---------------|-----------|------|---------------|-------|
| `municipality_compliance_gap` | 2.56 | 64.0 | Substantially ready | Substantially ready | True |
| `municipality_high_readiness` | 3.64 | 91.0 | Advanced readiness | Advanced readiness | True |
| `municipality_low_readiness` | 0.2 | 5.0 | Not ready | Not ready | True |
| `municipality_medium_readiness` | 2.0 | 50.0 | Substantially ready | Substantially ready | True |
| `municipality_sovereign_ready` | 3.88 | 97.0 | Advanced readiness | Advanced readiness | True |

## Verification

All discriminant ordering checks **passed**.

- low < medium < high ≤ sovereign_ready
- compliance_gap < high (documentation without oversight depth)

---
*Synthetic data — not empirical validation.*