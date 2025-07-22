"""Deprecated. Use [`duty.tools.isort`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import isort as _isort


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.isort` instead of `duty.callables.isort`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_isort, name)
