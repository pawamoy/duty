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

import os
from collections.abc import Callable
from contextlib import contextmanager, suppress
from typing import TYPE_CHECKING, Any

from failprint import run as failprint_run

from duty._internal.exceptions import DutyFailure
from duty._internal.tools._base import Tool

if TYPE_CHECKING:
    from collections.abc import Iterator

CmdType = str | list[str] | Callable
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
        old_wd = os.getcwd()  # noqa: PTH109
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
