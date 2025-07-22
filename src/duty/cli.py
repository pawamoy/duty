"""Deprecated. Import from `duty` directly."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from duty._internal import cli


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from `duty.cli` is deprecated. Import from `duty` directly.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(cli, name)
