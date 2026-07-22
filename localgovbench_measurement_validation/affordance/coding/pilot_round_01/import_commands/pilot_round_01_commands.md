# Exact commands — `pilot_round_01`

Repository root: `~/papers/localgovbench/localgovbench`

Blank packets:

- `localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv`
- `localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_B.csv`

Completed intake (after human coding):

- `.../pilot_round_01/completed_inputs/pilot_round_01_coder_A_completed.csv`
- `.../pilot_round_01/completed_inputs/pilot_round_01_coder_B_completed.csv`

---

## A. Validate Coder A independently (blank / pre-coding)

```bash
cd ~/papers/localgovbench/localgovbench
python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv \
  --mode pre
```

## B. Validate Coder B independently (blank / pre-coding)

```bash
python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_B.csv \
  --mode pre
```

## A′ / B′. Validate completed sheets (post-coding; no A↔B comparison)

```bash
python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_A_completed.csv \
  --mode post \
  --blank-packet localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_A.csv

python3.12 scripts/validate_pilot_packet.py \
  localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_B_completed.csv \
  --mode post \
  --blank-packet localgovbench_measurement_validation/affordance/coding/pilot_round_01/coder_packets/pilot_round_01_coder_B.csv
```

---

## C. Phase 3 pipeline on both completed files (`--allow-partial`)

```bash
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id pilot_round_01 \
  --coder-a localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_A_completed.csv \
  --coder-b localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_B_completed.csv \
  --allow-partial \
  --operator pilot_admin
```

Note: if A and B disagree, this command requires an adjudication file (see F).
For a first import attempt that only archives/validates independently, validate
each sheet with A′/B′ first, then export disagreements (D) before merging.

---

## D. Export disagreements

```bash
python3.12 - <<'PY'
from pathlib import Path
from localgovbench_measurement_validation.affordance.coding.validate import export_disagreements

a = Path('localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_A_completed.csv')
b = Path('localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_B_completed.csv')
out = Path('localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_disagreements.csv')
export_disagreements(a, b, out)
print(out)
PY
```

---

## E. Create adjudication input file

```bash
python3.12 - <<'PY'
from pathlib import Path
from localgovbench_measurement_validation.affordance.coding.validate import create_adjudication_input

disagree = Path('localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_disagreements.csv')
out = Path('localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_adjudication_input.csv')
create_adjudication_input(disagree, out)
print(out)
PY
```

Complete adjudication offline using `adjudication_protocol_v1.md`. Do not invent
resolutions in this preparation package.

---

## F. Run pipeline after adjudication

```bash
python3.12 scripts/run_affordance_experiment_pipeline.py \
  --experiment-id pilot_round_01_adjudicated \
  --coder-a localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_A_completed.csv \
  --coder-b localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_coder_B_completed.csv \
  --adjudication localgovbench_measurement_validation/affordance/coding/pilot_round_01/completed_inputs/pilot_round_01_adjudication_completed.csv \
  --allow-partial \
  --operator pilot_admin
```

Replace `pilot_round_01_adjudication_completed.csv` with the adjudicated sheet
filename actually used.

---

## Regenerate blank packets / checksums

```bash
python3.12 -m localgovbench_measurement_validation.affordance.coding.pilot_launch generate
```
