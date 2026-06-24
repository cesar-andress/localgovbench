# Pilot report — public satisfiability of LocalGovBench evidence requirements

**Study framing:** quantify the **public-satisfiability ceiling** of LocalGovBench v0.1 evidence requirements using official AI programme inventories. **No readiness scores** are produced.

## Pilot corpus

- **Programme records:** 4023
- **Sources:** CA-GC-AI-REG (412), US-OMB-2025 (3611)
- **Official URLs only** (US OMB 2025 GitHub CSV; Canada Open Government CSV)

## Key findings

- **Structurally internal (preliminary):** 17/25 (68.0%)
- **Partially or publicly satisfiable:** 8/25 (32.0%)
- **Score ≥3 gate unreachable from inventory fields:** 100.0% of criteria
- **Criteria with ≥1 direct inventory field mapping:** 3

### Publicly satisfiable (preliminary class)

- `operational_lifecycle_management`
- *(none)*

### Partially publicly satisfiable

- `legal_regulatory_ai_act_alignment`
- `organizational_accountability`
- `organizational_ownership`
- `organizational_procurement_governance`
- `operational_monitoring`
- `operational_human_oversight`
- `strategic_sovereignty_vendor_independence`

### Structurally internal

- `legal_regulatory_gdpr_readiness`
- `legal_regulatory_data_retention`
- `legal_regulatory_lawful_basis`
- `legal_regulatory_cross_border_avoidance`
- `technical_security_local_architecture`
- `technical_security_access_control`
- `technical_security_logging`
- `technical_security_auditability`
- `technical_security_model_updates`
- `organizational_role_definition`
- `organizational_risk_ownership`
- `operational_incident_response`
- `operational_documentation`
- `strategic_sovereignty_data_sovereignty`
- `strategic_sovereignty_infrastructure_control`
- `strategic_sovereignty_portability`
- `strategic_sovereignty_maintainability`

## Viability questions

### Is the public-satisfiability framing viable?

**Yes.** Inventories provide programme-level metadata but cannot supply named primary artefacts required for LocalGovBench score ≥3 gates. The pilot quantifies this ceiling rather than inferring readiness.

### Does this avoid Paper 2 overlap?

**Yes, if boundaries hold.** This pilot:

- uses **national AI use-case registers**, not the Paper 2 municipal documentary corpus;
- maps **inventory schema fields** to evidence requirements;
- does **not** analyse procurement/vendor stewardship, document genres, registers vs strategies, or Documentary Accountability Architecture;
- does **not** perform municipal documentary observability analysis.

### Does this avoid readiness scoring?

**Yes.** Outputs are coverage/satisfiability classes only. No maturity scores, rankings, or readiness indices are computed.

### Is the result non-trivial enough for a paper?

**Likely yes.** 100.0% of criteria show score ≥3 gates unreachable from public fields; 68.0% are structurally internal. This supports a claim that programme-level readiness evidence is largely non-observable in public inventories.

### Should the project proceed to full corpus collection?

**Proceed selectively.** Expand to NL Algoritmeregister and EU PSTW for robustness across jurisdictions, but **do not** pivot to readiness scoring. Pair with Delphi + confidential dossiers for instrument validation.

## Dimension ceilings

| Dimension | Partial/public ceiling % | Gate unreachable % |
|-----------|-------------------------:|-------------------:|
| Legal and Regulatory Compliance | 20.0 | 100.0 |
| Operational Management | 60.0 | 100.0 |
| Organizational Governance | 60.0 | 100.0 |
| Strategic Sovereignty | 20.0 | 100.0 |
| Technical and Security Readiness | 0.0 | 100.0 |

## Figures

- `figures/criterion_satisfiability_heatmap.png`
- `figures/dimension_public_ceiling_barplot.png`
- `figures/gate_reachability_by_dimension.png`

## Pilot GO decision

**GO**

| Check | Pass |
|-------|------|
| at_least_300_records | yes |
| partition_non_trivial | yes |
| at_least_30pct_structurally_internal_or_gate_unreachable | yes |
| at_least_25pct_partially_public_satisfiable | yes |
| paper2_boundary_documented | yes |

