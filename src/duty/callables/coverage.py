"""Deprecated. Use [`duty.tools.coverage`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import coverage as _coverage


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.coverage` instead of `duty.callables.coverage`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_coverage, name)
