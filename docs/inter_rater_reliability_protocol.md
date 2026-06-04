# GRB Inter-Rater Reliability Protocol

**Instrument:** Governance Readiness Benchmark (GRB) v0.1-experiment — **54 indicators**, six dimensions.  
**Status:** Specification, indicators, scoring formula, and safeguards are **frozen** for this validation phase.

**Audience:** Researchers running a GRB coding study before field deployment or Zenodo release.

---

## Objective

Estimate **inter-rater reliability** among trained assessors scoring the same synthetic or field evidence packs on the GRB 0–4 maturity scale. This protocol supports:

- Training and calibration of coders
- Documentation of disagreement patterns (especially D2 and D4)
- Reproducible IRR metrics (percent agreement, Cohen's κ, Fleiss' κ)

It does **not** certify legal conformity or replace municipal self-assessment.

---

## Assessor instructions

1. Read the case **evidence pack** (`case_*_evidence_pack.md`) in full before scoring.
2. Score **every indicator** in the GRB checklist for that case (54 items).
3. Use only integer scores **0–4**; do not leave items blank.
4. Record evidence references in the assessor YAML `evidence_log` when assigning scores ≥ 3.
5. Code **observable maturity** from artefacts, not aspirational policy language.
6. Work **independently** — do not discuss scores until the adjudication phase.
7. Flag uncertainty in `notes` (per case) rather than guessing.

---

## Unit of analysis

The reliability **unit** is one **(case_id, indicator_id)** pair:

- **Case:** a bounded municipal AI governance scenario (e.g. `case_alpha`).
- **Indicator:** one of 54 frozen GRB indicators (e.g. `d2_oversight_design_01`).

With three cases and 54 indicators, a full study yields **162 units per rater**.

---

## Scoring scale (0–4)

| Score | Label | Guidance |
|-------|-------|----------|
| 0 | Absent | No credible artefact; practice not evidenced |
| 1 | Ad hoc | Fragmentary or informal only |
| 2 | Defined | Documented expectation; partial implementation |
| 3 | Managed | Implemented, monitored, with accountable roles |
| 4 | Optimizing | Measured improvement; audit-ready evidence |

Scores feed the **frozen** GRB aggregation (subdimension → dimension → readiness). Assessor YAML files store **indicator-level** scores only.

---

## Evidence rules

Aligned with GRB experiment gates (E2/E3) documented in `localgovbench/grb/scoring.py`:

| Score | Evidence requirement |
|-------|---------------------|
| 0–2 | No minimum references (still cite sources in `evidence_log` when available) |
| ≥ 3 | At least **one** artefact reference per indicator |
| 4 | At least **two** independent references |

Acceptable references: policy excerpts, committee minutes, architecture diagrams, DPIA summaries, procurement clauses, audit logs (anonymised). **Do not** invent artefact IDs.

---

## How to handle uncertainty

1. Re-read the indicator **prompt** in the frozen specification.
2. If evidence is ambiguous, score **conservatively** (lower bound) and document rationale in `notes`.
3. If evidence is missing for a claimed practice, score **0** or **1**, not 3.
4. If two artefacts conflict, prefer the **older binding** governance document unless superseded.
5. Escalate systematic ambiguity to the study lead **before** adjudication — do not change indicator definitions.

---

## How to report disagreements

1. After independent coding, run:

```bash
python scripts/run_inter_rater_reliability.py
```

2. Review `reports/inter_rater_reliability.md` and `results/inter_rater_reliability.csv`.
3. For each |Δ| ≥ 2 on any indicator, complete an adjudication record (see `validation/templates/adjudication_record.yaml`).
4. Re-score only disputed units after consensus; store adjudicated files separately (`*_adjudicated.yaml`).
5. Report:
   - Percent agreement (unanimous units)
   - Cohen's κ for each rater pair
   - Fleiss' κ for three or more raters
   - Disagreement counts by dimension (D2/D4 expected in pilot)

---

## Bundled pilot materials

| Resource | Path |
|----------|------|
| Evidence packs | `examples/grb/inter_rater/case_*_evidence_pack.md` |
| Assessor templates | `examples/grb/inter_rater/assessor_*_scores.yaml` |
| Metrics | `localgovbench/grb/reliability.py` |
| Runner | `scripts/run_inter_rater_reliability.py` |

All bundled scores are **synthetic** for tooling validation.

---

## Limitations

- Pilot cases are fictional municipalities — not empirical benchmarks.
- κ depends on score prevalence; high agreement on few categories can yield moderate κ.
- Three raters and three cases are insufficient for generalisation.
- IRR does not validate indicator weights, safeguard G1, or readiness formula (frozen).
- No LLM auto-scoring in this phase — humans remain authoritative.

---

## Cross-references

- [validation_protocol.md](validation_protocol.md) — LocalGovBench v0.1 and GRB validation phases
- [benchmark_specification.md](benchmark_specification.md) — frozen v0.1 instrument
- `localgovbench/grb/specification.py` — GRB indicator tree (read-only)

---

*GRB inter-rater reliability protocol — research use only*
