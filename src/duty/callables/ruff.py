"""Deprecated. Use [`duty.tools.ruff`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import ruff as _ruff


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.ruff` instead of `duty.callables.ruff`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_ruff, name)
