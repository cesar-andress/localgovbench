# LocalGovBench — Artifact description (v0.1.0)

## Purpose

**LocalGovBench** is an open research software artifact for describing, scoring, and validating **governance practices** around **local and on-premise large language model (LLM)** deployments in **European public sector** organizations.

It supports:

- Structured self-assessment and document coding
- Reproducible scoring on a 0–4 maturity scale
- Scientific validation workflows (content validity, inter-rater reliability, discriminant cases)
- An extended **Governance Readiness Benchmark (GRB)** experiment (54 indicators) for structural testing

The artifact does **not** provide legal compliance certification.

---

## Scope

### LocalGovBench v0.1 (frozen instrument)

- **Five governance dimensions**, **25 criteria**
- Checklist generation, maturity scoring, indicative EU AI Act and GDPR **theme** mappings
- Empirical validation **templates and analysis scripts** (not completed field results)

### GRB experiment (frozen specification)

- **Six dimensions**, **54 indicators**, readiness index and safeguard **G1**
- Synthetic validation: sensitivity analysis, inter-rater reliability pilot
- **Separate** from v0.1 instrument definitions — do not merge scores across instruments

---

## What is included

| Component | Location |
|-----------|----------|
| Core package | `localgovbench/` |
| Framework v0.1 | `localgovbench/framework/` |
| GRB experiment | `localgovbench/grb/` |
| Validation package | `validation/`, `localgovbench/validation/` |
| Documentation | `docs/` |
| Synthetic examples | `examples/`, `examples/grb/` |
| Analysis scripts | `scripts/` |
| Tests | `tests/` |
| Prompts (research instruments) | `prompts/` |
| Data placeholders | `data/raw/`, `data/processed/`, `data/templates/` |
| Citation metadata | `CITATION.cff`, [citation.md](citation.md) (DOI [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779)) |

Bundled assessment outputs under `results/` and `reports/` are **generated** from scripts unless otherwise noted.

---

## What is excluded

- Real municipal benchmark scores or identifiable case materials
- Completed multi-site empirical validation datasets
- Manuscript PDFs, LaTeX sources, or submission packages
- Peer-review correspondence or editorial letters
- API keys, `.env` files, or production integrations
- Legal advice or conformity assessment opinions

---

## Synthetic validation status

The following have been run on **synthetic** inputs in this repository:

| Activity | Status | Output |
|----------|--------|--------|
| GRB sensitivity analysis (≥150 profiles) | Complete (synthetic) | `results/grb_sensitivity_analysis.csv` |
| GRB inter-rater reliability pilot | Complete (synthetic) | `results/inter_rater_reliability.csv` |
| LocalGovBench discriminant cases | Complete (synthetic) | `scripts/run_discriminant_validity.py` |
| Content validity example panel | Template + example YAML only | `validation/content_validity/` |
| IRR pilot (v0.1 criteria) | Synthetic ratings bundled | `validation/ratings/` |

These demonstrate **tooling and structural behaviour**, not generalisation to EU municipalities.

---

## Empirical validation status

| Phase | v0.1 instrument | GRB experiment |
|-------|-----------------|----------------|
| Content validity (expert panel) | **Pending** — templates ready | Not in scope for v0.1 field protocol |
| Inter-rater reliability (field) | **Pending** — κ/α scripts ready | Pilot synthetic only |
| Discriminant validity (field) | **Pending** — synthetic cases only | N/A |
| Multi-municipality deployment | **Pending** | N/A |

**v0.1.0 pre-release:** empirical validation is **not complete**. Do not cite bundled synthetic scores as empirical benchmarks.

---

## Ethical and legal disclaimer

- The instrument is for **research and organisational self-reflection** only.
- Regulatory mappings (`docs/ai_act_mapping.md`, `docs/gdpr_mapping.md`) are **indicative themes**, not legal advice.
- Maturity scores do **not** indicate GDPR or EU AI Act compliance.
- Field studies require ethics approval, lawful basis, and organisational authorisation.
- Do not commit personal data or confidential procurement material to this repository.

---

## Reproducibility instructions

See [reproducibility.md](reproducibility.md) for exact commands.

Minimum verification on a tagged release:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python scripts/validate_repository.py
```

Pre-release checklist: [release_v0_1_checklist.md](release_v0_1_checklist.md).

Zenodo deposit guide: [zenodo_release.md](zenodo_release.md).

**Archived release:** LocalGovBench v0.1.0 — https://doi.org/10.5281/zenodo.20543779

---

*LocalGovBench v0.1.0 — artifact description for GitHub and Zenodo*
