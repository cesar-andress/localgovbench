# LocalGovBench LLM evidence extraction benchmark

> **GENERATION MODE: MOCK (testing only)** — Deterministic pseudo-extractions without Ollama. **Do not report these metrics as empirical model comparison results.**

> Compares local **Ollama** models on GRB evidence extraction tasks with synthetic gold labels.

**Generation mode:** `mock` (this file: `model_benchmark_mock.md`)
**Results CSV:** `results/model_benchmark_mock.csv`
**Tasks:** `data/benchmark/evidence_extraction_tasks.json`

## Models

| Model | Evidence precision | Quote validity | Hallucination rate | Insufficient detection | Mean latency (s) | P95 latency (s) | Memory (MiB) | Status |
|-------|-------------------:|---------------:|-------------------:|-----------------------:|-----------------:|----------------:|-------------:|--------|
| `llama3.1:8b` | 0.8000 | 0.7273 | 0.2000 | 1.0000 | 0.074 | 0.096 | — | ok |
| `qwen2.5:7b` | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.071 | 0.095 | — | ok |
| `mistral:7b` | 0.8667 | 0.8182 | 0.1333 | 1.0000 | 0.079 | 0.098 | — | ok |
| `gemma2:9b` | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.080 | 0.100 | — | ok |
| `phi3` | 1.0000 | 1.0000 | 0.0000 | 1.0000 | 0.082 | 0.100 | — | ok |

## Metric definitions

| Metric | Definition |
|--------|------------|
| Evidence precision | Share of tasks where positive/negative evidence claims align with gold labels and valid quotes |
| Quote validity | Valid verbatim quotes / quotes emitted when claiming evidence |
| Hallucinated evidence rate | Tasks with non-verbatim quotes among all tasks |
| Insufficient evidence detection | Recall of gold insufficient tasks flagged via warning or low confidence |
| Latency | Wall-clock seconds per extraction (mean and P95) |
| Memory footprint | Ollama reported VRAM (`/api/ps`) after model run, MiB |

## Reproduce

Live (Ollama required):

```bash
ollama serve
ollama pull llama3.1:8b
python scripts/run_llm_model_benchmark.py
# writes results/model_benchmark_live.csv and reports/model_benchmark_live.md
```

Mock (testing only, no Ollama):

```bash
python scripts/run_llm_model_benchmark.py --mock
# writes results/model_benchmark_mock.csv and reports/model_benchmark_mock.md
```
