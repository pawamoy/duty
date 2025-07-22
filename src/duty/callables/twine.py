"""Deprecated. Use [`duty.tools.twine`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import twine as _twine


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.twine` instead of `duty.callables.twine`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_twine, name)
