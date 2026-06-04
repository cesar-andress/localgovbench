# LocalGovBench — reproducible end-to-end demo walkthrough

Complete **GRB (Governance Readiness Benchmark)** workflow from synthetic municipality documents to a readiness report. Run all commands from the **repository root** (`localgovbench/`).

**Prerequisites**

```bash
cd /path/to/localgovbench
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Demo inputs: `data/synthetic/workflow_demo/documents/`  
Demo outputs: `outputs/demo_municipality/` (gitignored; safe to delete and regenerate).

---

## 1. Clean previous outputs

Remove stale artifacts so this run is reproducible from a clean state.

```bash
rm -rf outputs/demo_municipality
mkdir -p outputs/demo_municipality
```

---

## 2. Generate assessment template (prepare phase)

Builds the evidence log and human scoring template. **No Ollama required.**

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template
```

Creates:

- `outputs/demo_municipality/evidence_log.yaml`
- `outputs/demo_municipality/assessor_scoring_template.yaml`
- `outputs/demo_municipality/machine_readable_results.json`

---

## 3. Inspect `evidence_log.yaml` and `assessor_scoring_template.yaml`

Confirm structure before scoring. The template must have **54 indicators** with `null` scores; the evidence log lists **candidate evidence** (not maturity scores).

```bash
head -n 30 outputs/demo_municipality/evidence_log.yaml
grep -c "entries:" outputs/demo_municipality/evidence_log.yaml
head -n 25 outputs/demo_municipality/assessor_scoring_template.yaml
grep -c ": null" outputs/demo_municipality/assessor_scoring_template.yaml
```

Optional full view:

```bash
less outputs/demo_municipality/evidence_log.yaml
less outputs/demo_municipality/assessor_scoring_template.yaml
```

Do **not** use `assessor_scoring_template.yaml` with `--compute-score` while scores are `null`.

---

## 4. Fill synthetic demo scores

**SYNTHETIC DEMO ONLY** — deterministic placeholders for pipeline walkthrough, not real human assessment.

```bash
python scripts/fill_demo_scores.py \
  --input outputs/demo_municipality/assessor_scoring_template.yaml \
  --output outputs/demo_municipality/assessor_scoring_completed.yaml
```

Verify scores are filled:

```bash
grep -c ": null" outputs/demo_municipality/assessor_scoring_completed.yaml || true
head -n 20 outputs/demo_municipality/assessor_scoring_completed.yaml
```

For a **real** municipality study, skip this script and edit the template manually (0–4 per indicator), then save as `assessor_scoring_completed.yaml`.

---

## 5. Compute readiness

Uses completed scores and the evidence log from step 2.

```bash
python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --scores outputs/demo_municipality/assessor_scoring_completed.yaml \
  --output-dir outputs/demo_municipality \
  --compute-score
```

Updates:

- `outputs/demo_municipality/readiness_report.md`
- `outputs/demo_municipality/machine_readable_results.json`

Expect a line similar to: `Readiness (final): 75.0 — Advanced readiness` (exact value depends on demo scores).

---

## 6. Open `readiness_report.md`

Review the report: it separates **candidate evidence**, **human/demo-assigned scores**, and **computed readiness**.

```bash
less outputs/demo_municipality/readiness_report.md
```

On Linux desktop (if available):

```bash
xdg-open outputs/demo_municipality/readiness_report.md
```

On macOS:

```bash
open outputs/demo_municipality/readiness_report.md
```

---

## 7. Optional: Ollama evidence extraction

Ollama extracts **candidate evidence only** — it **never** assigns maturity scores (0–4).

Terminal 1 — start Ollama:

```bash
ollama serve
```

Terminal 2 — pull model and re-run prepare (after step 1 clean, or on a fresh output dir):

```bash
ollama pull llama3.1:8b

rm -rf outputs/demo_municipality
mkdir -p outputs/demo_municipality

python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template \
  --use-ollama \
  --model llama3.1:8b
```

If Ollama is down, the workflow prints a **warning** and continues without LLM extraction.

Then repeat steps **4** and **5** (demo scores or manual scoring, then compute).

Standalone single-indicator prototype:

```bash
python scripts/run_ollama_evidence_extraction.py
```

See `prompts/evidence_extraction.md`.

---

## 8. Demo scores are synthetic — not empirical validation

| This walkthrough demonstrates | This walkthrough does **not** provide |
|------------------------------|---------------------------------------|
| CLI path: documents → evidence log → scores → readiness | Field-validated municipal benchmark scores |
| Frozen GRB scoring on synthetic inputs | Content validity, inter-rater reliability, or legal compliance |
| `fill_demo_scores.py` as a teaching aid | Evidence suitable for publication tables |

**Important:**

- `data/synthetic/workflow_demo/documents/` — fictional municipality text.
- `fill_demo_scores.py` — prints **SYNTHETIC DEMO ONLY**; never cite its output as study data.
- `assessor_scoring_template.yaml` — for real human coders; all `null` until completed.
- Empirical validation protocols: [validation_protocol.md](validation_protocol.md).

---

## Verify the repository

```bash
pytest -m "not integration"
python scripts/validate_repository.py
```

---

## One-shot command block (copy-paste)

After `pip install -e ".[dev]"` from the repo root:

```bash
rm -rf outputs/demo_municipality
mkdir -p outputs/demo_municipality

python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --output-dir outputs/demo_municipality \
  --generate-template

python scripts/fill_demo_scores.py \
  --input outputs/demo_municipality/assessor_scoring_template.yaml \
  --output outputs/demo_municipality/assessor_scoring_completed.yaml

python scripts/run_assessment_workflow.py \
  --case-id demo_municipality \
  --documents data/synthetic/workflow_demo/documents \
  --scores outputs/demo_municipality/assessor_scoring_completed.yaml \
  --output-dir outputs/demo_municipality \
  --compute-score

less outputs/demo_municipality/readiness_report.md
```

---

## Related links

- [reproducibility.md](reproducibility.md)
- [artifact_description.md](artifact_description.md)
- [data/synthetic/workflow_demo/README.md](../data/synthetic/workflow_demo/README.md)

---

*LocalGovBench v0.1.0 — GRB workflow demo*
