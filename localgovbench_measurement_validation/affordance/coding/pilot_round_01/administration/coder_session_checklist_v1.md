# Coder session checklist — `pilot_round_01`

- [ ] Confirm packet filename matches your slot (`coder_A` or `coder_B`)
- [ ] Confirm `assigned_coder_slot` column matches your slot
- [ ] Confirm reference manifest checksums if provided
- [ ] Do **not** change row order, `coding_unit_id`, or `coding_record_id`
- [ ] Code **one unit at a time**
- [ ] Follow codebook coding order / decision sequence
- [ ] Fill human judgment fields only; leave frozen context untouched
- [ ] Document rationale for each unit
- [ ] Flag uncertainty via `coder_confidence` / `unresolved_issue`
- [ ] Do **not** consult the other coder before freeze
- [ ] Do **not** use record-population rates
- [ ] Do **not** treat generic URLs as function-specific support
- [ ] Do **not** insert `adjudicated_value` / `adjudicator_id`
- [ ] Set `coder_id` to your slot (`coder_A` or `coder_B`) when coding
- [ ] Save as `pilot_round_01_coder_<A|B>_completed.csv`
- [ ] Run local post-coding validation before submission
