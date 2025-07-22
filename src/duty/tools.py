"""Our collection of tools."""

import warnings
from typing import Any

from duty._internal.tools import (
    autoflake,
    black,
    blacken_docs,
    build,
    coverage,
    flake8,
    git_changelog,
    griffe,
    interrogate,
    isort,
    mkdocs,
    mypy,
    pytest,
    ruff,
    safety,
    ssort,
    twine,
    yore,
)

__all__ = [
    "autoflake",
    "black",
    "blacken_docs",
    "build",
    "coverage",
    "flake8",
    "git_changelog",
    "griffe",
    "interrogate",
    "isort",
    "mkdocs",
    "mypy",
    "pytest",
    "ruff",
    "safety",
    "ssort",
    "twine",
    "yore",
]


# YORE: Bump 2: Remove block.
def __getattr__(name: str) -> Any:
    """Return the tool or lazy object by name."""
    from failprint import lazy  # noqa: F401,PLC0415

    from duty._internal.tools._base import LazyStderr, LazyStdout, Tool  # noqa: F401,PLC0415

    if name in locals():
        warnings.warn(
            f"Importing `{name}` from `duty.tools` is deprecated, import directly from `duty` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return locals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
