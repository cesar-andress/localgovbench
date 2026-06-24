# 4. Methods

## 4.1 Research design

This study employs a **source-schema satisfiability design** to measure the **public-evidence ceiling** of programme-level AI governance evidence requirements. The objective is not to evaluate whether public-sector AI programmes are well governed, compliant, or “ready” for deployment, but to determine **how far official public inventories can satisfy specified evidence requirements** when those requirements are defined with explicit evidence gates.

The **unit of analysis** is the pairing of (i) a LocalGovBench v0.1 **evidence requirement** (one of 25 criteria) and (ii) a **public inventory source schema** (one of five official programme-level datasets). Programme-level **records** provide the empirical volume over which inventory fields are observed (N = 7,434 records across sources), but satisfiability is assessed at the **requirement × source schema** level: we ask whether native fields exposed by an inventory could, in principle, supply the artefacts required by each evidence gate. Individual programmes are not scored, ranked, or classified by governance quality.

An **evidence requirement** specifies (a) a governance criterion statement, (b) an evidence hint describing the types of artefacts assessors would expect, (c) an expected primary artefact type, and (d) an **evidence gate** requiring at least one named primary artefact for achievement of the highest evidence tier in the LocalGovBench v0.1 scoring rubric (score ≥ 3). This study uses the instrument as a **requirement catalogue** and gate specification; it does **not** assign readiness scores, maturity indices, or composite governance measures to any programme or jurisdiction.

The **public-evidence ceiling** is the maximum level of evidence shortfall reduction achievable from **public inventory fields alone** across all sources for a given requirement. Where the ceiling falls below the evidence gate, the requirement is **gate-unreachable** from public data regardless of record volume. The ceiling is expressed on a graded **evidence shortfall scale** (Levels 0–4; see §4.2) rather than as a binary “present/absent” judgment.

**No readiness scores were assigned** in this study. Requirements were not used to assess programme performance, organisational capability, or policy outcomes. Non-availability of public evidence for a gate does **not** imply absence of internal governance artefacts; internal dossiers, security records, and legal files may satisfy gates without appearing in public inventories. This design therefore differs fundamentally from programme assessment studies that infer governance quality from observable public data.

---

## 4.2 LocalGovBench evidence-requirement specification

We used LocalGovBench v0.1 (`instrument_version: v0.1.0`; `framework_version: 0.1`) as a structured set of **25 evidence requirements** organised into **five governance dimensions** (five criteria each):

1. Legal and Regulatory Compliance  
2. Technical and Security Readiness  
3. Organizational Governance  
4. Operational Management  
5. Strategic Sovereignty  

Each criterion is defined in a machine-readable configuration file (`localgovbench_measurement_validation/pilot_public_satisfiability/config/localgovbench_criteria_v0.yaml`) with the following elements: `criterion_id`, `criterion_statement`, `evidence_hint`, `expected_artifact_type`, and `evidence_gate_score_3_requires` (≥ 1 primary named artefact per the LocalGovBench v0.1 scoring rubric). The configuration was generated from the framework dimension definitions (`localgovbench/framework/dimensions.py`) and frozen for analysis.

### Evidence-gated design

LocalGovBench v0.1 specifies that achievement of score ≥ 3 on a criterion requires **primary named artefacts** (e.g., a retention schedule, architecture diagram, risk register, or incident response plan)—not metadata proxies or narrative summaries alone. This study tests whether **public inventory schema fields** can surface such artefacts. A requirement is **gate-reachable from public inventories** only if at least one source schema could plausibly expose fields mapped to Level 4 on the shortfall scale (full evidence gate reachable). Requirements that reach Level 3 (named public artefact possible) but not Level 4 are still **gate-unreachable** under the score ≥ 3 threshold used here.

### Evidence shortfall scale (Levels 0–4)

For each requirement × source pair, we assigned an **evidence shortfall level** measuring the distance between what the inventory schema exposes and what the evidence gate demands. Levels were derived from native field coverage classes and a deterministic shortfall function (`mapping_rules.py::compute_shortfall`). Exact definitions:

| Level | Label | Definition |
|------:|-------|--------------|
| **0** | No public field | The inventory schema contains **no native field** mappable to the expected artefact type; the public layer provides no programme-level signal for this requirement. |
| **1** | Weak metadata proxy | One or more schema fields provide **weak metadata** (e.g., flags, supplier names, organisation labels) that may contextualise a programme but **do not constitute** the named primary artefact required for the evidence gate. |
| **2** | Partial programme-level signal | Schema fields provide **direct programme-level inventory disclosures** (e.g., lifecycle stage, human intervention narrative, lawful basis text) that partially align with the evidence hint but **do not satisfy** the primary-artefact threshold for score ≥ 3. |
| **3** | Named public artefact possible | A **named public artefact** may be inferable from inventory disclosures, but it does not meet the LocalGovBench primary-artefact threshold for full gate satisfaction. |
| **4** | Full evidence gate reachable | Native inventory fields could **fully satisfy** the score ≥ 3 evidence gate (≥ 1 primary named artefact reachable from public schema). |

The maximum shortfall level observed across sources for each requirement was used to summarise the public-evidence ceiling for that requirement. **Readiness scores (0–4 maturity levels for programmes) were not computed**; Levels 0–4 here index **evidence shortfall from public schema satisfiability**, not organisational maturity.

---

## 4.3 Corpus construction

### Sources and inclusion criteria

We assembled a multi-jurisdiction corpus of **official public-sector AI programme inventories** using machine-readable acquisition only. All records were collected on **2026-06-24**. Sources, access methods, and record counts are documented in `data/source_registry_expanded.csv`.

**United States — OMB 2025 AI Use Case Inventory (US-OMB-2025; n = 3,611).**  
Individually reported federal AI use cases published in CSV format via the official 2025 Federal Agency AI Use Case Inventory repository (`Data/2025_individually_reported_AI_use_cases.csv`). Inclusion: all data rows in the published file; no additional releasability filtering applied at collection.

**Canada — Government AI Register (CA-GC-AI-REG; n = 412).**  
MVP register of federal AI systems from Open Government Canada (CSV resource `gc-ai-register-mvp-registre-de-lia-du-gc-pmv-04-26.csv`). Inclusion: all register rows.

**Netherlands — National Algorithm Register (NL-ALGO-REG; n = 1,484).**  
Bulk English-language export via the official Algoritmeregister API (`/api/downloads/ENG?filetype=csv`). Inclusion: all algorithm descriptions in the bulk export.

**European Union — Public Sector Tech Watch (EU-PSTW; n = 1,794).**  
JRC curated cases dataset (`pstw_dataset.csv`; semicolon-delimited). Inclusion: cases where **Primary Technology = Artificial Intelligence** (1,794 of 2,291 total cases retained).

**United Kingdom — Algorithmic Transparency Recording Standard records (UK-ATRS; n = 133).**  
GOV.UK Search API records with `filter_document_type=algorithmic_transparency_record`, paginated to completeness. Inclusion: all returned transparency records at collection date.

**Total corpus: N = 7,434 programme-level records.**

Only official government or supranational publication channels were used. No proprietary databases, scraped HTML dossiers, or secondary compilations were included.

### Normalisation process

Each source row was normalised to a common **programme record** schema (`data/pilot_programme_records.csv`) with the following fields: `record_id`, `jurisdiction`, `source_name`, `source_url`, `programme_title`, `programme_description`, `agency_or_owner`, `raw_fields_json`, and `collection_date`. Normalisation was performed by `scripts/build_pilot_corpus.py`:

- **Identifier assignment:** Stable `record_id` prefixed by source (e.g., `us-omb-2025-{id}`, `nl-algo-{source_id}`).  
- **Title and description:** Mapped from source-native name/description fields; concatenated narrative fields where inventories split problem statement and benefits (US OMB).  
- **Agency or owner:** Mapped from agency, organisation, or responsible-body fields.  
- **Raw field preservation:** Complete source row serialised as JSON in `raw_fields_json` to preserve native schema for mapping and robustness tests.  

Programme-level records represent **one row per inventory entry** (use case, system, algorithm description, PSTW case, or transparency record). The corpus does not harmonise programmes across sources into deduplicated entities; cross-source analysis operates at the **schema satisfiability** level.

---

## 4.4 Criterion-to-evidence mapping

### Mapping rules

Native inventory fields were mapped to evidence requirements using a frozen rule set (`localgovbench_measurement_validation/pilot_public_satisfiability/mapping_rules.py`). For each of the 25 criteria and each of the five sources, rules specify:

- **`SOURCE_SCHEMAS`:** Complete list of native field names observed for that inventory.  
- **`MAPPING_RULES`:** Per criterion × source tuple of `(coverage_class, mapped_fields, rationale, can_gate)`.  

**Coverage classes** translate to base shortfall levels before gate adjustment:

| Coverage class | Base shortfall level |
|----------------|---------------------:|
| `no_public_field` | 0 |
| `weak_proxy` | 1 |
| `direct_field` | 2 |
| `named_artifact_possible` | 3 |

If `can_gate = True`, shortfall Level 4 is assigned. In the frozen rule set, **no criterion × source pair** was assigned `can_gate = True` or `named_artifact_possible`; all gate reachability results follow from schema inspection rather than post hoc record content coding.

Mapping was performed by two authors’ structured rule definitions documented in the rule file rationale strings, then exported to `outputs/field_criterion_coverage_matrix.csv` (125 rows = 25 criteria × 5 sources) via `scripts/map_inventory_fields_to_criteria.py`. Each row includes `evidence_shortfall_level`, `evidence_shortfall_label`, and `reason_gate_not_reachable`.

### Public / partially public / structurally internal partition

Each evidence requirement received a **public-evidence satisfiability class** summarising whether public inventories could partially satisfy the requirement:

- **`structurally_internal`:** Public schemas lack programme-level signal (max shortfall Level 0, or Level 1 with internal-artefact evidence hints).  
- **`partially_public_satisfiable`:** At least one source provides weak or partial public signal (Level 1–2, or Level 2 with direct fields) without gate reachability.  
- **`public_satisfiable`:** Inventory-native lifecycle or status fields provide the strongest public layer signal for the requirement (Level 2 with direct fields on lifecycle/status criteria); still distinct from gate reachability.

Classification used a **deterministic function** (`classify_from_evidence_rows`) applied to the five source-level shortfall rows for each criterion. Decision logic (in order):

1. If max shortfall ≥ 3 → `public_satisfiable`.  
2. If max shortfall ≥ 2 → `partially_public_satisfiable`, except `operational_lifecycle_management` with direct fields → `public_satisfiable`.  
3. If max shortfall = 1 and direct fields present → `partially_public_satisfiable`.  
4. If max shortfall = 1 and evidence hint matches partial keywords without internal keywords → `partially_public_satisfiable`.  
5. If max shortfall = 1 and evidence hint matches internal keywords → `structurally_internal`.  
6. If max shortfall = 0 → `structurally_internal`.  

This partition describes **evidence requirement satisfiability from public schema**, not governance quality or legal compliance.

---

## 4.5 Public-evidence ceiling measurement

### Satisfiability analysis

For each evidence requirement, we computed:

- **Maximum evidence shortfall level** across the five sources (public-evidence ceiling).  
- **Source coverage counts:** number of sources at shortfall Levels 0, 1, and ≥ 2.  
- **Satisfiability class** (§4.4).  

Aggregated outputs: `outputs/criterion_satisfiability_summary.csv` (25 rows), `outputs/dimension_satisfiability_summary.csv` (5 rows).

### Gate reachability

A requirement was coded **`gate-unreachable from public inventories`** if (a) no source mapping assigned `can_potentially_satisfy_gate = True` and (b) maximum shortfall level < 4. Gate reachability is reported as a count and percentage of the 25 requirements. **Gate-unreachable does not mean the requirement is unimportant or unmet in practice**; it means public inventory fields alone cannot surface the primary artefacts needed for score ≥ 3.

### Shortfall measurement

The **shortfall distribution** reports how many of the 25 requirements fall at each Level 0–4 (maximum across sources). This distribution characterises heterogeneity in the public-evidence ceiling—distinguishing requirements with no public fields from those with partial programme-level signals.

### Dimension ceilings

For each governance dimension (five requirements), we computed:

- **Public satisfiability ceiling (%):** proportion of requirements classified as partially or publicly satisfiable.  
- **Gate-unreachable (%):** proportion of requirements gate-unreachable from public inventories.  
- **Mean maximum shortfall level:** average of requirement-level max shortfall scores within the dimension.  

Dimension ceilings describe **structural limits of public inventory schemas** by governance theme; they are not dimension-level governance scores.

### Minimum internal evidence set

For each gate-unreachable requirement, we exported the expected primary artefact type and a recommended internal source type (`outputs/minimum_internal_evidence_set.csv`) using `scripts/derive_minimum_internal_evidence.py`. This set specifies the **internal evidence floor**—artefact classes that must be sought outside public inventories to satisfy evidence gates. Derivation is a logical consequence of gate-unreachability and artefact specifications; it does not empirically observe internal records.

**The study evaluates satisfiability of evidence requirements from public inventory schemas, not governance quality, programme performance, or regulatory compliance.**

---

## 4.6 Robustness procedures

### Sensitivity analysis (partition scenarios)

We tested whether the public/internal partition was an artefact of classification stringency by reassigning requirements under three scenarios (`scripts/analyze_sensitivity.py`):

| Scenario | Rule |
|----------|------|
| **Baseline** | Deterministic classification (§4.4). |
| **Conservative** | Downgrade borderline `partially_public_satisfiable` requirements to `structurally_internal` when max shortfall ≤ 1 and no direct schema fields; downgrade `public_satisfiable` to `partially_public_satisfiable` when max shortfall < 3. |
| **Liberal** | Upgrade to `partially_public_satisfiable` when any source shows shortfall ≥ 1; upgrade to `partially_public_satisfiable` or `public_satisfiable` (lifecycle criterion) when max shortfall ≥ 2. |

For each scenario we recomputed partition counts and gate reachability. Outputs: `outputs/sensitivity_main_results.csv`, `outputs/sensitivity_scenarios.csv`.

### Unit commensurability (programme-record granularity)

Inventory entries vary in scope (minimal tool entries vs richly documented systems). To test whether the public-evidence ceiling depends on this heterogeneity, we filtered programme records under three **granularity scenarios** (`scripts/analyze_unit_commensurability.py`; rules in `unit_commensurability.py`) and recomputed population-adjusted shortfall where applicable:

| Scenario | Filter definition |
|----------|-------------------|
| **A — All records** | No filter (N = 7,434). |
| **B — Minimum information threshold** | Retain records at or above the source-specific 30th percentile of an **information score** (non-empty native field count + log-scaled description length + title length) **and** ≥ 4 non-empty native fields **and** description length ≥ 30 characters (N = 5,204; 70.0% retained). |
| **C — Exclude high complexity** | Exclude records at or above the source-specific 90th percentile of a **complexity score** (field count, log-scaled description length, agency-wide keyword matches, high-impact flags) (N = 6,685; 89.9% retained). |

Within each filtered corpus, mapped-field **population rates** were computed per source. Effective shortfall was downgraded when mapped fields were populated in fewer than 10% of filtered records (Level → 0) or fewer than 25% for direct-field mappings (Level → 1). Partition, gate reachability, and shortfall distribution were recomputed. Outputs: `outputs/unit_commensurability_summary.csv`, `outputs/unit_commensurability_sensitivity.csv`.

### Partition robustness (dual classifier)

We compared the deterministic partition against an **alternative heuristic classifier** (`scripts/validate_partition_robustness.py`) that applies keyword patterns to evidence hints and mapped field tokens (internal vs partial keywords). An optional local LLM endpoint (`LOCALGOVBENCH_LLM_ENDPOINT`) is supported in the script architecture; when unset, the heuristic classifier runs by default. Agreement was measured as the proportion of the 25 requirements with identical satisfiability class assignments. Outputs: `outputs/partition_validation_agreement.csv`, `outputs/partition_sensitivity_summary.csv`.

### Detector reliability (hide-field / recover-field)

To assess whether automated field detection could artefactually inflate or deflate shortfall levels, we implemented a **hide-field / recover-field evaluation** (`scripts/evaluate_detector_reliability.py`; specifications in `detector_reliability.py`):

1. For each source, select native structured fields used in mapping (29 field tests across five sources).  
2. For each record, **remove** one field from the structured JSON.  
3. Build recovery context from **remaining** native fields only (derived normalised columns excluded to prevent label leakage).  
4. Attempt deterministic recovery (substring match, categorical scan, token-set match, or boolean match).  
5. Compare recovered value to the original; compute precision, recall, F1, and exact-match rate.  

Empty original values were evaluated with empty predictions only (no spurious categorical matching). Outputs: `outputs/detector_reliability_summary.csv`, `outputs/detector_reliability_by_source.csv`.

---

## 4.7 Reproducibility

All analysis code, frozen configuration, and summary outputs are maintained in the open LocalGovBench repository under `localgovbench_measurement_validation/pilot_public_satisfiability/`. The end-to-end validation pipeline is executed via:

```bash
python3.12 scripts/run_validation_upgrade.py
python3.12 scripts/evaluate_detector_reliability.py
python3.12 scripts/analyze_unit_commensurability.py
```

**Key scripts**

| Script | Function |
|--------|----------|
| `scripts/build_pilot_corpus.py` | Download and normalise five-source corpus |
| `scripts/generate_localgovbench_criteria_config.py` | Generate criteria YAML from framework |
| `scripts/map_inventory_fields_to_criteria.py` | Build 125-row coverage matrix |
| `scripts/analyze_public_satisfiability.py` | Baseline summaries and figures |
| `scripts/validate_partition_robustness.py` | Dual-classifier agreement |
| `scripts/analyze_sensitivity.py` | Conservative/liberal scenarios |
| `scripts/derive_minimum_internal_evidence.py` | Internal evidence floor export |
| `scripts/evaluate_detector_reliability.py` | Hide-field recovery tests |
| `scripts/analyze_unit_commensurability.py` | Granularity scenarios |

**Frozen outputs package** (authoritative numeric results for this manuscript: see `paper_data_policy/results_freeze.md`):

- `data/pilot_programme_records.csv`, `data/source_registry_expanded.csv`  
- `outputs/field_criterion_coverage_matrix.csv`  
- `outputs/criterion_satisfiability_summary.csv`, `outputs/dimension_satisfiability_summary.csv`  
- `outputs/sensitivity_main_results.csv`, `outputs/unit_commensurability_summary.csv`  
- `outputs/partition_validation_agreement.csv`, `outputs/detector_reliability_by_source.csv`  
- `outputs/minimum_internal_evidence_set.csv`  
- `figures/` (publication figures per `paper_data_policy/figure_plan.md`)  

**Zenodo archive.** A versioned deposit bundling the normalised corpus (or source download scripts where size limits apply), frozen CSV outputs, figure reproduction scripts, and the criteria configuration will be archived on Zenodo with the placeholder identifier **10.5281/zenodo.PLACEHOLDER** (to be replaced upon deposit). The repository DOI for LocalGovBench v0.1.2 instrument artefacts will be cited as a related identifier. Collection scripts re-fetch primary sources from official URLs documented in Table 1 (`source_registry_expanded.csv`) to support independent verification.

---

## Document statistics

| Section | Word count |
|---------|----------:|
| 4.1 Research design | 377 |
| 4.2 LocalGovBench evidence-requirement specification | 464 |
| 4.3 Corpus construction | 403 |
| 4.4 Criterion-to-evidence mapping | 347 |
| 4.5 Public-evidence ceiling measurement | 308 |
| 4.6 Robustness procedures | 496 |
| 4.7 Reproducibility | 241 |
| **Total (§4 Methods)** | **2,636** |

*Word counts exclude table content, code block, and this statistics section.*

---

## Missing citations to add later

The following references should be inserted during integration with the full manuscript bibliography:

1. **US OMB 2025 AI Use Case Inventory** — official policy mandate and inventory publication (M-24-10 or successor OMB guidance).  
2. **Government of Canada AI Register** — MVP launch and Open Government dataset documentation.  
3. **Dutch Algoritmeregister** — Algorithmic Transparency Standard and bulk export API.  
4. **EU Public Sector Tech Watch (JRC)** — dataset documentation and PID `http://data.europa.eu/89h/e8e7bddd-8510-4936-9fa6-7e1b399cbd92`.  
5. **UK Algorithmic Transparency Recording Standard (ATRS)** — GOV.UK policy standard and Search API.  
6. **LocalGovBench v0.1 instrument** — repository/Zenodo deposit for framework provenance (existing v0.1.2 DOI).  
7. **EU AI Act (Regulation (EU) 2024/1689)** — if cited in criterion background (legal dimension context only; no compliance claim).  
8. **Trustworthy AI / HLEG or OECD AI principles** — if criterion traceability is discussed in §3 cross-reference.  
9. **Public-sector algorithm transparency literature** — policy context for programme inventories (e.g., algorithm registers as transparency instruments).  
10. **Reproducibility / open government data methods** — Data & Policy methodological framing if required by reviewers.
