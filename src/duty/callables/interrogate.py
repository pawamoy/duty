"""Deprecated. Use [`duty.tools.interrogate`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import interrogate as _interrogate


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.interrogate` instead of `duty.callables.interrogate`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_interrogate, name)
