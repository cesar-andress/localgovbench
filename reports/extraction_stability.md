# Extraction stability benchmark

> **MOCK stability benchmark (testing only)** — run-indexed pseudo-variation. Do not cite as empirical Ollama stability.

Evaluates whether the **same model** returns **similar evidence** when the identical task is executed repeatedly.

**Runs per task:** 20
**Base seed (mock):** 42
**Tasks:** `data/benchmark/evidence_extraction_tasks.json`
**Results CSV:** `extraction_stability.csv`
**Per-task JSON:** `results/extraction_stability_runs/<model>/<task_id>.json`

## Stability metrics

| Metric | Definition |
|--------|------------|
| Quote stability | Share of runs whose normalized `quoted_text_span` matches the modal quote |
| Evidence stability | Share of runs whose normalized `candidate_evidence` matches the modal summary |
| Confidence stability | Share of runs whose `confidence_level` matches the modal level |

Values range 0–1 (1 = identical outputs every run). `unique_*` counts distinct normalized values.

## Model summary

| Model | Quote | Evidence | Confidence | Overall | Interpretation | Status |
|-------|------:|---------:|-----------:|--------:|----------------|--------|
| `llama3.1:8b` | 0.8 | 0.7467 | 0.7567 | 0.7678 | moderately stable | ok |
| `qwen2.5:7b` | 0.8633 | 0.8333 | 0.8467 | 0.8478 | moderately stable | ok |
| `mistral:7b` | 0.8233 | 0.7933 | 0.8533 | 0.8233 | moderately stable | ok |
| `gemma2:9b` | 0.81 | 0.7733 | 0.8 | 0.7944 | moderately stable | ok |
| `phi3` | 0.75 | 0.69 | 0.7433 | 0.7278 | moderately stable | ok |

## Variability interpretation

Mock mode injects controlled cross-run variation using a deterministic per-model **output_stability** rate. Models with lower configured stability produce more alternate quotes, evidence strings, and confidence labels — mirroring operational inconsistency without calling Ollama.

### Reading guide

- **Highly stable (≥0.9):** reviewers can expect near-identical candidate evidence across reruns.
- **Moderately stable (0.7–0.9):** minor wording drift; verify quotes before scoring.
- **Variable (0.5–0.7):** substantive disagreement; do not auto-accept evidence.
- **Highly variable (<0.5):** unsuitable for unattended extraction pipelines.

Confidence stability below quote stability often means the model hedges with alternating `low` / `medium` / `high` labels while paraphrasing similar content.

## Task-level detail

See `results/extraction_stability.csv` (`record_type=task_summary`) for per-task stability.

## Reproduce

```bash
python scripts/run_extraction_stability.py --mock
python scripts/run_extraction_stability.py  # requires Ollama
```

Mode: `mock`

### Least stable tasks (sample)

- `gemma2:9b` / `data_gov_d3_miss`: quote=0.5, evidence=0.5, confidence=0.6
- `phi3` / `incident_d5_monitor`: quote=0.55, evidence=0.4, confidence=0.5
- `mistral:7b` / `gov_sample_d6_vendor`: quote=0.6, evidence=0.55, confidence=0.65
- `llama3.1:8b` / `gov_sample_d5_incidents`: quote=0.65, evidence=0.65, confidence=0.7
- `phi3` / `gov_sample_d2_oversight`: quote=0.65, evidence=0.55, confidence=0.55
