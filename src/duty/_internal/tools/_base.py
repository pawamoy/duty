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
