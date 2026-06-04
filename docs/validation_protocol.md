# Empirical Validation Protocol — LocalGovBench v0.1

**Instrument status:** **Frozen** for v0.1 — five dimensions, 25 criteria, 0–4 maturity scale. This protocol governs **empirical validation only**; instrument definitions are not modified during Phase 1 studies.

**Audience:** Researchers preparing GIQ / EGOV field studies and Zenodo archival releases.

---

## Phase overview

| Phase | Package | Deliverable |
|-------|---------|-------------|
| 1 | Content validity | I-CVI, S-CVI/Ave, Lawshe CVR; criterion revisions log |
| 2 | Inter-rater reliability | Cohen's κ, Krippendorff's α per case |
| 3 | Discriminant validity | Profile separation on synthetic + field cases |
| 4 | Field deployment | Anonymised case repository (separate deposit) |
| 5 | Reporting | Validation benchmark report + paper |

---

## 1. Content validity package

| Resource | Path |
|----------|------|
| Expert review questionnaire | `validation/content_validity/expert_review_questionnaire.yaml` |
| Indicator relevance survey | `validation/content_validity/indicator_relevance_survey.yaml` |
| Assessor scoring rubric | `validation/content_validity/scoring_rubric.md` |
| Analysis script | `scripts/run_content_validity_analysis.py` |
| Example panel data (synthetic) | `validation/content_validity/indicator_relevance_survey_results.example.yaml` |

### Procedure

1. Recruit **6–8 experts** (public administration, law/DPO, IT security, AI ethics).
2. Collect relevance ratings (1–5) per criterion.
3. Run:

```bash
cp validation/content_validity/indicator_relevance_survey_results.example.yaml \
   validation/content_validity/indicator_relevance_survey_results.yaml
# Edit with real panel data, then:
python scripts/run_content_validity_analysis.py
```

4. Retain criteria with I-CVI ≥ 0.78 (configurable in `localgovbench/validation/content_validity.py`).
5. Document revisions in instrument changelog (v0.2+); **do not alter v0.1 mid-study**.

### Metrics

- **I-CVI** — Item Content Validity Index per criterion
- **S-CVI/Ave** — Mean I-CVI across scale
- **Lawshe CVR** — Essentiality ratio per item

---

## 2. Inter-rater reliability package

| Resource | Path |
|----------|------|
| Assessor guide | `validation/inter_rater/assessor_guide.md` |
| Scoring template | `validation/inter_rater/scoring_template.yaml` |
| Cohen's κ | `localgovbench/validation/reliability.py` |
| Krippendorff's α | `localgovbench/validation/reliability.py` |
| IRR analysis | `scripts/run_inter_rater_analysis.py` |
| Training ratings | `validation/ratings/` (synthetic pilot) |

### Procedure

1. Train coders on `validation/benchmark_cases/` synthetic cases.
2. Independent coding of field cases (two raters minimum).
3. Adjudicate |Δ| ≥ 2 (`validation/templates/adjudication_record.yaml`).
4. Run `python scripts/run_inter_rater_analysis.py`.
5. Report κ and α with confidence intervals in publication (bootstrap in field study).

---

## 3. Synthetic benchmark cases

| Case | Profile | Path |
|------|---------|------|
| Low readiness | Minimal governance | `validation/benchmark_cases/municipality_low_readiness.yaml` |
| Medium readiness | Partial maturity | `validation/benchmark_cases/municipality_medium_readiness.yaml` |
| High readiness | Advanced practice | `validation/benchmark_cases/municipality_high_readiness.yaml` |
| Sovereign ready | Strong sovereignty + controls | `validation/benchmark_cases/municipality_sovereign_ready.yaml` |
| Compliance gap | Strong docs, weak oversight | `validation/benchmark_cases/municipality_compliance_gap.yaml` |

Each file includes:

- `governance_evidence` — synthetic narrative and artefact references
- `responses` — 25 criterion scores
- `expected_outcome` — maturity, readiness index, band (for pipeline checks)

---

## 4. Discriminant validity package

```bash
python scripts/run_discriminant_validity.py
# → validation/reports/discriminant_validity.md
```

**Hypothesis (structural):** scoring ordering reflects low < medium < high maturity; `compliance_gap` scores below `high` despite strong legal/technical item scores.

---

## 5. GRB structural sensitivity (frozen 54-indicator experiment)

The **Governance Readiness Benchmark (GRB)** uses a separate six-dimension instrument. Its specification, indicators, and scoring formula are **frozen** for this experiment; sensitivity work varies **synthetic inputs only**.

| Resource | Path |
|----------|------|
| Profile generator and aggregation | `localgovbench/grb/sensitivity.py` |
| Runner | `scripts/run_grb_sensitivity_analysis.py` |
| Results | `results/grb_sensitivity_analysis.csv` |
| Report | `reports/grb_sensitivity_analysis.md` |
| Tests | `tests/test_grb_sensitivity_analysis.py` |

### Procedure

1. Generate **≥150** deterministic profiles across groups: `baseline`, `low_d2`, `low_d4`, `high_d6`, `mixed`.
2. Vary maturity inputs on **D2 Human Oversight**, **D4 Data Legitimacy and Processing**, and **D6 Strategic Sovereignty**; hold D1, D3, D5 at baseline unless noted in `mixed`.
3. Run:

```bash
python scripts/run_grb_sensitivity_analysis.py
```

4. Review group means, safeguard **G1** activation (cap at 60 when D2 or D4 dimension score &lt; 2.0), and directional contrasts in the Markdown report.

### What this phase claims

- Structural responsiveness of the **frozen** GRB scoring model on synthetic profiles.
- Reproducible CSV schema and deterministic profile IDs.

### What this phase does not claim

- Empirical municipal validation or weight calibration.
- Modification of GRB indicators or readiness formula.

---

## 6. GRB inter-rater reliability (frozen 54-indicator experiment)

| Resource | Path |
|----------|------|
| Protocol | [inter_rater_reliability_protocol.md](inter_rater_reliability_protocol.md) |
| Evidence packs & assessor YAML | `examples/grb/inter_rater/` |
| Metrics (κ, Fleiss, disagreement tables) | `localgovbench/grb/reliability.py` |
| Runner | `scripts/run_inter_rater_reliability.py` |
| Outputs | `results/inter_rater_reliability.csv`, `reports/inter_rater_reliability.md` |
| Tests | `tests/test_grb_reliability.py` |

### Procedure

1. Train assessors using the protocol (unit = case × indicator; scale 0–4; evidence rules E2/E3).
2. Independent coding of `case_alpha`, `case_beta`, `case_gamma` evidence packs.
3. Run `python scripts/run_inter_rater_reliability.py`.
4. Adjudicate indicators with |Δ| ≥ 2; document in adjudication template.

### Metrics reported

- Percent agreement (unanimous units)
- Cohen's κ (pairwise, two raters)
- Fleiss' κ (three or more raters)
- Disagreement table by indicator and dimension

---

## 7. Optional: Ollama evidence extraction

LLM proposes **candidate evidence only** — humans assign scores.

```bash
ollama serve
ollama pull llama3.1:8b
python scripts/run_ollama_evidence_extraction.py
```

See `prompts/evidence_extraction.md`.

---

## 8. Reporting and ethics

- Generate integrated report: `python scripts/generate_validation_report.py`
- Do not publish municipality league tables without consent.
- Do not commit identifiable procurement or citizen data.

---

## 9. What this protocol does not claim

- Legal certification or AI Act conformity
- Validated predictive power
- Completeness of EU local government diversity

---

## Cross-references

- [benchmark_specification.md](benchmark_specification.md) — frozen instrument
- [methodology.md](methodology.md) — research workflow
- [manuscript_positioning.md](manuscript_positioning.md) — related instruments
- [../validation/README.md](../validation/README.md) — package index

---

*LocalGovBench v0.1 empirical validation protocol*
