#!/usr/bin/env python3
"""Build Disclosure Functions v1 schema coding templates and pilot manifest.

Does not perform human coding, IRR calculation, realization, or manuscript edits.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from localgovbench_measurement_validation.affordance.coding.pilot import (  # noqa: E402
    write_pilot_manifest,
)
from localgovbench_measurement_validation.affordance.coding.render_codebook import (  # noqa: E402
    write_codebook,
)
from localgovbench_measurement_validation.affordance.coding.template import (  # noqa: E402
    build_coding_template_rows,
    write_coding_template,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    codebook_path = write_codebook()
    template_path = write_coding_template()
    pilot_path = write_pilot_manifest()
    rows = build_coding_template_rows()
    sources = sorted({r["source_name"] for r in rows})
    functions = sorted({r["disclosure_function_id"] for r in rows})
    print(f"Wrote {codebook_path}")
    print(f"Wrote {template_path}")
    print(f"  coding_units={len(rows)}")
    print(f"  sources={sources}")
    print(f"  functions={functions}")
    print(f"Wrote {pilot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
