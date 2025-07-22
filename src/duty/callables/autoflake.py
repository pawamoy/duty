"""Deprecated. Use [`duty.tools.autoflake`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import autoflake as _autoflake


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.autoflake` instead of `duty.callables.autoflake`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_autoflake, name)
