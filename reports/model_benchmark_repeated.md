# LocalGovBench repeated LLM evidence extraction benchmark

> **MOCK repeated benchmark (testing only)** — deterministic pseudo-extractions. Do not cite as empirical Ollama comparison.

**Repetitions per model:** 2
**Base seed:** 42 (run *i* uses seed = base_seed + i)
**Tasks:** `data/benchmark/evidence_extraction_tasks.json`
**Summary CSV:** `model_benchmark_repeated.csv`
**Individual runs:** `results/repeated_runs/<model>/run_XXX.json`

## Summary (mean ± std across repetitions)

95% confidence intervals (CI) apply to the **mean of per-run metrics** (Student-t, df = N−1).

| Model | Prec. mean±std | Prec. 95% CI | Halluc. mean±std | Latency mean±std (s) | Status |
|-------|----------------|--------------|------------------|----------------------|--------|
| `llama3.1:8b` | 0.8±0.0 | [0.8, 0.8] | 0.2±0.0 | 0.074±0.0 | ok |
| `qwen2.5:7b` | 1.0±0.0 | [1.0, 1.0] | 0.0±0.0 | 0.071±0.0 | ok |
| `mistral:7b` | 0.8667±0.0 | [0.8667, 0.8667] | 0.1333±0.0 | 0.079±0.0 | ok |
| `gemma2:9b` | 1.0±0.0 | [1.0, 1.0] | 0.0±0.0 | 0.08±0.0 | ok |
| `phi3` | 1.0±0.0 | [1.0, 1.0] | 0.0±0.0 | 0.082±0.0 | ok |

## Full metrics

See `results/model_benchmark_repeated.csv` for all means, standard deviations, and CI bounds:

- `evidence_precision`
- `quote_validity_rate`
- `hallucinated_evidence_rate`
- `insufficient_evidence_detection_rate`
- `mean_latency_seconds`

## Reproduce

```bash
python scripts/run_llm_model_benchmark_repeated.py --mock --repetitions 3
python scripts/run_llm_model_benchmark_repeated.py --repetitions 10
```

Mode: `mock`
