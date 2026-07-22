# Supplement G — Reproducibility

## Purpose

Provide a **reproducibility checklist** for the Disclosure Functions v1 software path: environment, builders, tests, locks/checksums, and verification of frozen artefacts. Legacy GRB reproduction is out of scope here (see historical DOI / tag `v0.1.0`).

## Inputs

| Requirement | Notes |
|-------------|-------|
| Python | `>=3.11` (docs commonly use `python3.12`) |
| Repository | [https://github.com/cesar-andress/localgovbench](https://github.com/cesar-andress/localgovbench) |
| Install | `pip install -e ".[dev]"` (includes PyYAML/pytest used by the active path) |
| Corpus bytes | Required to **regenerate** inventory/lock; verify SHA-256 (Supplement A) |
| Cited version | Prefer Git tag / Zenodo DOI / commit hash actually used |

## Outputs

Successful reproduction yields:

- validated specification artefacts;  
- regenerable coding templates (bit-stable given frozen Phase 1 inputs);  
- passing automated tests for affordance / coding / experiments;  
- optional experiment outputs only after real completed coding is supplied.

### Table G1 — Core reproducibility commands (active path)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Phase 1 — specification (regenerate locks/inventory only with corpus present)
python3.12 scripts/build_affordance_specification.py
python3.12 scripts/build_affordance_specification.py --validate-only

# Phase 2 — coding instruments
python3.12 scripts/build_affordance_coding_layer.py

# Tests (Phases 1–3)
python3.12 -m pytest localgovbench_measurement_validation/affordance/tests \
  localgovbench_measurement_validation/affordance/coding/tests \
  localgovbench_measurement_validation/affordance/experiments/tests -q

# Pilot blank packets (operational)
python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate
python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv \
  --mode pre

# Technical dry run only (non-substantive fixtures)
python3.12 scripts/dry_run_pilot_round_01.py
```

Structure check (broader repository; historically GRB-oriented):

```bash
python3.12 scripts/validate_repository.py
```

### Integrity anchors

| Anchor | Location |
|--------|----------|
| Corpus SHA-256 | `affordance/locks/corpus_lock_v1.json` / `.md` |
| Pilot reference manifest | `affordance/coding/pilot_round_01/locked_reference/pilot_reference_manifest_v1.json` |
| Pilot checksums | `affordance/coding/pilot_round_01/checksums/SHA256SUMS` |
| Software version metadata | `pyproject.toml`, `CITATION.cff` |

## Figures

None.

## Limitations

1. Without the corpus CSV, **regeneration** of lock/inventory cannot be demonstrated even if frozen outputs are present in git.  
2. `pip install` without `[dev]` may omit runtime YAML dependency (packaging gap).  
3. Runtime `localgovbench.__version__` may disagree with `pyproject.toml` on some commits — trust `pyproject.toml` / `CITATION.cff` / Git describe for citation until aligned.  
4. Legacy `docs/reproducibility.md` targets v0.1.0 GRB; use this supplement for the active path.  
5. Checksum files may mix absolute paths; prefer verifying hashes of relative artefacts from the repository root.

## Cross references

| Topic | See |
|-------|-----|
| Corpus verification | [Supplement A](A_corpus.md) |
| Pipeline | [Supplement F](F_experimental_pipeline.md) |
| Citation | [Supplement I](I_software_citation.md) |
| Versions | [Supplement J](J_version_history.md) |
| Root README reproducibility section | `README.md` |
| Affordance README | `affordance/README.md` |
