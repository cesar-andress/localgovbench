# Public satisfiability pilot (10-day)

**Framing:** quantify the public-satisfiability **ceiling** of LocalGovBench v0.1 evidence requirements.
**Not measured:** readiness scores, municipality rankings, Paper 2 documentary observability.

## Reproduce

### Pilot (US + Canada)

```bash
cd localgovbench
python3.12 scripts/generate_localgovbench_criteria_config.py
python3.12 scripts/build_pilot_corpus.py
python3.12 scripts/map_inventory_fields_to_criteria.py
python3.12 scripts/analyze_public_satisfiability.py
```

### Validation upgrade (5 sources + robustness)

```bash
cd localgovbench
python3.12 scripts/generate_localgovbench_criteria_config.py
python3.12 scripts/run_validation_upgrade.py
python3.12 scripts/evaluate_detector_reliability.py
```

## Outputs

| Path | Description |
|------|-------------|
| `config/localgovbench_criteria_v0.yaml` | 25 criteria + preliminary satisfiability classes |
| `data/pilot_programme_records.csv` | Normalized programme records (5 sources) |
| `data/source_registry_expanded.csv` | Expanded source registry metadata |
| `outputs/field_criterion_coverage_matrix.csv` | Source × criterion mapping + shortfall 0–4 |
| `outputs/partition_validation_agreement.csv` | Dual-classifier partition agreement |
| `outputs/sensitivity_main_results.csv` | Conservative/liberal sensitivity |
| `outputs/minimum_internal_evidence_set.csv` | Non-public evidence requirements |
| `outputs/detector_reliability_summary.csv` | Hide-field / recover-field metrics |
| `outputs/detector_reliability_by_source.csv` | Source-level detector averages |
| `outputs/criterion_satisfiability_summary.csv` | Criterion-level metrics |
| `outputs/dimension_satisfiability_summary.csv` | Dimension ceilings |
| `outputs/gate_reachability_summary.csv` | Score ≥3 gate reachability |
| `outputs/pilot_go_decision.json` | Automated GO/NO-GO checks |
| `figures/*.png` | Pilot figures (matplotlib) |
| `reports/pilot_public_satisfiability_report.md` | Pilot report |
| `reports/validation_upgrade_report.md` | Validation upgrade report |

## Paper 2 firewall

No Paper 2 corpus, no vendor stewardship claim, no documentary observability, no DAA.
