"""Module containing all the logic."""

import inspect
from typing import Any, Callable, Dict, List, Optional, Union

from failprint.cli import run as failprint_run

DutyListType = List[Union[str, Callable, "Duty"]]
CmdType = Union[str, List[str], Callable]


class DutyFailure(Exception):
    """An exception raised when a duty fails."""

    def __init__(self, code):
        """
        Initialize the object.

        Arguments:
            code: The exit code of a command.
        """
        super().__init__(self)
        self.code = code


class Duty:
    """The main duty class."""

    default_options: Dict[str, Any] = {}

    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        pre: Optional[DutyListType] = None,
        post: Optional[DutyListType] = None,
        opts: Dict[str, Any] = None,
    ) -> None:
        """
        Initialize the object.

        Arguments:
            name: The duty name.
            description: The duty description.
            function: The duty function.
            pre: A list of duties to run before this one.
            post: A list of duties to run after this one.
            opts: Options used to create the context instance.
        """
        self.name = name
        self.description = description
        self.function = function
        self.pre = pre or []
        self.post = post or []
        self.context = Context(**(opts or self.default_options))

    def __call__(self, *args, **kwargs) -> None:
        """
        Run the duty function.

        Arguments:
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed to the function.
        """
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs) -> None:
        """
        Run the duty function.

        This function also runs pre- and post-duties.

        Arguments:
            args: Positional arguments passed to the function.
            kwargs: Keyword arguments passed to the function.
        """
        run_duties(self.pre)
        self.function(self.context, *args, **kwargs)
        run_duties(self.post)


def run_duties(duties_list: DutyListType) -> None:
    """
    Run a list of duties.

    Arguments:
        duties_list: The list of duties to run.
    """
    for duty_item in duties_list:
        if isinstance(duty_item, Duty):
            duty_item.run()
        elif isinstance(duty_item, str):
            duties[duty_item].run()
        elif callable(duty_item):
            duty_item()


class Context:
    """
    A simple context class.

    Context instances are passed to functions decorated with `duty`.
    """

    def __init__(self, **options) -> None:
        """
        Initialize the object.

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


duties: Dict[str, Duty] = {}


def register_duty(
    func: Callable,
    name: Optional[str] = None,
    pre: Optional[DutyListType] = None,
    post: Optional[DutyListType] = None,
    **opts,
) -> Duty:
    """
    Register a duty in the `duties` dictionary.

    Arguments:
        func: The callable to register as a duty.
        name: The duty name.
        pre: Pre-duties.
        post: Post-duties.
        opts: Options passed to the context.

    Returns:
        The registered duty.
    """
    name = name or func.__name__
    description = inspect.getdoc(func) or ""
    duties[name] = Duty(name, description, func, pre=pre, post=post, opts=opts)
    return duties[name]


def duty(*args, **kwargs) -> Union[Callable, Duty]:
    """
    Decorate a callable to transform it and register it as a duty.

    Arguments:
        args: One callable.
        kwargs: Context options.

    Raises:
        ValueError: When the decorator is misused.

    Examples:
        Decorate a function:

        ```python
        @duty
        def clean(ctx):
            ctx.run("rm -rf build", silent=True)
        ```

        Pass options to the context:

        ```python
        @duty(silent=True)
        def clean(ctx):
            ctx.run("rm -rf build")  # silent=True is implied
        ```

    Returns:
        A duty when used without parentheses, a decorator otherwise.
    """
    if args and kwargs:
        raise ValueError("The duty decorator only accepts kwargs")
    if args:
        if len(args) > 1:
            raise ValueError(
                "The duty decorator only accepts a function as first argument " "and no extra positional args",
            )
        return register_duty(args[0])

    def decorator(func):
        return register_duty(func, **kwargs)

    return decorator
