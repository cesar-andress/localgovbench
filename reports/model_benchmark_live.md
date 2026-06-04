# LocalGovBench LLM evidence extraction benchmark

> **GENERATION MODE: LIVE** — Metrics from local Ollama inference on gold-labelled synthetic tasks. Suitable for reporting when models were actually run.

> Compares local **Ollama** models on GRB evidence extraction tasks with synthetic gold labels.

**Generation mode:** `live` (this file: `model_benchmark_live.md`)
**Results CSV:** `results/model_benchmark_live.csv`
**Tasks:** `data/benchmark/evidence_extraction_tasks.json`

## Models

| Model | Evidence precision | Quote validity | Hallucination rate | Insufficient detection | Mean latency (s) | P95 latency (s) | Memory (MiB) | Status |
|-------|-------------------:|---------------:|-------------------:|-----------------------:|-----------------:|----------------:|-------------:|--------|
| `llama3.1:8b` | 0.1333 | 0.8000 | 0.2000 | 0.2500 | 1.620 | 2.007 | 5211.5 | ok |
| `qwen2.5:7b` | 0.2667 | 0.2308 | 0.6667 | 0.7500 | 1.661 | 2.114 | 4696.1 | ok |
| `mistral:7b` | 0.2000 | 0.2667 | 0.7333 | 0.5000 | 1.226 | 1.624 | 4905.5 | ok |
| `gemma2:9b` | 0.4000 | 0.7857 | 0.2000 | 0.2500 | 3.274 | 4.414 | 7036.2 | ok |
| `phi3` | 0.0667 | 0.3333 | 0.6667 | 0.5000 | 0.975 | 1.470 | 3813.8 | ok |

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
