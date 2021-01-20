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

    def __init__(self, **options) -> None:
        """
        Initialize the context.

        Arguments:
            options: Options passed internally to `failprint` functions.
        """
        self.options = options

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
        try:
            code = failprint_run(cmd, args=args, kwargs=kwargs, **final_options)
        except KeyboardInterrupt:
            code = 130
        if code:
            raise DutyFailure(code)
