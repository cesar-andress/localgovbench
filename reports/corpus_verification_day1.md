# Day-1 corpus verification — LocalGovBench measurement-validation study

**Study label:** `localgovbench_measurement_validation`  
**Working folder:** `localgovbench_measurement_validation/`  
**Collection date:** 2026-06-24  
**Purpose:** Determine whether official **public programme/use-case inventories** can support
**psychometric validation** of the LocalGovBench v0.1 25-criterion instrument for Paper 1,
**without overlapping** Paper 2 (*Vendor Stewardship in the Public Record*, under review).

**Scope of this document:** corpus verification only. No scoring model, no LocalGovBench coding,
no manuscript drafting.

---

## 1. Repository context inspected

Relevant existing assets (not used as corpus here):

| Area | Role |
|------|------|
| `localgovbench/framework/dimensions.py` | Frozen 25 criteria / 5 dimensions (instrument SoT) |
| `validation/content_validity/delphi/` | Delphi Round 1 package (content validity track) |
| `validation/dossier/` | Confidential dossier protocol (preferred field design) |
| `exports/delphi_round1/` | Participant materials for Delphi |
| `paper/data/open_pilot/` | **Paper 2 corpus — excluded** |

Paper 1 repositioning under test: **empirical measurement-validation** using **official public
programme inventories**, distinct from Paper 2’s municipal documentary observability design.

---

## 2. Paper 2 firewall (hard exclusions)

This verification **did not** use or inspect:

- Paper 2 open-document / open_pilot municipal corpus
- Documentary Accountability Architecture
- Document-genre taxonomy (strategies vs registers/portals)
- Procurement/vendor stewardship as a central analytic frame

**Residual overlap risk:** any future study that codes **public transparency registers** as primary
evidence may still **look adjacent** to Paper 2 unless the research question, unit, and claims are
clearly separated (see §7).

---

## 3. Candidate sources summary

Machine-readable inventory: `data/corpus_candidates_day1.csv`

| Source ID | Jurisdiction | Est. entries | Machine-readable | Programme-level? |
|-----------|--------------|-------------:|------------------|------------------|
| US-OMB-2025 | US federal | **3,611** | Yes (CSV) | Yes (use cases) |
| US-OMB-2024 | US federal | ~1,750 | Yes (CSV) | Yes |
| NL-ALGO-REG | Netherlands | **~1,400** | Partial (bulk CSV/XLS) | Mostly (algorithms) |
| EU-PSTW | EU multi-country | **2,291** (1,803 AI) | Yes (CSV) | Mostly (cases) |
| CA-GC-AI-REG | Canada federal | **658** | Yes (CSV) | Yes (AI systems) |
| UK-ATRS | UK | **133** | Partial (Search API) | Yes (tools) |
| AU-DTA-STATEMENTS | Australia | ~114 agencies | No (use-case rows) | **No** |
| OECD-AI-POLICY | OECD curated | ~200 | No bulk | Partial |

### 3.1 United States — OMB 2025 Federal AI Use Case Inventory

- **URL:** https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory  
- **File:** `Data/2025_individually_reported_AI_use_cases.csv`  
- **Verified count:** **3,611** parsed rows (2026-06-24)  
- **Fields (sample):** agency, use_case_name, development_stage, is_high_impact, topic_area,
  classification (incl. Generative AI), vendor_name, ATO flags, training data notes, etc.  
- **Access:** Official GitHub; public releasability; some withheld/national-security omissions.  
- **Programme unit:** Each row is a bounded agency AI use case — plausible programme proxy.  
- **LocalGovBench fit:** Strong **volume**, weak **construct** (federal not municipal; not sovereign
  LLM-specific; register text ≠ evidence-gated dossier artefacts).

### 3.2 Netherlands — Algoritmeregister

- **URL:** https://algoritmes.overheid.nl/  
- **Estimated count:** **~1,394–1,442** public algorithm descriptions (site counter, 2026-06-24)  
- **Export:** Bulk CSV/Excel via “Download all algorithms”; metadata standard documented at
  https://standaard.algoritmeregister.org/  
- **Programme unit:** Algorithm/system entries from ministries, agencies, **and municipalities** —
  closer to local government than US federal, but unit is **algorithm** not **LLM programme**.  
- **Access:** Open government publication; English machine-translated; moving toward mandatory
  registration.  
- **LocalGovBench fit:** Best **European local-government mix** among statutory-style registers;
  still transparency metadata not internal governance dossiers.

### 3.3 EU — Public Sector Tech Watch (JRC)

- **URL:** https://interoperable-europe.ec.europa.eu/collection/public-sector-tech-watch/pstw-cases-viewer-data-download  
- **File:** `pstw_dataset.csv` (June 2026 attachment)  
- **Verified count:** **2,291** rows; **1,803** with Primary Technology = AI  
- **Local government subset:** **~668** rows tagged Local Government (incl. spelling variants)  
- **GenAI/LLM signal:** **~67** rows with generative/LLM keywords in description/keywords (Day-1
  text scan — not manual validation)  
- **Licence:** CC-BY 4.0  
- **Caveat:** Curated observatory, not a legal inventory; selection bias.  
- **LocalGovBench fit:** Useful for **European heterogeneity** and subnational coverage; uneven depth.

### 3.4 Canada — GC AI Register (MVP)

- **URL:** https://open.canada.ca/data/en/dataset/fcbc0200-79ba-4fa4-94a6-00e32facea6b  
- **Verified count:** **658** CSV rows (Apr 2026 export downloaded 2026-06-24)  
- **Fields:** system name, organisation, description, status, vendor, capabilities, data sources,
  personal information flags  
- **Programme unit:** One row ≈ one AI system / use case (MVP; incomplete fields).  
- **LocalGovBench fit:** Adds second national jurisdiction; federal not municipal.

### 3.5 United Kingdom — ATRS / GOV.UK register

- **URL:** https://www.gov.uk/algorithmic-transparency-records  
- **Verified count:** **133** records via GOV.UK Search API (`algorithmic_transparency_record`)  
- **Machine-readable path:** Search API pagination; no official bulk CSV  
- **Programme unit:** One ATRS record ≈ one algorithmic tool / use context — high-quality narrative
  but **small n**.  
- **LocalGovBench fit:** Quality benchmark only; insufficient alone for psychometric n.

### 3.6 Australia — transparency statements

- **URL:** https://www.digital.gov.au/policy/ai/list-of-transparency-statements  
- **Finding:** Central **index of agency statements**; **internal use-case registers are not
  published** as open data.  
- **Conclusion:** **Not viable** for 300+ programme-level records.

### 3.7 OECD / EU AI Act database

- **OECD.AI:** policy/case narratives — **no bulk programme inventory**.  
- **EU AI Act public database:** emerging provider/register infrastructure — **not yet** a usable
  municipal programme corpus for Day 1.

---

## 4. Aggregate corpus arithmetic (official public sources only)

| Metric | Value |
|--------|------:|
| Largest single source | 3,611 (US OMB 2025) |
| Sum of top independent inventories (deduplicated naïvely) | **~8,000+** rows |
| Jurisdictions with ≥300 programme-like rows | **≥4** (US, NL, EU-PSTW, CA) |
| Jurisdictions with ≥600 rows | **≥3** (US, NL, EU-PSTW) |
| Municipal/local-tagged rows (PSTW only, verified) | ~668 |
| Municipal sovereign LLM programmes (verified) | **Not enumerated Day 1** — likely **≪300** |

**Important:** naïve summation **double-counts** conceptually similar cases across catalogues.
Research design must pick **one primary registry family** or a deduplicated merge protocol.

---

## 5. Suitability for LocalGovBench psychometric validation

LocalGovBench v0.1 assumes:

- unit = **bounded municipal LLM/AI programme**;
- evidence = **confidential programme dossier** with quotable artefacts;
- scoring = **evidence-gated 0–4 maturity** by independent assessors.

Public inventories provide:

- **self-declared metadata** (purpose, stage, vendor, sometimes oversight);
- **not** RoPA extracts, contracts, runbooks, IR plans, or architecture dossiers;
- **mixed technology** (classical ML, rules, GenAI, Copilot seats).

### What psychometric work is realistically supported

| Validation type | Feasible on public inventories? |
|-----------------|-----------------------------------|
| Delphi content validity | Yes (separate track; already prepared) |
| Item response on **register-field proxies** | Partial — requires **new coding rubric**, not full 25-criterion gates |
| Factor structure / dimensionality of **inventory fields** | Possible — but tests **register schema**, not LocalGovBench construct directly |
| Inter-rater reliability on **full evidence-gated LocalGovBench** | **No** — insufficient artefact depth |
| Confirmatory validation of **sovereign municipal LLM readiness** | **No** — wrong population |

---

## 6. Paper 2 non-overlap assessment

| Dimension | Paper 2 (under review) | Proposed Paper 1 inventory path | Overlap risk |
|-----------|------------------------|----------------------------------|--------------|
| Corpus | 20-municipality public document corpus | Multi-jurisdiction AI use-case registers | **Medium** (both public-sector AI transparency) |
| Method | Documentary observability / genres | Register metadata psychometrics | **Low–medium** if claims differ |
| Construct | Documentary accountability / vendor stewardship | Programme-level governance readiness | **Medium** if both discuss “what registers show” |
| Geography | Europe + N. America cities | US + EU + NL + CA (+ UK) | **Low** if municipal cases disjoint |

**To avoid salami slicing:** Paper 1 must **not** analyse municipal strategy PDFs, portal
coverage, or procurement observability. It should treat inventories as **structured administrative
disclosures of AI programmes**, reporting **measurement properties** of mapping LocalGovBench
criteria onto **available public fields** — or use inventories only as **sampling frame** for
recruiting confidential dossiers (hybrid design).

---

## 7. Legal and access constraints (pessimistic)

| Risk | Severity | Mitigation |
|------|----------|------------|
| US withheld / national-security omissions | Medium | Document selection bias; no imputation |
| EU PSTW CC-BY attribution | Low | Cite JRC; respect licence |
| NL translation errors | Medium | Use Dutch source fields where possible |
| Scraping GOV.UK at scale | Medium | Use official Search API; respect rate limits |
| Re-identification from rare use cases | Medium | Aggregate reporting; no municipal league tables |
| Paper 2 corpus contamination | **High** if shared cases | Maintain disjoint case list |

No Day-1 source flagged as **legally prohibitive** for small-sample inspection; bulk reuse requires
licence/attribution review per source.

---

## 8. Day-1 actions not taken (by design)

- No large dataset downloads archived in repo (only header/row-count verification)
- No LocalGovBench scoring
- No Paper 2 asset access
- No synthetic responses

---

## 9. Go / no-go recommendation

### 9.1 Corpus volume criterion (pre-specified thresholds)

| Threshold | Result |
|-----------|--------|
| **≥300 programme-level records** from official public sources | **GO** — exceeded by US (3,611), NL (~1,400), PSTW AI (~1,803), CA (658) individually |
| **≥600 records across ≥2 jurisdictions** | **STRONG GO** — US + NL, or US + PSTW, or NL + PSTW easily satisfy |
| Too small / inaccessible / legally fragile | **Not triggered** for major official inventories |

**Volume verdict:** **STRONG GO**

### 9.2 Paper 1 rescue criterion (measurement-validation without Paper 2 overlap)

**CONDITIONAL NO-GO** for the naïve design: *“Psychometrically validate all 25 evidence-gated
LocalGovBench criteria by coding public inventories as primary evidence.”*

Reasons:

1. **Construct mismatch** — inventories are not municipal sovereign LLM programme dossiers.  
2. **Evidence depth mismatch** — public fields cannot support evidence-gated scoring ≥3/4.  
3. **Paper 2 adjacency** — public AI transparency registers risk editorial classification as
   overlapping observability research unless methods and claims are tightly bounded.  
4. **Municipal n** — local-government programme rows exist (esp. NL + PSTW) but **verified sovereign
   LLM municipal n** is likely far below 300.

### 9.3 Recommended path if proceeding (Day-2 pointer, not implemented here)

**Hybrid STRONG GO:**

- **Primary psychometric evidence:** Delphi (already packaged) + **confidential dossiers** (n small).  
- **Secondary structural pilot (optional):** use **US OMB + NL register + PSTW** to test **field
  availability mapping** (which criteria have any public proxy field) — report as **feasibility
  analysis**, not maturity validation.  
- **Explicit paper claim:** “public inventories insufficient for evidence-gated readiness scoring;
  Delphi + dossier field study validates instrument where registers cannot.”

---

## 10. Final recommendation (single line)

**Corpus acquisition: STRONG GO. Paper 1 full LocalGovBench psychometric validation on public
inventories alone: NO-GO.** Proceed only with a **hybrid** design that keeps Paper 2 exclusions and
does not treat register metadata as dossier-equivalent evidence.

---

## References (verified 2026-06-24)

- OMB 2025 inventory: https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory  
- Dutch Algorithm Register: https://algoritmes.overheid.nl/  
- EU PSTW download: https://interoperable-europe.ec.europa.eu/collection/public-sector-tech-watch/pstw-cases-viewer-data-download  
- Canada AI Register: https://open.canada.ca/data/en/dataset/fcbc0200-79ba-4fa4-94a6-00e32facea6b  
- UK ATRS hub: https://www.gov.uk/algorithmic-transparency-records  
- GOV.UK Search API (133 ATRS records verified programmatically)

---

*Day-1 corpus verification — LocalGovBench measurement-validation study*
