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

from __future__ import annotations

import sys

from duty._internal.tools._base import Tool


class ssort(Tool):  # noqa: N801
    """Call [ssort](https://github.com/bwhmather/ssort)."""

    cli_name = "ssort"
    """The name of the executable on PATH."""

    def __init__(
        self,
        *files: str,
        diff: bool | None = None,
        check: bool | None = None,
    ) -> None:
        """Run `ssort`.

        Parameters:
            *files: Files to format.
            diff: Prints a diff of all changes ssort would make to a file.
            check: Check the file for unsorted statements. Returns 0 if nothing needs to be changed. Otherwise returns 1.
        """
        cli_args = list(files)

        if diff:
            cli_args.append("--diff")

        if check:
            cli_args.append("--check")

    def __call__(self) -> None:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from ssort._main import main as run_ssort  # noqa: PLC0415  # ty:ignore[unresolved-import]

        old_sys_argv = sys.argv
        sys.argv = ["ssort", *self.cli_args]
        try:
            run_ssort()
        finally:
            sys.argv = old_sys_argv
