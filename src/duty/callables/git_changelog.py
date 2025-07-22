"""Deprecated. Use [`duty.tools.git_changelog`][] instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal.callables import git_changelog as _git_changelog


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Callables are deprecated in favor of tools, use `duty.tools.git_changelog` instead of `duty.callables.git_changelog`.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(_git_changelog, name)
