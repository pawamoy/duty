"""Deprecated. Use [`duty.tools.blacken_docs`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import blacken_docs as _blacken_docs


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.blacken_docs` instead of `duty.callables.blacken_docs`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_blacken_docs, name)
