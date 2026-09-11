# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
    ty,
    yore,
    zensical,
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
    "ty",
    "yore",
    "zensical",
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
