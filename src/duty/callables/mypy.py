"""Deprecated. Use [`duty.tools.mypy`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import mypy as _mypy


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.mypy` instead of `duty.callables.mypy`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_mypy, name)
