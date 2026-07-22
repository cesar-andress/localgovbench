# Worked examples v1 — Schema coding

All examples use fields present in the frozen schema inventory / candidate map.  
No invented fields or records. Support labels: `dedicated` | `indirect` | `absent`.

---

## 1. Clear dedicated — NL purpose

- **Unit:** `NL-ALGO-REG` × `cf_purpose`
- **Decision:** support=`dedicated`; encoding=`free_text`; linkage=`none`
- **Primary fields:** `goal`
- **Why:** `goal` is PRIMARY in the candidate map and natively hosts purpose/goal disclosure.
- **Rejected alternative:** coding `description_short` as dedicated — it is INDIRECT/generic; `goal` already exists, so anti-over-credit blocks generic dedicated.

## 2. Clear indirect — UK purpose

- **Unit:** `UK-ATRS` × `cf_purpose`
- **Decision:** support=`indirect`
- **Indirect fields:** `description`
- **Why:** Frozen rule — UK Search API `description` is INDIRECT purpose only.
- **Rejected alternative:** `dedicated` — violates `uk_description_indirect_purpose`.

## 3. Clear absent — UK operational status

- **Unit:** `UK-ATRS` × `cf_operational_status`
- **Decision:** support=`absent`; encoding=`not_applicable` or `other` only if forced empty structured; prefer `not_applicable` when no host exists; linkage=`none`
- **Why:** API-slim object has no status field (`public_timestamp` is REJECTED as status).
- **Rejected alternative:** using `public_timestamp` as status.

## 4. Catalogue-inapplicable — PSTW data involvement

- **Unit:** `EU-PSTW` × `cf_data_involvement`
- **Decision:** applicability=`catalogue_inapplicable`; support=`absent`; encoding=`not_applicable`; linkage=`not_applicable`
- **Why:** Contrast case catalogue; register-native data-involvement N/A.
- **Rejected alternative:** `indirect` via `Description` — forbidden under catalogue_inapplicable + anti-over-credit.

## 5. Conditional US high-impact — oversight

- **Unit:** `US-OMB-2025` × `om_human_oversight`
- **Decision:** applicability=`conditional`; support based on whether hi_* oversight hosts exist as schema fields (they do: `hi_independent_review`, etc.) — typically `indirect` or `dedicated` only if treating a hi_* field as the host under conditional applicability; follow candidate map (SECONDARY for hi_*). Practical coding: support=`indirect` with indirect fields listing hi_* SECONDARY candidates, **or** `absent` if the round requires schema-wide dedicated hosts only. **Frozen candidate map lists hi_* as SECONDARY, not PRIMARY** → maximum defensible support without inventing PRIMARY is **`indirect`** (SECONDARY/INDIRECT hosts), not `dedicated`.
- **Why:** Oversight fields are high-impact conditional; no schema-wide `human_roles` in inventory.
- **Rejected alternative:** `dedicated` via non-existent `human_roles`; using `have_ato` or `contact_email`.

## 6. UK API-slim — accountable body

- **Unit:** `UK-ATRS` × `cf_accountable_body`
- **Decision:** support=`indirect`; indirect=`organisation_title`
- **Why:** Publisher identity (observed Cabinet Office), never PRIMARY.
- **Rejected alternative:** `dedicated`.

## 7. PSTW generic description — purpose

- **Unit:** `EU-PSTW` × `cf_purpose`
- **Decision:** support=`dedicated`; primary=`Description`; generic_narrative_used=`true`
- **Why:** Under anti-over-credit, generic `Description` may be the sole dedicated host for purpose on this object; Application/Process type are SECONDARY.
- **Rejected alternative:** also coding `Description` dedicated for risk/oversight/technical.

## 8. Accountable body vs supplier conflict — US

- **Unit:** `US-OMB-2025` × `om_supplier`
- **Decision:** support=`dedicated`; primary=`vendor_name` (SECONDARY `contracting_usage` optional in reviewed list, not required for dedicated if vendor_name is PRIMARY)
- **Why:** Supplier ≠ accountable agency.
- **Rejected alternative:** using `agency_name` as supplier evidence.

## 9. Purpose vs technical-method conflict — CA

- **Unit:** `CA-GC-AI-REG` × `om_technical_method`
- **Decision:** support=`dedicated`; primary=`ai_system_capabilities_en`
- **Why:** Capabilities field is PRIMARY for technical; `description_ai_system_en` is REJECTED for technical because it is reserved as purpose host.
- **Rejected alternative:** dedicated technical via description.

## 10. Generic URL vs function-specific linkage — US data involvement

- **Unit:** `US-OMB-2025` × `cf_data_involvement`
- **Decision:** support=`dedicated`; primary=`has_pii`; linkage may be `function_specific` only if coding the pointer capability of `link_to_data` as linkage attribute with type `dataset_documentation` — **not** by upgrading a generic contact URL.
- **Why:** `has_pii` is frozen PRIMARY; `contact_email` is generic and never function-specific evidence.
- **Rejected alternative:** treating `contact_email` URL-like values as dataset documentation.

---

## Cross-cutting rejection checklist used above

1. REJECTED map rows never become primary evidence.  
2. Generic narrative dedicated at most once (normally purpose).  
3. Dates ≠ operational status.  
4. PSTW outcome flags ≠ risk.  
5. NL `proportionality` supports nothing.  
6. Confidence never changes support.
