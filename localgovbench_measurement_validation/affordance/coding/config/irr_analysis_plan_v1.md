# IRR analysis plan v1 (plan only — no calculations)

**Status:** planning artefact for future analysis after human coding.  
**Do not compute IRR in Phase 2.**

## Attributes and recommended statistics

| Attribute | Scale | Primary statistics | Notes |
|-----------|-------|--------------------|-------|
| `support_level` | ordinal (`absent` < `indirect` < `dedicated`) | raw agreement; Cohen’s κ (2 coders); **linear weighted κ** as sensitivity | Report unweighted and weighted |
| `applicability_label` | nominal | raw agreement; unweighted Cohen’s κ | Do not ordinalize labels |
| `encoding_type` | nominal | raw agreement; unweighted κ | `not_applicable` may dominate — report prevalence |
| `documentary_linkage_layer` | nominal | raw agreement; unweighted κ | Same prevalence caution |

## Prevalence and marginal imbalance

Expect high prevalence of `absent` on UK-API slim modules and of `catalogue_inapplicable` on PSTW register-native functions.  
Report:

- category prevalence per attribute,
- observed agreement vs expected agreement,
- κ alongside raw agreement (κ alone can be unstable).

## Function-level and source-level reporting

Compute agreement:

- overall,
- by `disclosure_function_id`,
- by `source_name` / `schema_object_type`,
- optionally by scoring role (core_scored vs module vs descriptive_only).

## Treatment of not-applicable units

- Units with applicability `catalogue_inapplicable` should be analysed in a **separate stratum** for support agreement, or coded to forced `absent` and reported both pooled and stratified.
- Prefer stratified reporting to avoid inflated agreement from trivial absences.

## Treatment of adjudicated values

- Primary IRR uses **independent pre-adjudication** coder labels only.
- Adjudicated consensus may be used for a final analysis dataset but **must not** be fed back into κ as if independent.
- Report adjudication volume and disagreement types.

## Pass/fail cutoff

No universal publication gate is frozen.

**TO BE DETERMINED AFTER PILOT REVIEW**

Any future cutoff must be justified from pilot prevalence and disagreement typology, not imported from unrelated instruments.
