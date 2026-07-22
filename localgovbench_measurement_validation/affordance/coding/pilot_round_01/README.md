# Pilot Round 01 — Disclosure Functions v1

**Status:** Operational launch package for human double-coding  
**Pilot units:** 33  
**Coder slots:** `coder_A`, `coder_B` (anonymous)

This directory prepares the human pilot. It does **not** contain study results,
IRR statistics, adjudication outcomes, realization rates, or gap figures.

## Contents

| Path | Role |
|------|------|
| `coder_packets/` | Blank independent packets (33 units each) |
| `administration/` | Pilot guide, checklist, handoff |
| `locked_reference/` | SHA-256 reference manifest for frozen inputs |
| `checksums/` | Packet and reference checksums |
| `validation/` | Launch-readiness report + validators |
| `import_commands/` | Exact CLI commands for post-coding pipeline |
| `completed_inputs/` | Placeholder only — place completed sheets later |

## Generate / regenerate packets

```bash
python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate
```

Do not hand-edit blank packets. Regenerate from the frozen pilot manifest.

## Critical rules

- Coders must not discuss answers before both completed sheets are frozen.
- Do not prefill support, encoding, linkage, confidence, or rationales.
- Do not place fake completed coding sheets in `completed_inputs/`.
