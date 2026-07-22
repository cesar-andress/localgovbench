#!/usr/bin/env python3
"""Stub for F06_coder_agreement. Refuses to invent findings."""
import sys
print(
    "F06_coder_agreement: required study inputs are not present. "
    "Do not invent results. Needed: pilot completed sheets + disagreements CSV (future)",
    file=sys.stderr,
)
sys.exit(2)
