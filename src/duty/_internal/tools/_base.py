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

# Utilities for creating tools.

from __future__ import annotations

import shlex
import sys
from io import StringIO
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class LazyStdout(StringIO):
    """Lazy stdout buffer.

    Can be used when tools' main entry-points
    expect a file-like object for stdout.
    """

    def write(self, value: str) -> int:
        """Write a string to the stdout buffer."""
        return sys.stdout.write(value)

    def __repr__(self) -> str:
        return "stdout"


class LazyStderr(StringIO):
    """Lazy stderr buffer.

    Can be used when tools' main entry-points
    expect a file-like object for stderr.
    """

    def write(self, value: str) -> int:
        """Write a string to the stderr buffer."""
        return sys.stderr.write(value)

    def __repr__(self) -> str:
        return "stderr"


class Tool:
    """Base class for tools."""

    cli_name: str = ""
    """The name of the executable on PATH."""

    def __init__(
        self,
        cli_args: list[str] | None = None,
        py_args: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the tool.

        Parameters:
            cli_args: Initial command-line arguments. Use `add_args()` to add more.
            py_args: Python arguments. Your `__call__` method will be able to access
                these arguments as `self.py_args`.
        """
        self.cli_args: list[str] = cli_args or []
        """Registered command-line arguments."""
        self.py_args: dict[str, Any] = py_args or {}
        """Registered Python arguments."""

    def add_args(self, *args: str) -> Self:
        """Append CLI arguments."""
        self.cli_args.extend(args)
        return self

    @property
    def cli_command(self) -> str:
        """The equivalent CLI command."""
        if not self.cli_name:
            raise ValueError("This tool does not provide a CLI.")
        return shlex.join([self.cli_name, *self.cli_args])
