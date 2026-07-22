# Supplement C — Disclosure Functions v1

## Purpose

Provide the citable overview of the **normative Disclosure Functions v1 catalogue**: measurement construct, unit of analysis, core functions, modules, applicability defaults, and anti-over-credit principles.

Authoritative definitions remain in YAML. This supplement does **not** replace the normative file and does **not** report coding outcomes.

## Inputs

| Input | Path |
|-------|------|
| Normative function catalogue | `affordance/config/disclosure_functions_v1.yaml` |
| Applicability overrides | `affordance/config/applicability_overrides_v1.yaml` |
| Field→function candidates | `affordance/config/field_function_candidates_v1.csv` |
| Realization rules (specified; empirical tables later) | `affordance/config/realization_rules_v1.yaml` |
| Linkage field types | `affordance/config/linkage_field_types_v1.csv` |

**Meta (from catalogue):** specification version `1.0.0`; measurement construct `schema_disclosure_affordance`; primary unit `schema_x_disclosure_function`; secondary unit (planned) `record_level_realization`.

## Outputs

The catalogue itself is the output of Phase 1 authoring (hand-maintained, validated). Downstream consumers:

- schema coding template (55 units) — Supplement D;  
- experiment matrix schema — Supplement F.

### Table C1 — Disclosure Functions v1 (core + modules)

| Function ID | Display name | Tier | Status | Default applicability |
|-------------|--------------|------|--------|------------------------|
| `cf_system_identity` | System or use-case identity | core | `core_unscored` | universal |
| `cf_purpose` | Purpose | core | `core_scored` | universal |
| `cf_operational_status` | Operational status | core | `core_scored` | universal |
| `cf_accountable_body` | Accountable body identification | core | `core_scored` | universal |
| `cf_data_involvement` | Data involvement | core | `core_scored` | universal |
| `om_human_oversight` | Human oversight description | module | `module` | object_specific |
| `om_risk_or_impact` | Risk or impact designation | module | `module` | object_specific |
| `om_legal_basis` | Legal basis | module | `module` | jurisdiction_specific |
| `om_supplier` | Supplier identification | module | `module` | universal |
| `om_technical_method` | Technical method or capability | module | `module` | universal |
| `om_redress_pointer` | Redress pointer | module | `module` | conditional |

**Source:** `affordance/config/disclosure_functions_v1.yaml` (`core_functions`, `modules`).

### Construct boundaries (from catalogue principles)

Functions describe **disclosure capabilities a public inventory schema may support**. They do **not** describe governance quality, AI maturity, organisational readiness, benchmarking, or compliance. Prohibited constructs in the normative meta include readiness, maturity, shortfall, composite scores, jurisdiction ranking, and compliance scores.

Anti-over-credit rules (generic narrative fields, dedicated-exists-blocks-generic, UK description policy, affordance ≠ realization) are normative in the same YAML; operational restatement for coders is in the codebook (Supplement D).

## Figures

None. The catalogue is definitional; no results figure is implied.

## Limitations

1. **Default applicability is specification input**, not the coder’s final applicability judgment (see coding columns in Supplement D).  
2. **Candidate fields are not automatic credits** — human coding decides support level.  
3. **Realization rules** are specified for a later empirical stage; this repository’s Phase 3 pipeline must not be read as having completed realization analysis (Supplement F).  
4. Rejected candidates and extensibility policy live in the YAML; consult the file for full text.

## Cross references

| Topic | See |
|-------|-----|
| Observed fields | [Supplement B](B_observed_schema_inventory.md) |
| Human coding | [Supplement D](D_coding_framework.md) |
| Label enumerations | [Supplement E](E_validation_rules.md) |
| Full normative catalogue | `affordance/config/disclosure_functions_v1.yaml` |
| Package overview | `affordance/README.md` |
