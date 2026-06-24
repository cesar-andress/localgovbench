# Title, abstract, and keywords

## Recommended title

**The Public-Evidence Ceiling of AI Programme Governance Requirements: A Multi-Inventory Analysis of LocalGovBench Evidence Gates**

## Alternative titles

1. **What Public AI Inventories Can and Cannot Prove: Evidence-Requirement Satisfiability Across Five Official Registers**
2. **Programme Transparency Metadata and Governance Evidence Gates: A 7,434-Record Public-Evidence Ceiling Study**

---

## Structured abstract (draft, ~280 words)

**Background.** Governments are publishing machine-readable inventories of public-sector AI programmes as transparency instruments. Assessment frameworks such as LocalGovBench v0.1 specify programme-level **evidence requirements** with score ≥3 **evidence gates** that call for named primary artefacts (e.g., risk registers, architecture diagrams, incident response plans). It remains unclear how far official public inventories can satisfy those requirements—a question distinct from measuring AI governance readiness.

**Objective.** To quantify the **public-evidence ceiling** of LocalGovBench evidence requirements using five official programme-level data sources, without assigning readiness scores or ranking jurisdictions.

**Methods.** We assembled 7,434 normalised programme records from the 2025 US OMB AI Use Case Inventory (n=3,611), the Government of Canada AI Register (n=412), the Dutch National Algorithm Register (n=1,484), EU Public Sector Tech Watch AI-primary cases (n=1,794), and UK Algorithmic Transparency Records (n=133). For each of 25 evidence requirements, we mapped native inventory schema fields to requirement types, assigned an **evidence shortfall** level (0–4), classified requirements as structurally internal or partially/publicly satisfiable, and tested robustness via conservative/liberal sensitivity scenarios, unit commensurability filters, and hide-field detector reliability evaluation. **No readiness scores were assigned; no programme or jurisdiction was ranked.**

**Results.** Baseline partition: 15/25 (60%) structurally internal, 10/25 (40%) partially or publicly satisfiable. **Evidence gate ≥3 was reachable for 0/25 criteria**; maximum observed shortfall level was 2 (partial programme-level signal). Shortfall distribution: L0=7, L1=10, L2=8, L3=0, L4=0. Gate unreachability remained 100% under conservative (84% internal) and liberal (72% partial-public) scenarios and under all unit-commensurability filters (7,434 / 5,204 / 6,685 records). Detector precision was 1.000; extraction errors were false negatives and cannot explain absent gate-reachable evidence.

**Conclusions.** Official inventories provide metadata and **partial signals** but do not satisfy LocalGovBench evidence gates from public fields alone. The contribution is a reproducible **public-evidence ceiling** estimate and a **minimum internal evidence set** (25/25 criteria) for programme-level AI governance assessment—informing policy design without equating transparency publication with governance proof.

---

## Keywords (7)

1. public-sector AI
2. algorithmic transparency
3. evidence requirements
4. AI governance
5. programme inventories
6. policy evaluation
7. reproducible research
