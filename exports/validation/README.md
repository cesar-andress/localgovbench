# Publishable validation exports (real expert panel + real dossier studies only)
# Run scripts/validate_redevelopment_scope.py before committing aggregates here.

study_label: localgovbench_instrument_validation_redevelop

allowed_export_types:
  - content_validity_summary.json
  - delphi_round_comparison.csv
  - irr_field_summary.json
  - gate_ablation.csv
  - sensitivity_real_scores.csv
  - adjudicated_scores_summary.json

forbidden_in_exports:
  - synthetic_irr_as_field_validation
  - open_pilot_as_validation_evidence
  - public_document_observability_as_primary_outcome
