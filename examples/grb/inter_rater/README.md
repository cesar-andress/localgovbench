# GRB inter-rater reliability pilot

Synthetic IRR materials for the frozen **54-indicator GRB** experiment.

| File | Purpose |
|------|---------|
| `case_alpha_evidence_pack.md` | Low oversight / medium accountability scenario |
| `case_beta_evidence_pack.md` | Balanced managed maturity scenario |
| `case_gamma_evidence_pack.md` | Compliance gap (strong D4, weak D2) |
| `assessor_1_scores.yaml` | Reference coder (synthetic) |
| `assessor_2_scores.yaml` | Second coder with deliberate disagreements |
| `assessor_3_scores.yaml` | Third coder with deliberate disagreements |

Run analysis:

```bash
python scripts/run_inter_rater_reliability.py
```

See [docs/inter_rater_reliability_protocol.md](../../../docs/inter_rater_reliability_protocol.md).
