"""Module containing the context definition."""

from typing import Callable, List, Union

from failprint.runners import run as failprint_run

from duty.exceptions import DutyFailure

CmdType = Union[str, List[str], Callable]


class Context:
    """
    A simple context class.

    Context instances are passed to functions decorated with `duty`.
    """

    def __init__(self, options, options_override=None) -> None:
        """
        Initialize the context.

        Arguments:
            options: Base options specified in `@duty(**options)`.
            options_override: Options that override `run` and `@duty` options.
                This argument is used to allow users to override options from the CLI or environment.
        """
        self.options = options
        self.options_override = options_override or {}

    def run(self, cmd: CmdType, args=None, kwargs=None, **options):
        """
        Run a command in a subprocess or a Python callable.

        Arguments:
            cmd: A command or a Python callable.
            args: Positional arguments passed to the Python callable.
            kwargs: Keyword arguments passed to the Python callable.
            options: Options passed to `failprint` functions.

        Raises:
            DutyFailure: When the exit code / function result is greather than 0.
        """
        final_options = dict(self.options)
        final_options.update(options)
        final_options.update(self.options_override)
        try:
            code = failprint_run(cmd, args=args, kwargs=kwargs, **final_options)
        except KeyboardInterrupt:
            code = 130
        if code:
            raise DutyFailure(code)
