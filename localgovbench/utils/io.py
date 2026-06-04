"""Lightweight YAML I/O without mandatory third-party dependencies."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import yaml as _yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - optional dependency
    _yaml = None


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file into a dictionary."""
    text = Path(path).read_text(encoding="utf-8")
    if _yaml is not None:
        data = _yaml.safe_load(text)
    else:
        data = _minimal_yaml_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at root of {path}, got {type(data).__name__}")
    return data


def save_yaml(path: str | Path, data: dict[str, Any]) -> None:
    """Write a dictionary to YAML (stdlib fallback emits JSON-style for tests)."""
    path = Path(path)
    if _yaml is not None:
        path.write_text(
            _yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    else:
        # Fallback sufficient for synthetic examples in this artifact.
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _minimal_yaml_load(text: str) -> dict[str, Any]:
    """
    Parse a restricted subset of YAML used by bundled examples.

    For full YAML support, install PyYAML: ``pip install pyyaml``.
    """
    lines = [ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    if not lines:
        return {}
    # Detect JSON-compatible documents
    stripped = text.strip()
    if stripped.startswith("{"):
        return json.loads(stripped)

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for raw in lines:
        if ":" not in raw:
            continue
        indent = len(raw) - len(raw.lstrip())
        key, _, rest = raw.strip().partition(":")
        value_str = rest.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if value_str == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        elif value_str in {"true", "false"}:
            parent[key] = value_str == "true"
        elif value_str.isdigit():
            parent[key] = int(value_str)
        else:
            parent[key] = value_str.strip('"').strip("'")

    return root
