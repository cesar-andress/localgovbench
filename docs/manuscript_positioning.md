# Manuscript Positioning — LocalGovBench

**Audience:** Government Information Quarterly (GIQ), Electronic Government (EGOV), and related public administration / digital government venues.

**Purpose:** Position LocalGovBench against established instruments and clarify its **scientific contribution** without overclaiming legal compliance, empirical validation, or superiority over existing frameworks.

**Instrument version:** LocalGovBench v0.1 — five dimensions, 25 criteria (unchanged). Extended GRB (54 indicators) and Ollama evidence extraction are **research prototypes**, not part of the core validated claim until field studies are reported.

---

## Related instruments and positioning

The table below compares representative families of tools and frameworks. Wording is **indicative** for manuscript drafting; authors should verify current versions of external instruments at submission time.

| Instrument | Primary scope | Unit of analysis | Output metric | Evidence requirements | Sector specificity | LLM / local-sovereign specificity | Empirical validation status | Gap relative to LocalGovBench |
|------------|---------------|------------------|---------------|----------------------|--------------------|-----------------------------------|----------------------------|------------------------------|
| **ALTAI / EU Trustworthy AI Assessment List** | Trustworthy AI self-assessment aligned with HLEG requirements | Organisation or AI system (general) | Qualitative checklist / narrative assessment | Self-declared responses; varies by user | Cross-sector | Low — not tailored to on-premise LLM in municipalities | Widely used in EU policy context; peer-reviewed validation of municipal use limited | Lacks **municipal** unit of analysis, **readiness index**, and **evidence-gated** 0–4 protocol for sovereign local deployments |
| **NIST AI Risk Management Framework** | Risk management lifecycle (Govern, Map, Measure, Manage) | Organisation (flexible) | Risk profile / maturity narrative | Documentation of risk practices recommended | Cross-sector (US-origin, globally referenced) | Low — general AI systems | NIST publications and adoption studies; not a municipal LLM benchmark | Does not provide a **compact benchmark** with **comparative readiness score** for **European local government** LLM governance |
| **ISO/IEC 42001 AI Management System** | Certifiable AI management system (AIMS) | Organisation seeking certification | Conformity to management system requirements | Audit evidence for certification | Cross-sector | Low — not LLM- or locality-specific | International standard with certification pathway | **Certification-oriented**, not a **lightweight research benchmark**; high barrier for small municipalities |
| **General public-sector digital maturity models** | eGovernment / digital government capability (services, data, infrastructure) | Jurisdiction or agency | Maturity stage / index | Varies by model (surveys, indicators) | Public sector (often national) | Very low — pre-GenAI assumptions | Decades of eGov maturity literature | **Does not address AI governance** for **sovereign LLM** deployments |
| **AI readiness indexes** | National or organisational capacity to adopt AI | Country, sector, or enterprise | Composite readiness / adoption index | Mixed (surveys, expert judgment) | Often national or industry | Low — adoption and capacity, not governance depth | Various policy reports and indices | Conflates **adoption readiness** with **governance readiness**; weak on **human oversight** and **data sovereignty** for local LLM |
| **AI Act compliance checklists** | Legal obligations under Regulation (EU) 2024/1689 | Provider / deployer by system class | Compliance gap lists | Legal and technical documentation | EU-regulated contexts | Medium for deployer duties; not municipal operations | Emerging practice; not unified validated municipal instrument | **Legal compliance** focus, not **governance maturity**; risk of **checklist compliance** without institutional capacity metrics |
| **Responsible AI toolkits** | Ethical principles (fairness, transparency, accountability) | Project or organisation | Principle coverage / policy templates | Variable | Cross-sector | Low — rarely operationalised for on-prem LLM in government | Large normative literature; toolkits vary | Principles without **standardised municipal benchmark**, **scoring**, or **IRR package** |
| **LocalGovBench** | Governance **readiness** for **sovereign on-premise LLM** in **European local government** | Municipal (or inter-municipal) LLM programme | Criterion maturity 0–4; dimension and readiness indices | **Evidence-gated** scoring protocol (documented artefacts) | **European local public sector** (explicit scope) | **High** — designed for local/sovereign LLM context | **Instrument + validation package** in repo; **field validation pending** | Fills niche: **research-grade open artifact** linking HLEG / AI Act **themes** to **auditable indicators** without claiming legal certification |

### Positioning summary (one paragraph for manuscripts)

LocalGovBench does not replace ALTAI, NIST AI RMF, ISO/IEC 42001, or AI Act conformity tools. It **complements** them by offering a **domain-specific**, **evidence-oriented** governance readiness benchmark for **municipal sovereign LLM deployments**, packaged as an open, reproducible instrument with templates for content validity and inter-rater reliability studies.

---

## Contribution statement

LocalGovBench contributes to digital government and AI governance research in three ways:

1. **A context-specific governance readiness instrument** for **sovereign large language model (LLM) deployments** in **European local governments**. The benchmark operationalises governance expectations relevant to on-premise or institution-controlled hosting—where prompts, logs, and model weights remain under public authority control—using five dimensions and 25 assessable criteria derived from trustworthy AI, accountability, and public-sector governance literature.

2. **An evidence-gated scoring protocol** that separates **governance readiness** from **technical model performance**. Maturity scores (0–4) and aggregated readiness indices are tied to documentary and procedural evidence rules; the instrument does not evaluate perplexity, accuracy, or benchmark leaderboards. This distinction supports socio-technical research on whether **institutional governance capacity** is plausibly associated with responsible deployment decisions.

3. **An open and reproducible benchmark artifact** suitable for **empirical validation** and **future comparative studies**. The repository provides checklist generation, scoring utilities, synthetic cases, inter-rater reliability metrics (Cohen's κ, Krippendorff's α), sensitivity analysis tooling, and Zenodo-oriented release documentation—enabling independent replication and municipal case studies without proprietary lock-in.

**Explicit non-claims:** LocalGovBench does **not** certify legal compliance, does **not** demonstrate full AI Act conformity, does **not** assert superiority over ALTAI, NIST, or ISO instruments, and does **not** claim validated predictive power regarding outcomes (e.g., incidents, citizen trust, or service quality) until such evidence is reported in peer-reviewed field research.

---

## Reviewer objections and mitigation strategies

| # | Likely objection | Mitigation strategy |
|---|------------------|---------------------|
| 1 | **Redundancy with ALTAI / EU tools** | Provide side-by-side mapping table (see `docs/ai_act_mapping.md`); emphasise **municipal unit of analysis**, **0–4 evidence-gated scoring**, and **readiness index** not offered as a unified municipal package elsewhere. |
| 2 | **No empirical validation yet** | Report validation **protocol** and synthetic IRR pilot; position paper as **instrument development** + pilot; commit to field study in discussion / future work. |
| 3 | **Arbitrary 0–4 scale and equal weights** | Document scale definitions; report **sensitivity analysis** (`scripts/run_sensitivity_analysis.py`); plan weight calibration in post-pilot revision. |
| 4 | **Confusing readiness with legal compliance** | Prominent disclaimers; separate **legal mapping** (indicative) from **maturity scores**; avoid “compliant/non-compliant” language. |
| 5 | **Small municipalities cannot meet evidence burden** | Discuss **proportionality**; recommend tiered use (self-assessment vs external review); future “light” item subsets in discussion. |
| 6 | **Checklist governance / performativity** | Triangulate documents with interviews in field design; acknowledge gap between **documented** and **practised** governance. |
| 7 | **Western / EU-centric bias** | State explicit geographic scope; discuss transferability limits; avoid universal claims. |
| 8 | **GenAI obsolescence** | Version instrument (v0.1); modular criteria; Zenodo versioning; open change log. |
| 9 | **League tables harm weaker municipalities** | Policy: no public rankings; aggregated/anonymised research only; ethics in `validation/docs/validation_protocol.md`. |
| 10 | **LLM-assisted coding bias** | Ollama module extracts **candidate evidence only**; **human scoring** mandatory; report in methods if used. |
| 11 | **Construct validity unproven** | Conduct **content validity** expert panel (`validation/templates/content_validity_study.yaml`); report I-CVI / qualitative synthesis. |
| 12 | **n too small for generalisation** | Frame as exploratory municipal cases; use **thick description** + reliability metrics; avoid statistical generalisation beyond sample. |

---

## Manuscript claims to avoid

Do **not** write (examples):

- “LocalGovBench certifies AI Act compliance.”
- “Municipalities achieving readiness ≥75 are safe to deploy citizen-facing LLMs.”
- “We validate the framework across Europe.” (unless a representative multi-country study is actually conducted)
- “Superior to ALTAI / NIST / ISO for all AI governance purposes.”
- “The readiness score predicts reduced harm / increased trust.” (without outcome data)
- “Fully validated benchmark” (while only synthetic IRR and templates exist)
- “Automated assessment via LLM replaces expert judgment.”
- “Sovereign AI guaranteed by high scores.”
- “Generalisable digital maturity index for all AI systems.”
- “Legal advice for deployers.”

**Safer formulations:**

- “We **propose** an instrument…”
- “Indicative alignment with AI Act **themes**…”
- “Pilot inter-rater reliability on **synthetic** cases suggests the scoring pipeline is **operable**…”
- “Readiness denotes **documented governance maturity**, not legal conformity.”

---

## Recommended empirical validation plan

| Phase | Activity | Repository support | Deliverable |
|-------|----------|-------------------|-------------|
| **1. Content validity** | 6–8 expert panel rates clarity/relevance per criterion | `validation/templates/content_validity_study.yaml`, `validation/docs/content_validity_guide.md` | CV metrics, revised criteria (v0.2) |
| **2. Expert review** | Structured questionnaire on overlap and municipal fit | `validation/templates/expert_review_questionnaire.yaml` | Qualitative synthesis section |
| **3. Inter-rater reliability** | Two coders × 3+ municipal cases (documents + rating sheets) | `validation/cases/`, `validation/ratings/`, `scripts/run_inter_rater_analysis.py` | κ, α per case and pooled |
| **4. Synthetic benchmark cases** | Training coders; pipeline test before fieldwork | `validation/cases/`, `examples/example_assessment.yaml` | Coding manual appendix |
| **5. Sensitivity analysis** | Vary dimension inputs; test safeguard rules | `scripts/run_sensitivity_analysis.py`, `results/sensitivity_analysis.csv` | Structural properties of scoring model |
| **6. Optional evidence extraction** | Ollama proposes quotes; **humans assign scores** | `scripts/run_ollama_evidence_extraction.py`, `prompts/evidence_extraction.md` | Methods paragraph on HITL |
| **7. Field cases** | 3–5 municipalities (ethics approval, anonymisation) | Store **only** anonymised derivatives; not raw docs in public repo | Case narratives + readiness profiles |
| **8. Reporting** | Full validation benchmark report | `scripts/generate_validation_report.py` | Supplementary material / Zenodo archive |

**Publication sequence suggestion:** (1) instrument paper with phases 1–3 + synthetic IRR pilot; (2) field study paper with phases 7–8; or combined if timeline permits.

---

## Suggested manuscript sections (GIQ / EGOV)

| Section | Content pointer |
|---------|-----------------|
| Introduction | Municipal sovereign LLM gap; readiness vs model metrics |
| Related work | Table in this document + AI gov / eGov literature |
| Instrument design | `docs/benchmark_specification.md`, `docs/framework.md` |
| Methods | `validation/docs/validation_protocol.md`, IRR metrics |
| Results | Expert panel + field cases (when available) |
| Discussion | Limitations from “Reviewer objections” |
| Data availability | Git + Zenodo DOI; synthetic vs field data labelled |

---

## Cross-references

- Benchmark specification: [benchmark_specification.md](benchmark_specification.md)
- Methodology: [methodology.md](methodology.md)
- Validation package: [../validation/README.md](../validation/README.md)
- AI Act / GDPR mappings: [ai_act_mapping.md](ai_act_mapping.md), [gdpr_mapping.md](gdpr_mapping.md)

---

*Internal manuscript support document — not a published paper section without author editing.*
