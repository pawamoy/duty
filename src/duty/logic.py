"""Module containing all the logic."""

import inspect
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from failprint.runners import run as failprint_run

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
        self.run_duties(self.pre)
        self.function(self.context, *args, **kwargs)
        self.run_duties(self.post)

    def run_duties(self, duties_list: DutyListType) -> None:
        """
        Run a list of duties.

        Arguments:
            duties_list: The list of duties to run.
        """
        for duty_item in duties_list:
            if isinstance(duty_item, Duty):
                duty_item.run()
            elif isinstance(duty_item, str):
                get_duty(duty_item).run()
            elif callable(duty_item):
                duty_item(self.context)


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
duties_aliases: Dict[str, Duty] = {}


def get_duty(name_or_alias: str) -> Duty:
    """
    Get a duty by its name or alias.

    Arguments:
        name_or_alias: The name or alias of the duty.

    Returns:
        A duty.
    """
    try:
        return duties[name_or_alias]
    except KeyError:
        return duties_aliases[name_or_alias]


def register_duty(
    func: Callable,
    name: Optional[str] = None,
    aliases: Optional[Iterable[str]] = None,
    pre: Optional[DutyListType] = None,
    post: Optional[DutyListType] = None,
    **opts,
) -> Duty:
    """
    Register a duty in the `duties` dictionary.

    Arguments:
        func: The callable to register as a duty.
        name: The duty name.
        aliases: A set of aliases for this duty.
        pre: Pre-duties.
        post: Post-duties.
        opts: Options passed to the context.

    Returns:
        The registered duty.
    """
    aliases = set(aliases) if aliases else set()
    name = name or func.__name__
    dash_name = name.replace("_", "-")
    if name != dash_name:
        aliases.add(name)
        name = dash_name
    description = inspect.getdoc(func) or ""
    duties[name] = Duty(name, description, func, pre=pre, post=post, opts=opts)
    for alias in aliases:
        duties_aliases[alias] = duties[name]
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
    if args:
        if len(args) > 1:
            raise ValueError(
                "The duty decorator accepts only one positional argument",
            )
        return register_duty(args[0], **kwargs)

    def decorator(func):
        return register_duty(func, **kwargs)

    return decorator
