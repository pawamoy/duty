# This module contains logic used to validate parameters passed to duties.
#
# We validate the parameters before running the duties,
# effectively checking all CLI arguments and failing early
# if they are incorrect.

from __future__ import annotations

import sys
import textwrap
from contextlib import suppress
from functools import cached_property, partial
from inspect import Parameter, Signature, signature
from typing import TYPE_CHECKING, Any, Callable, ForwardRef, Union, get_args, get_origin

if TYPE_CHECKING:
    from collections.abc import Sequence

# YORE: EOL 3.9: Replace block with lines 6-13.
if sys.version_info < (3, 10):
    from eval_type_backport import eval_type_backport as _eval_type

    _union_types = (Union,)
else:
    from types import UnionType
    from typing import _eval_type  # type: ignore[attr-defined]

    if sys.version_info >= (3, 13):
        _eval_type = partial(_eval_type, type_params=None)
    _union_types = (Union, UnionType)


def to_bool(value: str) -> bool:
    """Convert a string to a boolean.

    Parameters:
        value: The string to convert.

    Returns:
        True or False.
    """
    return value.lower() not in {"", "0", "no", "n", "false", "off"}


def cast_arg(arg: Any, annotation: Any) -> Any:
    """Cast an argument using a type annotation.

    Parameters:
        arg: The argument value.
        annotation: A type annotation.

    Returns:
        The cast value.
    """
    if annotation is Parameter.empty:
        return arg
    if annotation is bool:
        annotation = to_bool
    if get_origin(annotation) in _union_types:
        for sub_annotation in get_args(annotation):
            if sub_annotation is type(None):
                continue
            with suppress(Exception):
                return cast_arg(arg, sub_annotation)
    try:
        return annotation(arg)
    except Exception:  # noqa: BLE001
        return arg


class ParamsCaster:
    """A helper class to cast parameters based on a function's signature annotations."""

    def __init__(self, signature: Signature) -> None:
        """Initialize the object.

        Parameters:
            signature: The signature to use to cast arguments.
        """
        self.params_dict = signature.parameters
        """A dictionary of parameters, indexed by their name."""
        self.params_list = list(self.params_dict.values())
        """A list of parameters, in the order they appear in the signature."""

    @cached_property
    def var_positional_position(self) -> int:
        """Give the position of the variable positional parameter in the signature.

        Returns:
            The position of the variable positional parameter.
        """
        for pos, param in enumerate(self.params_list):
            if param.kind is Parameter.VAR_POSITIONAL:
                return pos
        return -1

    @cached_property
    def has_var_positional(self) -> bool:
        """Tell if there is a variable positional parameter.

        Returns:
            True or False.
        """
        return self.var_positional_position >= 0

    @cached_property
    def var_positional_annotation(self) -> Any:
        """Give the variable positional parameter (`*args`) annotation if any.

        Returns:
            The variable positional parameter annotation.
        """
        return self.params_list[self.var_positional_position].annotation

    @cached_property
    def var_keyword_annotation(self) -> Any:
        """Give the variable keyword parameter (`**kwargs`) annotation if any.

        Returns:
            The variable keyword parameter annotation.
        """
        for param in self.params_list:
            if param.kind is Parameter.VAR_KEYWORD:
                return param.annotation
        return Parameter.empty

    def annotation_at_pos(self, pos: int) -> Any:
        """Give the annotation for the parameter at the given position.

        Parameters:
            pos: The position of the parameter.

        Returns:
            The positional parameter annotation.
        """
        return self.params_list[pos].annotation

    def eaten_by_var_positional(self, pos: int) -> bool:
        """Tell if the parameter at this position is eaten by a variable positional parameter.

        Parameters:
            pos: The position of the parameter.

        Returns:
            Whether the parameter is eaten.
        """
        return self.has_var_positional and pos >= self.var_positional_position

    def cast_posarg(self, pos: int, arg: Any) -> Any:
        """Cast a positional argument.

        Parameters:
            pos: The position of the argument in the signature.
            arg: The argument value.

        Returns:
            The cast value.
        """
        if self.eaten_by_var_positional(pos):
            return cast_arg(arg, self.var_positional_annotation)
        return cast_arg(arg, self.annotation_at_pos(pos))

    def cast_kwarg(self, name: str, value: Any) -> Any:
        """Cast a keyword argument.

        Parameters:
            name: The name of the argument in the signature.
            value: The argument value.

        Returns:
            The cast value.
        """
        if name in self.params_dict:
            return cast_arg(value, self.params_dict[name].annotation)
        return cast_arg(value, self.var_keyword_annotation)

    def cast(self, *args: Any, **kwargs: Any) -> tuple[Sequence, dict[str, Any]]:
        """Cast all positional and keyword arguments.

        Parameters:
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Returns:
            The cast arguments.
        """
        positional = tuple(self.cast_posarg(pos, arg) for pos, arg in enumerate(args))
        keyword = {name: self.cast_kwarg(name, value) for name, value in kwargs.items()}
        return positional, keyword


def _get_params_caster(func: Callable, *args: Any, **kwargs: Any) -> ParamsCaster:
    duties_module = sys.modules[func.__module__]
    exec_globals = dict(duties_module.__dict__)
    eval_str = False
    for name in list(exec_globals.keys()):
        if exec_globals[name] is annotations:
            eval_str = True
            del exec_globals[name]
            break
    exec_globals["__context_above"] = {}

    # Don't keep first parameter: context.
    params = list(signature(func).parameters.values())[1:]
    params_no_types = [Parameter(param.name, param.kind, default=param.default) for param in params]
    code_sig = Signature(parameters=params_no_types)
    if eval_str:
        params_types = [
            Parameter(
                param.name,
                param.kind,
                default=param.default,
                annotation=(
                    _eval_type(
                        ForwardRef(param.annotation) if isinstance(param.annotation, str) else param.annotation,
                        exec_globals,
                        {},
                    )
                    if param.annotation is not Parameter.empty
                    else type(param.default)
                ),
            )
            for param in params
        ]
    else:
        params_types = params
    cast_sig = Signature(parameters=params_types)

    code = f"""
        import inspect
        def {func.__name__}{code_sig}: ...
        __context_above['func'] = {func.__name__}
    """

    exec(textwrap.dedent(code), exec_globals)  # noqa: S102
    func = exec_globals["__context_above"]["func"]

    # Trigger TypeError early.
    func(*args, **kwargs)

    return ParamsCaster(cast_sig)


def validate(
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> tuple[Sequence, dict[str, Any]]:
    """Validate positional and keyword arguments against a function.

    First we clone the function, removing the first parameter (the context)
    and the body, to fail early with a `TypeError` if the arguments
    are incorrect: not enough, too much, in the wrong order, etc.

    Then we cast all the arguments using the function's signature
    and we return them.

    Parameters:
        func: The function to copy.
        *args: The positional arguments.
        **kwargs: The keyword arguments.

    Returns:
        The casted arguments.
    """
    return _get_params_caster(func, *args, **kwargs).cast(*args, **kwargs)
