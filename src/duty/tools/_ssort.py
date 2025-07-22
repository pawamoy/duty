"""Callable for [ssort](https://github.com/bwhmather/ssort)."""

from __future__ import annotations

import sys

from duty.tools._base import Tool


class ssort(Tool):  # noqa: N801
    """Call [ssort](https://github.com/bwhmather/ssort)."""

    cli_name = "ssort"

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

    def __call__(self) -> int:
        from ssort._main import main as run_ssort  # noqa: PLC0415

        old_sys_argv = sys.argv
        sys.argv = ["ssort", *self.cli_args]
        try:
            return run_ssort()
        finally:
            sys.argv = old_sys_argv
