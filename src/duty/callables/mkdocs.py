"""Deprecated. Use [`duty.tools.mkdocs`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import mkdocs as _mkdocs


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.mkdocs` instead of `duty.callables.mkdocs`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_mkdocs, name)
