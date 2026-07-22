# Pilot launch readiness — Disclosure Functions v1 (`pilot_round_01`)

**Date:** 2026-07-23  
**Generator:** `python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate`

## Preflight summary

| Check | Result |
|-------|--------|
| Pilot unit count | **33** |
| Unique units | **33** (no duplicates) |
| Present in full 55-unit template | **Yes** |
| Sources covered | US-OMB-2025, CA-GC-AI-REG, NL-ALGO-REG, EU-PSTW, UK-ATRS (**5/5**) |
| Functions covered | 11/11 Disclosure Functions v1 |
| Selection rationales present | **Yes** (all 33) |
| Judgment fields empty on blank packets | **Yes** |
| Frozen references (spec 1.0.0 + corpus lock) | **Match** |
| Packet checksums | `checksums/SHA256SUMS` generated |
| Technical dry run (`NON_SUBSTANTIVE_TEST_FIXTURE`) | **PASS** (`scripts/dry_run_pilot_round_01.py`) |
| Frozen-artefact contradictions | **None** |

## Packet notes

- `frozen_default_applicability` carries specification defaults; `applicability_label` remains blank for human coding.
- `assigned_coder_slot` is `coder_A` / `coder_B`; `coder_id` starts blank.
- No adjudicated values in blank packets.
- A and B packets share identical `coding_unit_id` universes.

## Exact remaining human actions

1. Assign two independent human coders to slots A and B.
2. Distribute blank packets + locked reference materials.
3. Coders complete sheets independently (no discussion before freeze).
4. Validate each completed sheet (`scripts/validate_pilot_packet.py --mode post`).
5. Freeze + checksum completed files into intake.
6. Export disagreements → adjudicate → run Phase 3 with `--allow-partial`.

## Known TBD decisions

- Whether completed sheets may be committed to git (default: prefer external intake if identifying).
- Scheduling / training session logistics (out of scope for this package).
- Whether a Zenodo concept DOI should appear on coder-facing docs (not required for coding).

## Contradictions found

None. Frozen Phase 1–2 artefacts are consistent with the 33-unit pilot manifest.

---

## Final status

**A. READY FOR TWO INDEPENDENT HUMAN CODERS**
