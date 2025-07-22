from __future__ import annotations

import os
from contextlib import contextmanager, suppress
from typing import TYPE_CHECKING, Any, Callable, Union

from failprint import run as failprint_run

from duty._internal.exceptions import DutyFailure
from duty._internal.tools._base import Tool

if TYPE_CHECKING:
    from collections.abc import Iterator

CmdType = Union[str, list[str], Callable]
"""Type of a command that can be run in a subprocess or as a Python callable."""


class Context:
    """A simple context class.

    Context instances are passed to functions decorated with `duty`.
    """

    def __init__(self, options: dict[str, Any], options_override: dict[str, Any] | None = None) -> None:
        """Initialize the context.

        Parameters:
            options: Base options specified in `@duty(**options)`.
            options_override: Options that override `run` and `@duty` options.
                This argument is used to allow users to override options from the CLI or environment.
        """
        self._options = options
        self._option_stack: list[dict[str, Any]] = []
        self._options_override = options_override or {}

    @contextmanager
    def cd(self, directory: str) -> Iterator:
        """Change working directory as a context manager.

        Parameters:
            directory: The directory to go into.

        Yields:
            Nothing.
        """
        if not directory:
            yield
            return
        old_wd = os.getcwd()
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(old_wd)

    def run(self, cmd: CmdType, **options: Any) -> str:
        """Run a command in a subprocess or a Python callable.

        Parameters:
            cmd: A command or a Python callable.
            options: Options passed to `failprint` functions.

        Raises:
            DutyFailure: When the exit code / function result is greather than 0.

        Returns:
            The output of the command.
        """
        final_options = dict(self._options)
        final_options.update(options)

        if "command" not in final_options and isinstance(cmd, Tool):
            with suppress(ValueError):
                final_options["command"] = cmd.cli_command

        allow_overrides = final_options.pop("allow_overrides", True)
        workdir = final_options.pop("workdir", None)

        if allow_overrides:
            final_options.update(self._options_override)

        with self.cd(workdir):
            try:
                result = failprint_run(cmd, **final_options)
            except KeyboardInterrupt as ki:
                raise DutyFailure(130) from ki

        if result.code:
            raise DutyFailure(result.code)

        return result.output

    @contextmanager
    def options(self, **opts: Any) -> Iterator:
        """Change options as a context manager.

        Can be nested as will, previous options will pop once out of the with clause.

        Parameters:
            **opts: Options used in `run`.

        Yields:
            Nothing.
        """
        self._option_stack.append(self._options)
        self._options = {**self._options, **opts}
        try:
            yield
        finally:
            self._options = self._option_stack.pop()
