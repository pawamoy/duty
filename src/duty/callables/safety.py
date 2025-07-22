"""Deprecated. Use [`duty.tools.safety`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import safety as _safety


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.safety` instead of `duty.callables.safety`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_safety, name)
