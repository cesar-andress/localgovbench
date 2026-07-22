# Codebook — Schema Disclosure Affordance v1

**Specification version:** 1.0.0  
**Coding layer version:** 1.0.0  
**Unit of analysis:** `schema_object × disclosure_function`  
**Construct:** schema disclosure affordance (not readiness, maturity, shortfall, compliance, or governance quality).

## Global coding labels

| Attribute | Allowed values |
|-----------|----------------|
| Support level | `dedicated`, `indirect`, `absent` |
| Applicability | `universal`, `conditional`, `jurisdiction_specific`, `object_specific`, `catalogue_inapplicable`, `unknown` |
| Encoding type | `free_text`, `structured`, `mixed`, `other`, `not_applicable` |
| Documentary linkage layer | `generic_url`, `record_locator`, `function_specific`, `none`, `not_applicable` |
| Confidence | `high`, `medium`, `low` (metadata only; never changes support) |

## Support level definitions

- **dedicated:** Schema exposes a field whose native role is to host this disclosure function.
- **indirect:** Schema exposes only a proxy or adjacent field that may carry related information without being dedicated.
- **absent:** No dedicated or acceptable indirect host for this function on this schema object.

When applicability is `catalogue_inapplicable`, do **not** assign `dedicated` or `indirect`. Use support `absent` with encoding/linkage `not_applicable`, or follow the pilot sheet instruction for N/A marking while keeping support=`absent`.

## Global anti-over-credit rules

- **generic_dedicated_once:** A generic narrative field (description, Description, description_short, additional information, notes, summary) may receive at most one dedicated support credit, and only for the function named in generic_field_policy (normally purpose).
- **dedicated_exists_blocks_generic:** If a dedicated candidate field exists for a function, a generic narrative field must not be coded dedicated for that function.
- **uk_description_indirect_purpose:** UK-ATRS description is at most INDIRECT for purpose; never PRIMARY dedicated.
- **affordance_ne_realization:** Record content richness must not retroactively upgrade schema dedicatedness.

## Prohibited coder behaviours

- Inferring undisclosed content or organisational quality.
- Using record population rates to decide schema support.
- Treating a generic URL as function-specific evidence without an explicit field role.
- Using LocalGovBench, readiness, maturity, shortfall, or compliance concepts.
- Consulting external pages unless the coding round explicitly authorizes documentation review.

---

## cf_system_identity — System or use-case identity

- **Identifier:** `cf_system_identity`
- **Display name:** System or use-case identity
- **Tier:** `core`
- **Scoring role:** `descriptive_only`
- **Normative definition:** Stable public identifier and/or name that makes the inventory entry addressable as a distinct system, use case, algorithm, or case.
- **Primary coding question:** Does the schema expose a dedicated identity or naming field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `identity_titles_allowed`
- **Documentary linkage relevance:** `record_locator`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `name_ai_system_fr` | French alias; EN canonical for realization. |
| CA-GC-AI-REG | PRIMARY | `name_ai_system_en` | English system name (canonical). |
| CA-GC-AI-REG | SECONDARY | `ai_register_id` | Register identifier. |
| EU-PSTW | PRIMARY | `Name` | Case name. |
| EU-PSTW | SECONDARY | `PSTW ID` | Case identifier. |
| NL-ALGO-REG | PRIMARY | `name` | Algorithm name. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | REJECTED | `source_id` | Sparse/noisy identifier. |
| NL-ALGO-REG | SECONDARY | `algorithm_id` | Stable algorithm id. |
| UK-ATRS | PRIMARY | `title` | Record title. |
| UK-ATRS | REJECTED | `format` | Document type metadata. |
| UK-ATRS | REJECTED | `index` | Search index metadata. |
| UK-ATRS | SECONDARY | `link` | Record locator path. |
| US-OMB-2025 | PRIMARY | `use_case_name` | Public use-case title. |
| US-OMB-2025 | REJECTED | `system_name_ato` | ATO system label, not inventory identity. |
| US-OMB-2025 | SECONDARY | `id` | Agency-side identifier; not always populated. |

### Positive examples

- US `use_case_name`; NL `name`; UK `title`.

### Negative examples / non-examples

- US `system_name_ato`; NL `source_id`; UK `format`/`index`.

### Source-specific caveats

- Descriptive only; do not use in scored affordance profiles.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `cf_system_identity`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## cf_purpose — Purpose

- **Identifier:** `cf_purpose`
- **Display name:** Purpose
- **Tier:** `core`
- **Scoring role:** `core_scored`
- **Normative definition:** Disclosure of what problem, goal, or intended use the system or use case is meant to address.
- **Primary coding question:** Does the schema provide a field that can host purpose or goal disclosure?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `may_be_sole_dedicated_on_generic_description`
- **Documentary linkage relevance:** `low`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `ai_system_results_en` | Results/benefits-like narrative. |
| CA-GC-AI-REG | PRIMARY | `description_ai_system_en` | Generic description host under anti-overcredit. |
| CA-GC-AI-REG | REJECTED | `ai_system_capabilities_en` | Maps to technical method, not purpose. |
| EU-PSTW | PRIMARY | `Description` | Catalogue description under anti-overcredit. |
| EU-PSTW | SECONDARY | `Application type` | Application type classification. |
| EU-PSTW | SECONDARY | `Process type` | Process type classification. |
| NL-ALGO-REG | INDIRECT | `description_short` | Short generic description. |
| NL-ALGO-REG | PRIMARY | `goal` | Dedicated goal/purpose field. |
| NL-ALGO-REG | REJECTED | `category` | Policy category, not purpose. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| UK-ATRS | INDIRECT | `description` | Frozen: UK description is INDIRECT purpose only. |
| US-OMB-2025 | INDIRECT | `system_outputs` | Outputs related but not purpose. |
| US-OMB-2025 | PRIMARY | `problem_solved` | Dedicated problem/purpose narrative. |
| US-OMB-2025 | REJECTED | `topic_area` | Topic label is not purpose. |
| US-OMB-2025 | SECONDARY | `benefits` | Benefits narrative; report separately from primary. |

### Positive examples

- US `problem_solved`; NL `goal`; CA/PSTW description hosts under anti-over-credit.

### Negative examples / non-examples

- `topic_area`; NL `proportionality`; capabilities fields reserved for technical.

### Source-specific caveats

- UK description is INDIRECT only. Generic description may be dedicated at most once (usually purpose).

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `cf_purpose`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## cf_operational_status — Operational status

- **Identifier:** `cf_operational_status`
- **Display name:** Operational status
- **Tier:** `core`
- **Scoring role:** `core_scored`
- **Normative definition:** Disclosure of lifecycle or operational status (for example pilot, in use, retired), distinct from timestamps alone.
- **Primary coding question:** Does the schema expose a status or development-stage field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `generic_description_not_dedicated`
- **Documentary linkage relevance:** `none`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `ai_system_status_fr` | French alias. |
| CA-GC-AI-REG | PRIMARY | `ai_system_status_en` | English status (canonical). |
| CA-GC-AI-REG | REJECTED | `status_date` | Date is not operational status. |
| EU-PSTW | PRIMARY | ` Status` | Raw field has leading space; normalized status. |
| EU-PSTW | REJECTED | `End Year` | Year is not operational status. |
| EU-PSTW | REJECTED | `Start Year` | Year is not operational status. |
| NL-ALGO-REG | PRIMARY | `status` | Operational status. |
| NL-ALGO-REG | REJECTED | `begin_date` | Date is not operational status. |
| NL-ALGO-REG | REJECTED | `end_date` | Date is not operational status. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | REJECTED | `publication_dt` | Publication timestamp, not status. |
| UK-ATRS | REJECTED | `public_timestamp` | Timestamp is not operational status. |
| US-OMB-2025 | PRIMARY | `development_stage` | Lifecycle/development stage. |
| US-OMB-2025 | REJECTED | `operational_date` | Date is not operational status. |

### Positive examples

- US `development_stage`; NL `status`; CA `ai_system_status_en`; PSTW raw ` Status`.

### Negative examples / non-examples

- Any date/year/timestamp field (`operational_date`, `begin_date`, `Start Year`, etc.).

### Source-specific caveats

- PSTW raw field name is ` Status` (leading space).

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `cf_operational_status`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## cf_accountable_body — Accountable body identification

- **Identifier:** `cf_accountable_body`
- **Display name:** Accountable body identification
- **Tier:** `core`
- **Scoring role:** `core_scored`
- **Normative definition:** Disclosure of the public organisation accountable for the system or use case, distinct from vendor/supplier and from mere publishing platform identity.
- **Primary coding question:** Does the schema identify the accountable public body?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `generic_description_not_dedicated`
- **Documentary linkage relevance:** `low`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | PRIMARY | `government_organization` | Responsible government organisation. |
| CA-GC-AI-REG | REJECTED | `ai_system_primary_users_en` | Users are not accountable body. |
| CA-GC-AI-REG | REJECTED | `vendor_information` | Supplier field. |
| EU-PSTW | PRIMARY | `Responsible organisation` | Responsible organisation. |
| EU-PSTW | REJECTED | `Company name or GovTech ID` | Supplier/company, not accountable body. |
| NL-ALGO-REG | PRIMARY | `organization` | Operating organisation. |
| NL-ALGO-REG | REJECTED | `contact_email` | Contact email is not accountable body. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | REJECTED | `provider` | Provider is supplier. |
| NL-ALGO-REG | SECONDARY | `org_id` | Organisation id. |
| UK-ATRS | INDIRECT | `organisation_title` | Frozen: never PRIMARY; publisher identity. |
| US-OMB-2025 | PRIMARY | `agency_name` | Reporting agency name. |
| US-OMB-2025 | REJECTED | `contact_email` | Contact email is not accountable body. |
| US-OMB-2025 | REJECTED | `vendor_name` | Vendor is supplier, not accountable body. |
| US-OMB-2025 | SECONDARY | `agency` | Agency code. |
| US-OMB-2025 | SECONDARY | `agency_bureau` | Bureau within agency. |

### Positive examples

- US `agency_name`; CA `government_organization`; NL `organization`.

### Negative examples / non-examples

- Vendor/provider fields; `contact_email`; UK `organisation_title` as dedicated.

### Source-specific caveats

- UK publisher identity is INDIRECT only.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `cf_accountable_body`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## cf_data_involvement — Data involvement

- **Identifier:** `cf_data_involvement`
- **Display name:** Data involvement
- **Tier:** `core`
- **Scoring role:** `core_scored`
- **Normative definition:** Disclosure of whether and how data are involved at summary level, via a personal-data/PII flag and/or a dedicated data-sources or data-description field. Does not require training-data provenance.
- **Primary coding question:** Does the schema expose a personal-data flag or dedicated data-sources / data-description field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `generic_description_not_dedicated`
- **Documentary linkage relevance:** `dataset_documentation`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `personal_information_banks_en` | PIB codes; sparse. |
| CA-GC-AI-REG | PRIMARY | `involves_personal_information` | Frozen primary: PI flag. |
| CA-GC-AI-REG | REJECTED | `notification_ai` | Y/N notification flag, not data involvement. |
| CA-GC-AI-REG | SECONDARY | `data_sources_en` | Narrative fallback; report separately. |
| EU-PSTW | REJECTED | `Description` | Catalogue-inapplicable; generic must not substitute. |
| NL-ALGO-REG | PRIMARY | `source_data` | Frozen primary: source data narrative. |
| NL-ALGO-REG | REJECTED | `impacttoetsen` | Impact assessment text/links, not data involvement. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | SECONDARY | `source_data_grouping` | Grouped/linked data sources fallback. |
| UK-ATRS | REJECTED | `description` | No dedicated data field on API slim. |
| US-OMB-2025 | INDIRECT | `link_to_data` | Pointer capability; linkage layer. |
| US-OMB-2025 | PRIMARY | `has_pii` | Frozen primary: personal-data flag. |
| US-OMB-2025 | REJECTED | `demographic_features` | Not primary data-involvement field. |
| US-OMB-2025 | REJECTED | `hi_training_established` | Personnel training, not training-data provenance. |
| US-OMB-2025 | SECONDARY | `data_description` | Narrative fallback; report separately. |

### Positive examples

- US `has_pii`; CA `involves_personal_information`; NL `source_data`.

### Negative examples / non-examples

- `demographic_features`; `hi_training_established`; `notification_ai`; `impacttoetsen`.

### Source-specific caveats

- PSTW is catalogue_inapplicable. Report primary vs narrative fallback separately later (realization).

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `cf_data_involvement`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_human_oversight — Human oversight description

- **Identifier:** `om_human_oversight`
- **Display name:** Human oversight description
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure describing human roles, intervention, or oversight in system operation, distinct from organisational ownership and from redress procedures.
- **Primary coding question:** Does the schema provide a human oversight or intervention field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `object_specific`
- **Generic field policy:** `generic_description_indirect_only`
- **Documentary linkage relevance:** `medium`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `description_ai_system_en` | Generic only; not dedicated. |
| EU-PSTW | REJECTED | `Description` | Catalogue-inapplicable / not dedicated oversight. |
| NL-ALGO-REG | PRIMARY | `human_intervention` | Dedicated human intervention field. |
| NL-ALGO-REG | REJECTED | `contact_email` | Contact email is not oversight. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| UK-ATRS | REJECTED | `description` | No dedicated oversight on API slim. |
| US-OMB-2025 | REJECTED | `contact_email` | Contact email is not oversight. |
| US-OMB-2025 | REJECTED | `have_ato` | ATO flag is not human oversight description. |
| US-OMB-2025 | SECONDARY | `hi_failsafe_presence` | HI failsafe field. |
| US-OMB-2025 | SECONDARY | `hi_independent_review` | HI oversight-related field. |
| US-OMB-2025 | SECONDARY | `hi_ongoing_monitoring` | HI monitoring field. |

### Positive examples

- NL `human_intervention` (dedicated).

### Negative examples / non-examples

- `have_ato`; `contact_email`; using description as dedicated.

### Source-specific caveats

- US hi_* fields are conditional on high-impact subclass.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_human_oversight`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_risk_or_impact — Risk or impact designation

- **Identifier:** `om_risk_or_impact`
- **Display name:** Risk or impact designation
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure of a risk/impact designation flag and/or a dedicated risk or impact narrative. Distinct from outcome-benefit ticks and from DPIA content.
- **Primary coding question:** Does the schema expose a risk/impact flag or dedicated risk field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `object_specific`
- **Generic field policy:** `generic_description_indirect_only`
- **Documentary linkage relevance:** `impact_assessment`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | INDIRECT | `description_ai_system_en` | Generic only; not dedicated. |
| EU-PSTW | REJECTED | `Better collaboration and better communication` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Cost-reduction` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Description` | Catalogue-inapplicable; not risk designation. |
| EU-PSTW | REJECTED | `Enabled greater fairness, honesty, equality` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Improved Administrative Efficiency` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Improved Public Service` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Improved management of public resources` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Improved public control and influence on government actions and policies` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Increase quality of PSI and services` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Increased public participation in government actions and policy making` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Increased quality of processes and systems` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Increased transparency of public sector operations` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `More responsive, efficient, and cost-effective public services` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `New services or channels` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Open government capabilities` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Personalized Services` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Public (citizen)-centered services` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Reduced or eliminated the risk of corruption and abuse of the law by public servants` | PSTW outcome flag rejected as risk disclosure. |
| EU-PSTW | REJECTED | `Responsiveness of government operation` | PSTW outcome flag rejected as risk disclosure. |
| NL-ALGO-REG | INDIRECT | `impacttoetsen` | Not PRIMARY risk; impact-assessment text/links. |
| NL-ALGO-REG | PRIMARY | `risks` | Dedicated risks narrative. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | SECONDARY | `publication_category` | Frozen: secondary risk designation only. |
| UK-ATRS | REJECTED | `description` | No dedicated risk on API slim. |
| US-OMB-2025 | PRIMARY | `is_high_impact` | High-impact designation flag. |
| US-OMB-2025 | SECONDARY | `HI_justification` | Justification narrative. |
| US-OMB-2025 | SECONDARY | `hi_potential_impacts` | Impact narrative under HI block. |

### Positive examples

- US `is_high_impact`; NL `risks`.

### Negative examples / non-examples

- PSTW outcome `Improved…` flags; NL `proportionality`; `impacttoetsen` as PRIMARY.

### Source-specific caveats

- NL `publication_category` is SECONDARY only; `impacttoetsen` not PRIMARY.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_risk_or_impact`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_legal_basis — Legal basis

- **Identifier:** `om_legal_basis`
- **Display name:** Legal basis
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure of the legal basis for processing or operating the system.
- **Primary coding question:** Does the schema expose a lawful-basis or legal-basis field?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `jurisdiction_specific`
- **Generic field policy:** `generic_description_indirect_only`
- **Documentary linkage relevance:** `legal_or_policy_document`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| NL-ALGO-REG | PRIMARY | `lawful_basis` | Dedicated lawful basis. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| NL-ALGO-REG | SECONDARY | `lawful_basis_grouping` | Grouped lawful-basis material. |

### Positive examples

- NL `lawful_basis`.

### Negative examples / non-examples

- Inferring law from purpose text; using `proportionality`.

### Source-specific caveats

- Jurisdiction-specific; dedicated host observed only in NL export.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_legal_basis`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_supplier — Supplier identification

- **Identifier:** `om_supplier`
- **Display name:** Supplier identification
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure of vendor, provider, or contracting/supply arrangement, distinct from the accountable public body.
- **Primary coding question:** Does the schema expose vendor/provider/contracting fields?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `generic_description_indirect_only`
- **Documentary linkage relevance:** `procurement_document`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | PRIMARY | `vendor_information` | Vendor information. |
| CA-GC-AI-REG | SECONDARY | `developed_by_en` | Developer attribution categories. |
| EU-PSTW | INDIRECT | `Company name or GovTech ID` | Weak supplier signal. |
| NL-ALGO-REG | PRIMARY | `provider` | Provider/supplier field. |
| NL-ALGO-REG | REJECTED | `organization` | Accountable body, not supplier. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| US-OMB-2025 | PRIMARY | `vendor_name` | Vendor name. |
| US-OMB-2025 | SECONDARY | `contracting_usage` | Contracting/in-house usage. |

### Positive examples

- US `vendor_name`; CA `vendor_information`; NL `provider`.

### Negative examples / non-examples

- Agency/organization accountable-body fields.

### Source-specific caveats

- Do not confuse with accountable body.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_supplier`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_technical_method — Technical method or capability

- **Identifier:** `om_technical_method`
- **Display name:** Technical method or capability
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure of technical method, model class, or system capabilities, distinct from purpose.
- **Primary coding question:** Does the schema expose method, capability, or technical classification fields?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `universal`
- **Generic field policy:** `generic_description_indirect_only`
- **Documentary linkage relevance:** `source_code_or_technical_report`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | PRIMARY | `ai_system_capabilities_en` | Capabilities narrative. |
| CA-GC-AI-REG | REJECTED | `description_ai_system_en` | Reserved as purpose dedicated host. |
| EU-PSTW | PRIMARY | `AI Classification (I)` | AI classification. |
| EU-PSTW | REJECTED | `Description` | Reserved as purpose dedicated host. |
| EU-PSTW | SECONDARY | `AI Classification Subdomain (II) (main)` | AI subdomain. |
| EU-PSTW | SECONDARY | `Primary Technology` | Primary technology label. |
| NL-ALGO-REG | INDIRECT | `tags` | Weak technical tags. |
| NL-ALGO-REG | PRIMARY | `methods_and_models` | Methods and models narrative. |
| NL-ALGO-REG | REJECTED | `goal` | Purpose field. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| US-OMB-2025 | PRIMARY | `classification` | Technical method classification. |
| US-OMB-2025 | REJECTED | `problem_solved` | Purpose field; not technical method. |
| US-OMB-2025 | SECONDARY | `topic_area` | Topic label; thin technical signal. |

### Positive examples

- NL `methods_and_models`; CA `ai_system_capabilities_en`; US `classification`.

### Negative examples / non-examples

- Purpose primaries (`problem_solved`, `goal`); purpose-dedicated descriptions.

### Source-specific caveats

- If description is dedicated for purpose, it cannot also be dedicated technical.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_technical_method`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

## om_redress_pointer — Redress pointer

- **Identifier:** `om_redress_pointer`
- **Display name:** Redress pointer
- **Tier:** `module`
- **Scoring role:** `module`
- **Normative definition:** Disclosure capability for pointing to contestation, appeal, or complaint channels specific to the system. Generic contact email alone is insufficient.
- **Primary coding question:** Does the schema expose an appeal/contestation field (not merely a contact email)?
- **Unit of analysis:** schema_object × disclosure_function
- **Default applicability:** `conditional`
- **Generic field policy:** `contact_email_never_sufficient`
- **Documentary linkage relevance:** `appeal_process`

### What counts as DEDICATED

A field listed as PRIMARY in `field_function_candidates_v1.csv` for this function and source, whose native role matches the definition.

### What counts as INDIRECT

A field listed as INDIRECT (or used as a constrained proxy under source caveats), not a PRIMARY host.

### What counts as ABSENT

No PRIMARY/acceptable INDIRECT host, or applicability forbids support (`catalogue_inapplicable`).

### Candidate map (frozen)

| Source | Label | Raw field | Rationale |
|--------|-------|-----------|-----------|
| CA-GC-AI-REG | REJECTED | `notification_ai` | Not an appeal/contestation field. |
| NL-ALGO-REG | REJECTED | `contact_email` | Contact email is never redress. |
| NL-ALGO-REG | REJECTED | `proportionality` | Proportionality rejected for all DF v1. |
| UK-ATRS | REJECTED | `contact_email` | Field not in UK API slim; placeholder reject rule. |
| US-OMB-2025 | PRIMARY | `hi_appeal_process` | Appeal process field under HI. |
| US-OMB-2025 | REJECTED | `contact_email` | Generic contact email is never redress. |

### Positive examples

- US `hi_appeal_process` only under high-impact conditional applicability.

### Negative examples / non-examples

- `contact_email`; `notification_ai`.

### Source-specific caveats

- Conditional; generic contact is never sufficient.

### Common coding errors

- Upgrading INDIRECT to DEDICATED because a narrative is rich.
- Using population rates.
- Ignoring REJECTED rows in the candidate map.
- Function-specific: see caveats for `om_redress_pointer`.

### Adjudication notes

- Prefer the frozen candidate map over memory.
- If Phase 1 artefacts contradict, escalate as specification contradiction; do not invent a local rule.

---

