"""Deprecated. Use [`duty.tools.flake8`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import flake8 as _flake8


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.flake8` instead of `duty.callables.flake8`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_flake8, name)
