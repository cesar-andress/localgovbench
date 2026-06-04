# Reproducibility guide — LocalGovBench v0.1.0

Reproduce the computational artefact from a clean environment. Use the **Git tag** and **Zenodo version** cited in your paper.

**Requirements:** Python **3.11+**, Git. Optional: [Ollama](https://ollama.com) for evidence extraction prototype.

---

## 1. Install dependencies

```bash
git clone https://github.com/cesar-andress/localgovbench.git
cd localgovbench
git checkout v0.1.0

python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## 2. Run tests

```bash
pytest -m "not integration"
```

Or simply `pytest` (integration tests are excluded by default in `pyproject.toml`).

Expected: all unit tests pass with **no Ollama server, network, or downloaded model** required.

Optional live Ollama checks (local server + model):

```bash
ollama serve
OLLAMA_INTEGRATION=1 pytest -m integration
```

---

## 3. Validate repository paths

```bash
python scripts/validate_repository.py
```

Expected: `Repository structure validation passed.`

### Construct traceability

```bash
python scripts/validate_traceability.py
```

Expected: `Status: PASS` and updated `data/traceability/indicator_mapping.csv`, `reports/traceability_report.md`.

---

## 4. Run LocalGovBench v0.1 example assessment

```bash
python scripts/run_example_assessment.py
```

Uses synthetic `examples/example_assessment.yaml`.

---

## 5. Run LocalGovBench validation workflows

### Content validity (example panel)

```bash
python scripts/run_content_validity_analysis.py \
  --input validation/content_validity/indicator_relevance_survey_results.example.yaml
```

### Inter-rater reliability (v0.1 criteria, synthetic ratings)

```bash
python scripts/run_inter_rater_analysis.py
```

### Discriminant validity (synthetic benchmark cases)

```bash
python scripts/run_discriminant_validity.py
```

### Integrated validation report

```bash
python scripts/generate_validation_report.py
```

---

## 6. Run GRB assessment

Assess one bundled synthetic municipality profile:

```bash
python scripts/run_grb_assessment.py examples/grb/high_readiness_municipality.yaml
```

Other examples: `examples/grb/low_readiness_municipality.yaml`, `medium_readiness_municipality.yaml`.

---

## 7. Run GRB sensitivity analysis

```bash
python scripts/run_grb_sensitivity_analysis.py
```

**Outputs:** `results/grb_sensitivity_analysis.csv`, `reports/grb_sensitivity_analysis.md`

---

## 8. Run GRB inter-rater reliability

Uses bundled synthetic assessor files in `examples/grb/inter_rater/`:

```bash
python scripts/run_inter_rater_reliability.py
```

**Outputs:** `results/inter_rater_reliability.csv`, `reports/inter_rater_reliability.md`

---

## 9. Run legacy GRB sensitivity script (100-profile experiment)

```bash
python scripts/run_sensitivity_analysis.py
```

**Output:** `results/sensitivity_analysis.csv`, `reports/sensitivity_analysis.md`

---

## 10. Run end-to-end GRB assessment workflow

Full step-by-step guide: **[demo_walkthrough.md](demo_walkthrough.md)** (template, demo scores, compute, optional Ollama).

## 11. Run Ollama evidence extraction locally (optional)

Requires Ollama running with a pulled model (e.g. `llama3.1:8b`).

```bash
ollama serve
ollama pull llama3.1:8b
python scripts/run_ollama_evidence_extraction.py
```

See `prompts/evidence_extraction.md`. The prototype proposes **candidate evidence only** — humans assign scores.

## 12. Benchmark local LLM models (optional)

Compare Ollama models on gold-labelled synthetic evidence extraction tasks:

```bash
ollama serve
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
# ... mistral:7b, gemma2:9b, phi3
python scripts/run_llm_model_benchmark.py
```

**Outputs (live):** `results/model_benchmark_live.csv`, `reports/model_benchmark_live.md`

Deterministic mock run (testing only, no Ollama): `python scripts/run_llm_model_benchmark.py --mock`  
→ `results/model_benchmark_mock.csv`, `reports/model_benchmark_mock.md` (not for empirical reporting)

---

## Verification summary

| Step | Command | Pass criterion |
|------|---------|----------------|
| Tests | `pytest` | Exit code 0 |
| Structure | `python scripts/validate_repository.py` | Exit code 0 |
| GRB sensitivity | `python scripts/run_grb_sensitivity_analysis.py` | CSV and MD created |
| GRB IRR | `python scripts/run_inter_rater_reliability.py` | CSV and MD created |
| LLM benchmark (mock) | `python scripts/run_llm_model_benchmark.py --mock` | `*_mock.csv` / `*_mock.md` created |

---

## Citation and archive integrity

1. Cite [CITATION.cff](../CITATION.cff) and Zenodo DOI [10.5281/zenodo.20543779](https://doi.org/10.5281/zenodo.20543779) (see [citation.md](citation.md)).
2. Record the Git tag (`v0.1.0`) and archive SHA-256 from [release_v0_1_checklist.md](release_v0_1_checklist.md).

---

*LocalGovBench v0.1.0 reproducibility guide*
