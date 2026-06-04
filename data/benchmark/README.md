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

Outputs: `results/model_benchmark.csv`, `reports/model_benchmark.md`.
