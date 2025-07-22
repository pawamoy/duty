"""Deprecated. Use [`duty.tools.ssort`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import ssort as _ssort


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.ssort` instead of `duty.callables.ssort`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_ssort, name)
