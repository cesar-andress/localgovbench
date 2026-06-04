# Synthetic benchmark cases (discriminant validity)

| File | Profile |
|------|---------|
| `municipality_low_readiness.yaml` | Not ready |
| `municipality_medium_readiness.yaml` | Substantially ready |
| `municipality_high_readiness.yaml` | Advanced readiness |
| `municipality_sovereign_ready.yaml` | Advanced readiness (sovereignty-strong) |
| `municipality_compliance_gap.yaml` | Documentation-heavy, weak oversight |

Each case includes `governance_evidence`, `responses` (25 criteria), and `expected_outcome`.

```bash
python scripts/run_discriminant_validity.py
```
