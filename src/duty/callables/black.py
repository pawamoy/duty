"""Deprecated. Use [`duty.tools.black`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import black as _black


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.black` instead of `duty.callables.black`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_black, name)
