"""Module containing the decorator provided to users."""

import inspect
from typing import Callable, Iterable, Optional, Union

from duty.collection import Duty, DutyListType


def create_duty(
    func: Callable,
    name: Optional[str] = None,
    aliases: Optional[Iterable[str]] = None,
    pre: Optional[DutyListType] = None,
    post: Optional[DutyListType] = None,
    **opts,
) -> Duty:
    """
    Register a duty in the collection.

    Parameters:
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
    duty = Duty(name, description, func, aliases=aliases, pre=pre, post=post, opts=opts)
    duty.__name__ = name  # type: ignore
    duty.__doc__ = description
    duty.__wrapped__ = func  # type: ignore  # noqa: WPS609
    return duty


def duty(*args, **kwargs) -> Union[Callable, Duty]:
    """
    Decorate a callable to transform it and register it as a duty.

    Parameters:
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
        return create_duty(args[0], **kwargs)

    def decorator(func):
        return create_duty(func, **kwargs)

    return decorator
