"""Module containing callables for many tools.

Tip: Call to developers!
    If you are the author or maintainer of one of the tools we support
    (or more generally if you are the author/maintainer of a Python CLI/library),
    we kindly request that you add such a callable to your code base. Why?

    - Most of the time, all `duty` can do is hook into the CLI entrypoint
        for the lack of a better alternative. This is not ideal because
        we have to translate function arguments to CLI arguments,
        that are then parsed again and translated back to Python objects
        by the tool itself. This is not efficient.
    - It is not feasible for `duty` to maintain callables for different versions
        of these tools. Having the callables maintained in the tools
        themselves would make this support transparent.
    - We believe it simply provides a better user- *and* developer-experience.
        Clear separation of concerns: don't intertwine logic into the CLI parser.
        Easy to maintain, easy to test. The CLI parser just has to translate CLI args
        to their equivalent Python arguments.

    Tips for writing such a library entry point:

    - Make it equivalent to the CLI entry point: every flag and option must have an equivalent parameter.
        Slight customizations can be made to support `--flag` / `--no-flag` with single parameters.
    - Use only built-in types: don't make users import and use objects from your API.
        For example, accept a list of strings, not a list of `MyCustomClass` instances.
"""

from __future__ import annotations

from functools import wraps
from typing import Callable

from failprint.lazy import lazy as failprint_lazy


def lazy(name: str | None = None) -> Callable:
    """Transform a callable into a lazy callable.

    Also assign the given name to the callable, for better display.

    Parameters:
        name: The name to assign to the callable.

    Returns:
        A lazy callable.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):  # noqa: ANN002,ANN003,ANN202
            return func(*args, **kwargs)

        if name:
            inner.__name__ = name
        return failprint_lazy(inner)

    return decorator
