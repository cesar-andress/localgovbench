# Contribution statement (one page)

## Theoretical contribution

The paper reframes AI governance assessment research from **readiness measurement** to **public-evidence ceiling analysis**. It distinguishes (a) transparency metadata published in official programme inventories, (b) partial programme-level signals inferable from inventory fields, and (c) named primary artefacts required by evidence-gated assessment protocols. This tri-level distinction offers a policy-theoretic account of why transparency registers and dossier-based assessment serve complementary—not substitutable—functions in public-sector AI governance.

## Methodological contribution

We provide a reproducible **source-schema-to-evidence-requirement satisfiability** protocol:

- Normalised multi-jurisdiction corpus construction from official APIs/downloads only
- Graded **evidence shortfall** scale (0–4) tied to LocalGovBench gates
- Deterministic public/internal partition with dual-classifier robustness check (92% agreement)
- Conservative/liberal sensitivity analysis on partition rules
- Unit commensurability stress test for programme-record granularity
- Hide-field detector reliability evaluation separating false positives from false negatives

The pipeline is scripted, frozen, and re-runnable (`run_validation_upgrade.py`); it produces auditable CSV outputs rather than opaque scores.

## Empirical contribution

- **7,434 programme records** across five official sources (US, Canada, Netherlands, EU PSTW, UK ATRS)
- **25 evidence requirements** mapped to inventory schemas
- **0/25 gate-reachable** from public inventories; max shortfall level **2**
- **Minimum internal evidence set** covering all 25 criteria (5 per governance dimension)
- Robustness bundle: sensitivity scenarios, commensurability filters, detector reliability (precision = 1.000)

## Practical contribution

For policy designers and assessment practitioners:

- Identifies which evidence types must remain **internal** (dossiers, security records, contracts) even when inventories expand
- Shows where inventories already supply **partial signals** (lifecycle, human oversight, lawful basis in NL register)
- Provides a template for evaluating future registers (EU AI Act database, municipal algorithms) against explicit evidence gates rather than checklist overlap
- Supports proportionate transparency policy: publish metadata without implying that publication satisfies assessment gates

## Distinction from the rejected original LocalGovBench paper

| Original (rejected) framing | Paper 1 (this manuscript) |
|----------------------------|---------------------------|
| Municipal governance **readiness** scoring | **Public-evidence ceiling** of requirements |
| Readiness indices and maturity scores | Shortfall levels and gate reachability only |
| Claim risk: infer governance quality from public data | Explicit **non-claim**: no governance quality assessment |
| Single-jurisdiction or observational pilot | Five-source, 7k+ record reproducible corpus |
| Psychometric validation implied | Instrument slice + ceiling analysis; Delphi/dossiers deferred |

**Reuse from old text:** dimension definitions, criterion statements, evidence hints, AI Act/GDPR mapping tables (methods background only).

**Delete from old text:** readiness score reporting, municipal ranking language, “validates LocalGovBench as benchmark,” GIQ-first positioning, observability/disclosure framing.

## Distinction from Paper 2 (Vendor Stewardship in the Public Record)

| Paper 2 | Paper 1 |
|---------|---------|
| Municipal **documentary** corpus (20 cities) | **National/EU programme inventories** |
| Document genres, registers vs strategies | **Inventory schema fields** |
| Vendor stewardship central claim | Vendor fields as weak proxies only; not central |
| Documentary Accountability Architecture (DAA) | Not used |
| Observability of public records | **Public-evidence ceiling** language |

**Firewall:** No Paper 2 corpus (`paper/data/open_pilot/`); no genre comparison; no DAA constructs.
