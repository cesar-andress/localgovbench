> **Status: LEGACY — v0.1.0**  
> Retained for provenance of the historical Governance Readiness Benchmark / v0.1 instrument.  
> **Do not use this document as the current analytical specification.**  
> **Active framework:** Disclosure Functions v1 — see [`localgovbench_measurement_validation/affordance/README.md`](../localgovbench_measurement_validation/affordance/README.md) and the root [`README.md`](../README.md).

# Exploratory experiment: live LLM evidence extraction benchmark

**Status:** Exploratory pilot (not instrument validation)  
**Generation mode:** Live Ollama inference  
**Results:** `results/model_benchmark_live.csv`, `reports/model_benchmark_live.md`  
**Task set:** `data/benchmark/evidence_extraction_tasks.json` (15 synthetic gold-labelled tasks per model)

---

## Objective

To compare **local Ollama models** on an auxiliary evidence-extraction workflow for the Governance Readiness Benchmark (GRB). The experiment asks whether different open-weight models can propose **candidate evidence** (summary + verbatim quote) for GRB indicators when given synthetic municipal governance documents.

This pilot supports **workflow prototyping** and reproducibility tooling. It does **not** validate the LocalGovBench v0.1 instrument, GRB scoring formulas, or municipal field readiness.

**Role boundary:** LLMs extract **candidate evidence only**. They must **not** assign GRB maturity scores (0–4) or readiness values; human assessors retain scoring authority (`localgovbench/llm/evidence_extraction.py`, `prompts/evidence_extraction.md`).

---

## Models evaluated

| Ollama model | Parameters (nominal) |
|--------------|----------------------|
| `llama3.1:8b` | 8B |
| `qwen2.5:7b` | 7B |
| `mistral:7b` | 7B |
| `gemma2:9b` | 9B |
| `phi3` | ~3.8B |

Models were run via `scripts/run_llm_model_benchmark.py` against a local Ollama server. Pull tags before running: `ollama pull <model>`.

---

## Task set description

- **n = 15 tasks per model** (same task list for every model).
- Tasks pair one **synthetic** governance document with one **GRB indicator** id.
- Gold labels (`gold_has_evidence`, `gold_keywords`, `gold_expect_insufficient`) are **reviewer-defined** for pipeline testing—not municipal field coding.
- Documents are fictional samples under `data/synthetic/` and `data/synthetic/workflow_demo/documents/`.
- Tasks include both **positive** (evidence expected) and **negative** (insufficient / wrong-document) cases.

The benchmark measures agreement with these **synthetic gold labels**, not real-world municipal performance.

---

## Metrics

| Metric | Meaning |
|--------|---------|
| **Evidence precision** | Share of tasks where the model’s evidence claim aligns with gold (presence/absence + valid quote + keyword overlap when gold expects evidence) |
| **Quote validity** | Fraction of emitted quotes that are verbatim substrings of the source document |
| **Hallucinated evidence rate** | Share of all tasks where the model claims evidence but the quote is not verbatim in the document |
| **Insufficient evidence detection** | Recall on gold “insufficient” tasks (warning or low confidence with empty quote) |
| **Mean / P95 latency** | Wall-clock seconds per extraction |
| **Memory footprint** | Ollama-reported VRAM (MiB) from `/api/ps` after the model run |

Definitions are implemented in `localgovbench/llm/benchmark_metrics.py`.

---

## Live results (bundled run)

> **Exploratory only.** Small synthetic task set; single-machine run. Do not generalise to production municipal deployment without field replication.

| Model | Evidence precision | Quote validity | Hallucination rate | Insufficient detection | Mean latency (s) | P95 latency (s) | Memory (MiB) |
|-------|-------------------:|---------------:|-------------------:|-----------------------:|-----------------:|----------------:|-------------:|
| `gemma2:9b` | **0.4000** | 0.7857 | 0.2000 | 0.2500 | 3.274 | 4.414 | 7036.2 |
| `qwen2.5:7b` | 0.2667 | 0.2308 | 0.6667 | 0.7500 | 1.661 | 2.114 | 4696.1 |
| `mistral:7b` | 0.2000 | 0.2667 | 0.7333 | 0.5000 | 1.226 | 1.624 | 4905.5 |
| `llama3.1:8b` | 0.1333 | **0.8000** | 0.2000 | 0.2500 | 1.620 | 2.007 | 5211.5 |
| `phi3` | 0.0667 | 0.3333 | 0.6667 | 0.5000 | **0.975** | **1.470** | **3813.8** |

Source: `results/model_benchmark_live.csv` (mode `live`, 15/15 successful extractions per model).

---

## Result interpretation

- **Gemma2:9b** showed the **highest evidence precision** (0.40) in this run, with moderate hallucination (0.20) and strong quote validity (0.79) when it claimed evidence.
- **Llama3.1:8b** showed **high quote validity** (0.80) but **lower evidence precision** (0.13), suggesting quotes were often verbatim yet misaligned with gold keyword/indicator expectations.
- **Hallucination rates** (0.20–0.73 across models) indicate that **human verification of quotes** remains necessary before any evidence enters an assessor log.
- **Latency and memory** vary materially: **phi3** was fastest and lightest on VRAM; **gemma2:9b** was slowest and used the most memory, trading speed for somewhat better precision on this small set.

Rankings may change with prompt revisions, temperature, hardware, or a larger task battery.

---

## Limitations

| Limitation | Implication |
|------------|-------------|
| Synthetic gold labels only | No claim about real municipalities or legal compliance |
| n = 15 tasks | High variance; not powered for definitive model ranking |
| Exploratory design | Results inform tooling, not GRB construct validity |
| Not GRB instrument validation | Sensitivity/IRR pilots are separate experiments |
| JSON-structured Ollama output | Parser failures and format drift affect scores |
| Single host / run | No multi-seed or cross-site replication recorded here |
| English synthetic docs | May not reflect multilingual municipal corpora |

**Mock outputs** (`model_benchmark_mock.*`) are for CI and pipeline tests only—never cite them as empirical results.

---

## What this benchmark does not do

- Does **not** validate the LocalGovBench v0.1 checklist or GRB readiness formula.
- Does **not** certify EU AI Act or GDPR compliance.
- Does **not** replace human assessors or inter-rater studies.
- Does **not** assign readiness scores or maturity levels (forbidden in the extraction prompt and parser).

---

## Reproducibility commands

```bash
# From repository root; Python 3.11+
pip install -e ".[dev]"

# Live benchmark (requires Ollama + pulled models)
ollama serve
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
ollama pull mistral:7b
ollama pull gemma2:9b
ollama pull phi3

python scripts/run_llm_model_benchmark.py
# → results/model_benchmark_live.csv
# → reports/model_benchmark_live.md

# Pipeline test only (no Ollama)
python scripts/run_llm_model_benchmark.py --mock
# → results/model_benchmark_mock.csv (not for empirical reporting)
```

Verify structure and unit tests:

```bash
pytest -m "not integration"
python scripts/validate_repository.py
```

See also: [data/benchmark/README.md](../data/benchmark/README.md), [reproducibility.md](reproducibility.md).

---

*LocalGovBench v0.1.0 — exploratory LLM evidence extraction benchmark documentation*
