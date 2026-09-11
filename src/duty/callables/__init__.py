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

"""Module containing callables for many tools.

These callables are **deprecated** in favor of our new [tools][duty.tools].
"""

# YORE: Bump 2: Remove file.

from __future__ import annotations

import warnings

from failprint import lazy  # noqa: F401

from duty._internal.callables import (
    autoflake,  # noqa: F401
    black,  # noqa: F401
    blacken_docs,  # noqa: F401
    build,  # noqa: F401
    coverage,  # noqa: F401
    flake8,  # noqa: F401
    git_changelog,  # noqa: F401
    griffe,  # noqa: F401
    interrogate,  # noqa: F401
    isort,  # noqa: F401
    mkdocs,  # noqa: F401
    mypy,  # noqa: F401
    pytest,  # noqa: F401
    ruff,  # noqa: F401
    safety,  # noqa: F401
    ssort,  # noqa: F401
    twine,  # noqa: F401
)

warnings.warn(
    "Callables are deprecated in favor of our new `duty.tools`. "
    "They are easier to use and provide more functionality "
    "like automatically computing `command` values in `ctx.run()` calls. "
    "Old callables will be removed in a future version.",
    DeprecationWarning,
    stacklevel=1,
)
