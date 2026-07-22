# Supplement H — Repository structure

## Purpose

Orient readers to the **software repository layout**, distinguishing the **active Disclosure Functions v1 surface** from **historical Governance Readiness Benchmark (v0.1)** materials retained for provenance.

## Inputs

| Input | Role |
|-------|------|
| Root `README.md` | Public architecture and non-claims |
| `docs/releases/public_positioning_v0.2.0.md` | Frozen public positioning |
| Tree under repository root | As shipped in the cited version |

## Outputs

This supplement is navigational. It does not generate data products.

### Table H1 — Top-level roles

| Path | Role (active paper path) |
|------|---------------------------|
| `localgovbench_measurement_validation/affordance/` | **ACTIVE** DF v1 specification, coding, experiments, pilot launch |
| `localgovbench_measurement_validation/pilot_public_satisfiability/` | Corpus host + earlier public-satisfiability pilot tooling (precursor; not DF coding results) |
| `scripts/build_affordance_*.py`, `run_affordance_experiment_pipeline.py`, `validate_pilot_packet.py`, `dry_run_pilot_round_01.py` | **ACTIVE** CLIs |
| `docs/supplements/` | This supplementary package |
| `docs/releases/` | v0.2.0 release / positioning documentation |
| `localgovbench/` (Python package) | Installable package; includes retained v0.1/GRB modules |
| `docs/*.md` (most files), `validation/`, `examples/`, `data/benchmark/` | **LEGACY — v0.1.0** (labelled in-repo) |
| `CITATION.cff`, `.zenodo.json`, `pyproject.toml`, `CHANGELOG.md` | Release metadata |
| `paper_data_policy/` | Manuscript scaffold notes (not a results release) |

### Table H2 — Affordance subtree (active)

```text
affordance/
  config/           # normative YAML/CSV (functions, candidates, rules)
  locks/            # corpus lock
  outputs/          # schema inventory
  coding/           # codebook, templates, pilot_round_01, adjudication
  experiments/      # Phase 3 pipeline
  tests/            # Phase 1 tests
```

## Figures

None beyond the textual tree above.

## Limitations

1. Historical GRB scripts and reports remain executable; **do not** treat them as current DF outputs.  
2. Nested naming (`localgovbench` repo vs `localgovbench` package) can confuse path instructions — commands assume **repository root**.  
3. Some mid-tree READMEs still use precursor “shortfall/ceiling” language; prefer root README + `affordance/README.md` + these supplements for the active construct.

## Cross references

| Topic | See |
|-------|-----|
| Master supplement index | [README.md](README.md) |
| Citation | [Supplement I](I_software_citation.md) |
| Versions | [Supplement J](J_version_history.md) |
| Root architecture | `README.md` § “Current repository architecture” |
| Affordance package | `affordance/README.md` |
