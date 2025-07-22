"""Deprecated. Use [`duty.tools.pytest`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import pytest as _pytest


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.pytest` instead of `duty.callables.pytest`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_pytest, name)
