> **Status: LEGACY — v0.1.0**  
> Retained for provenance of historical GRB / Ollama evidence-extraction materials.  
> **Do not use this material as the current analytical specification.**  
> **Active framework:** [`../../localgovbench_measurement_validation/affordance/README.md`](../../localgovbench_measurement_validation/affordance/README.md).

# Evidence extraction benchmark tasks

Gold-labelled **synthetic** tasks for comparing local Ollama models on GRB evidence extraction.

| File | Purpose |
|------|---------|
| `evidence_extraction_tasks.json` | Document + indicator pairs with reviewer-defined gold labels |

Run the benchmark:

```bash
ollama serve
ollama pull llama3.1:8b   # repeat for each model under test
python scripts/run_llm_model_benchmark.py
```

Deterministic mock run (no Ollama):

```bash
python scripts/run_llm_model_benchmark.py --mock
```

| Mode | CSV | Report |
|------|-----|--------|
| Mock (`--mock`) | `results/model_benchmark_mock.csv` | `reports/model_benchmark_mock.md` |
| Live (Ollama) | `results/model_benchmark_live.csv` | `reports/model_benchmark_live.md` |

**Mock results are for pipeline testing only** — do not cite them as empirical model comparisons.

Do not use deprecated `results/model_benchmark.csv` or `reports/model_benchmark.md`; the CLI removes them when run.

## Repeated benchmark (N runs per model)

Randomizes task order on each repetition and aggregates mean, standard deviation, and 95% CI across runs:

```bash
python scripts/run_llm_model_benchmark_repeated.py --mock --repetitions 3
python scripts/run_llm_model_benchmark_repeated.py --repetitions 10
```

| Output | Path |
|--------|------|
| Summary CSV | `results/model_benchmark_repeated.csv` |
| Report | `reports/model_benchmark_repeated.md` |
| Individual runs | `results/repeated_runs/<model>/run_XXX.json` |
