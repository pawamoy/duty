"""Deprecated. Use [`duty.tools.build`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import build as _build


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.build` instead of `duty.callables.build`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_build, name)
