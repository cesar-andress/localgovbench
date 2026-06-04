# GRB synthetic validation profiles

**Governance Readiness Benchmark (GRB)** — 54 indicators, 6 dimensions.

| File | Profile |
|------|---------|
| `low_readiness_municipality.yaml` | Low maturity (D2/D4 at 0) |
| `medium_readiness_municipality.yaml` | Medium maturity (D2/D4 at 2) |
| `high_readiness_municipality.yaml` | High maturity with evidence references |

All files are **synthetic** (`metadata.synthetic: true`).

Run:

```bash
python scripts/run_grb_assessment.py examples/grb/high_readiness_municipality.yaml
```
