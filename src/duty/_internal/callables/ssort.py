# YORE: Bump 2: Remove file.

from __future__ import annotations

import sys

from failprint import lazy


@lazy(name="ssort")
def run(
    *files: str,
    diff: bool | None = None,
    check: bool | None = None,
) -> int:
    """Run `ssort`.

    Parameters:
        *files: Files to format.
        diff: Prints a diff of all changes ssort would make to a file.
        check: Check the file for unsorted statements. Returns 0 if nothing needs to be changed. Otherwise returns 1.
    """
    from ssort._main import main as ssort  # noqa: PLC0415

    cli_args = list(files)

    if diff:
        cli_args.append("--diff")

    if check:
        cli_args.append("--check")

    old_sys_argv = sys.argv
    sys.argv = ["ssort*", *cli_args]
    try:
        return ssort()
    finally:
        sys.argv = old_sys_argv
