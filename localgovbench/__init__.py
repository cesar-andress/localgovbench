"""LocalGovBench: schema disclosure affordance research software (Disclosure Functions v1)."""

from __future__ import annotations

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

try:
    __version__ = version("localgovbench")
except PackageNotFoundError:  # pragma: no cover - editable/source tree without install
    __version__ = "1.0.0"

__all__ = ["__version__"]
