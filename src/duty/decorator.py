"""Module containing the decorator provided to users."""
from __future__ import annotations

import inspect
from typing import Any, Callable, Iterable, overload

from duty.collection import Duty, DutyListType


def create_duty(
    func: Callable,
    name: str | None = None,
    aliases: Iterable[str] | None = None,
    pre: DutyListType | None = None,
    post: DutyListType | None = None,
    **opts: Any,
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


@overload
def duty(**kwargs: Any) -> Callable[[Callable], Duty]:  # type: ignore[misc]
    ...


@overload
def duty(func: Callable) -> Duty:
    ...


def duty(*args: Any, **kwargs: Any) -> Callable | Duty:
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
