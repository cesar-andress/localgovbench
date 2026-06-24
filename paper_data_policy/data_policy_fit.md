# Data & Policy fit statement

## Why this manuscript belongs in Data & Policy

### 1. Reproducible dataset and pipeline as first-class contribution

Data & Policy explicitly values **data-driven policy research** with reproducible artifacts. This paper delivers:

- A **7,434-record normalised corpus** from five official government/EU sources
- Documented acquisition URLs, filters, and collection metadata (`source_registry_expanded.csv`)
- A scripted pipeline (`run_validation_upgrade.py`) regenerating all tables and figures
- Frozen CSV outputs for audit (`results_freeze.md`)

This aligns with the journal’s interest in **what public data can support** in policy analysis—not only narrative policy commentary.

### 2. Direct policy relevance

The study addresses a live policy design question: as governments expand **AI programme inventories** (OMB mandates, Algoritmeregister, EU AI Act transparency tools), can those registers support **evidence-gated governance assessment**?

The answer—**partial signals yes, evidence gates no**—informs:

- Transparency policy (what to publish vs what to keep in dossiers)
- Assessment protocol design (internal evidence floor specifications)
- Proportionate expectations for auditors and regulators

### 3. Public-sector AI governance without overclaim

Data & Policy readers expect **bounded claims**. The manuscript:

- Does not rank jurisdictions
- Does not assign readiness scores
- Separates public metadata from internal evidence requirements
- Provides a **minimum internal evidence set** as a policy planning tool

### 4. Transparent, auditable methods

Methods are rule-based and documented:

- Source-schema mapping rules (`mapping_rules.py`)
- Graded evidence shortfall scale (0–4)
- Sensitivity analysis (conservative/liberal)
- Unit commensurability proxies
- Detector reliability (hide-field / recover-field)

Reviewers can inspect logic without proprietary models.

### 5. Multi-jurisdiction empirical scope

Five inventories across North America and Europe (7,434 records) exceed typical single-register policy notes, supporting **comparative public-administration relevance** without league tables.

### 6. Artifact contribution suitable for open deposit

Package suitable for Zenodo/OSF:

- Normalised corpus (or download scripts if CSV too large)
- Mapping rules + criteria config
- All summary CSVs and figures
- README with one-command reproduction

Data & Policy’s readership includes practitioners building **policy data infrastructures**—this paper is an empirical stress test of one such infrastructure class.

---

## Fit relative to Information Polity (fallback)

Strong overlap on **algorithmic transparency**, **public sector information**, and **governance of digital government**. Slightly less emphasis on theoretical IR/governance theory; strengthen normative framing in discussion if submitting there.

---

## Deliberate non-fit: Government Information Quarterly

Not optimised for GIQ because:

- No full psychometric instrument validation (Delphi/dossiers deferred)
- No municipal case ethnography
- Ceiling study is **policy data** paper, not e-government implementation study

GIQ remains venue for dossier validation wave later.

---

## Suggested Data & Policy article type

**Research article** (empirical + method + policy implications) with **data descriptor** elements in Methods/Data availability.

Optional companion **data note** if journal scope allows separate corpus publication—otherwise integrated Methods + OSF deposit.
