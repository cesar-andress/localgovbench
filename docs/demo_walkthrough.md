# End-to-end GRB workflow — reproducible demo walkthrough

This guide runs the **Governance Readiness Benchmark (GRB)** pipeline from synthetic municipality documents to a readiness report. All bundled inputs and the optional demo score filler are **synthetic** — they do **not** constitute empirical validation.

**Prerequisites:** Python 3.11+, repository root as working directory.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Demo documents: `data/synthetic/workflow_demo/documents/`  
Output folder: `outputs/demo_municipality/` (created by the scripts; listed in `.gitignore`).

---

## 1. Generate the template (prepare phase)

Creates `evidence_log.yaml` and `assessor_scoring_template.yaml` with **all 54 indicators** set to `null`. No Ollama required.

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template
```

**Expected outputs:**

| File | Purpose |
|------|---------|
| `outputs/demo_municipality/evidence_log.yaml` | Candidate evidence entries (indexed from documents) |
| `outputs/demo_municipality/assessor_scoring_template.yaml` | Human scoring template — **scores are null** |
| `outputs/demo_municipality/machine_readable_results.json` | Machine-readable prepare-phase metadata |

Do **not** pass `assessor_scoring_template.yaml` to `--compute-score` until every indicator has a score.

---

## 2. Fill synthetic demo scores (walkthrough helper only)

Deterministic placeholder scores (~level 3 per dimension) for pipeline testing.

```bash
python scripts/fill_demo_scores.py \
  --input outputs/demo_municipality/assessor_scoring_template.yaml \
  --output outputs/demo_municipality/assessor_scoring_completed.yaml
```

**Expected output:** `outputs/demo_municipality/assessor_scoring_completed.yaml`

For a **real** assessment, skip this step and edit the template manually (integer scores 0–4 per indicator), then save under a new filename (e.g. `assessor_scoring_completed.yaml`).

---

## 3. Compute readiness

Uses **human or demo-completed** scores plus `evidence_log.yaml` from step 1.

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --scores outputs/demo_municipality/assessor_scoring_completed.yaml \
  --output-dir outputs/demo_municipality \
  --compute-score
```

**Expected outputs:**

| File | Purpose |
|------|---------|
| `outputs/demo_municipality/readiness_report.md` | Report separating candidate evidence, human/demo scores, and computed readiness |
| `outputs/demo_municipality/machine_readable_results.json` | Updated JSON with readiness metrics |

Example console line: `Readiness (final): … — …`

---

## 4. Optional: Ollama candidate evidence extraction

Requires a **local** [Ollama](https://ollama.com) server and a pulled model. Ollama proposes **candidate evidence only** — it **never** assigns maturity scores (0–4).

Start Ollama (separate terminal):

```bash
ollama serve
ollama pull llama3.1:8b
```

Re-run the **prepare** phase with `--use-ollama` (replace or refresh outputs in the same folder):

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template \
  --use-ollama \
  --model llama3.1:8b
```

If Ollama is unavailable, the workflow prints a **warning** and continues without LLM extraction.

Standalone extraction prototype (single indicator experiment):

```bash
python scripts/run_ollama_evidence_extraction.py
```

See `prompts/evidence_extraction.md`.

After Ollama prepare, continue from **step 2** (demo scores or manual scoring) and **step 3** (compute).

---

## 5. Synthetic demo scores are not validation evidence

| What the demo provides | What it does **not** prove |
|------------------------|----------------------------|
| Reproducible CLI path from documents → evidence log → scores → readiness | Municipal governance quality in the field |
| Frozen GRB scoring engine behaviour on synthetic inputs | Content validity, inter-rater agreement, or legal compliance |
| `fill_demo_scores.py` deterministic placeholders for walkthroughs | Expert-assessed or empirically validated benchmark scores |

**Rules:**

- `assessor_scoring_template.yaml` — empty template for **real** human coders only.
- `fill_demo_scores.py` — **SYNTHETIC DEMO ONLY**; do not cite outputs as study results.
- Published claims require field data, validation protocols in [validation_protocol.md](validation_protocol.md), and explicit `synthetic: false` metadata only when genuinely applicable.

Bundled workflow documents under `data/synthetic/workflow_demo/` are fictional municipalities.

---

## Quick verification

```bash
pytest -m "not integration"
python scripts/validate_repository.py
```

---

## Related documentation

- [reproducibility.md](reproducibility.md) — full install and script index
- [artifact_description.md](artifact_description.md) — scope and validation status
- [data/synthetic/workflow_demo/README.md](../data/synthetic/workflow_demo/README.md) — demo document index

---

*LocalGovBench GRB workflow demo — research artifact v0.1.0*
