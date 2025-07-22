"""Deprecated. Use [`duty.tools.griffe`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import griffe as _griffe


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.griffe` instead of `duty.callables.griffe`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_griffe, name)
