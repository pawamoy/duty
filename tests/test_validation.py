"""Tests for the `validation` module."""

from __future__ import annotations

from inspect import Parameter
from typing import Any, Callable

import pytest

from duty._internal.validation import _get_params_caster, cast_arg, to_bool
from tests.fixtures import validation as valfix


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("y", True),
        ("Y", True),
        ("yes", True),
        ("YES", True),
        ("on", True),
        ("ON", True),
        ("true", True),
        ("TRUE", True),
        ("anything else", True),
        ("-1", True),
        ("1", True),
        ("", False),
        ("n", False),
        ("N", False),
        ("no", False),
        ("NO", False),
        ("false", False),
        ("FALSE", False),
        ("off", False),
        ("OFF", False),
    ],
)
def test_bool_casting(value: str, expected: bool) -> None:
    """Check that we correctly cast string values to booleans.

    Parameters:
        value: The value to cast.
        expected: The expected result.
    """
    assert to_bool(value) == expected


class CustomType1:  # noqa: PLW1641
    """Dummy type to test type-casting."""

    def __init__(self, value: str):  # noqa: D107
        self.value = value

    def __eq__(self, other: object):
        return self.value == other.value  # type: ignore[attr-defined]


class CustomType2:
    """Dummy type to test type-casting."""

    def __init__(self, value, extra):  # noqa: ANN001,D107
        ...  # pragma: no cover


@pytest.mark.parametrize(
    ("arg", "annotation", "expected"),
    [
        ("hello", Parameter.empty, "hello"),
        ("off", bool, False),
        ("on", bool, True),
        ("1", int, 1),
        ("1", float, 1.0),
        ("fie", str, "fie"),
        ("fih", CustomType1, CustomType1("fih")),
        ("foh", CustomType2, "foh"),
    ],
)
def test_cast_arg(arg: str, annotation: Any, expected: Any) -> None:
    """Check that arguments are properly casted given an annotation.

    Parameters:
        arg: The argument value to cast.
        annotation: The annotation to use.
        expected: The expected result.
    """
    assert cast_arg(arg, annotation) == expected


_parametrization = [
    (valfix.no_params, (), {}, (), {}),
    (valfix.pos_or_kw_param, ("1",), {}, (1,), {}),
    (valfix.pos_or_kw_param, (), {"a": "1"}, (), {"a": 1}),
    (valfix.pos_or_kw_params, ("1", "2"), {}, (1, 2), {}),
    (valfix.pos_or_kw_params, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (valfix.pos_or_kw_params, (), {"a": "1", "b": "2"}, (), {"a": 1, "b": 2}),
    (valfix.varpos_param, (), {}, (), {}),
    (valfix.varpos_param, ("1", "2"), {}, (1, 2), {}),
    (valfix.pos_and_varpos_param, ("1",), {}, (1,), {}),
    (valfix.pos_and_varpos_param, ("1", "2"), {}, (1, 2), {}),
    (valfix.pos_and_varpos_param, ("1", "2", "3"), {}, (1, 2, 3), {}),
    (valfix.kwonly_param, (), {"b": "1"}, (), {"b": 1}),
    (valfix.kwonly_param, ("2",), {"b": "1"}, (2,), {"b": 1}),
    (valfix.kwonly_param, ("2", "3"), {"b": "1"}, (2, 3), {"b": 1}),
    (valfix.varkw_param, ("1",), {}, (1,), {}),
    (valfix.varkw_param, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (valfix.varkw_param, ("1",), {"b": "2", "c": "3"}, (1,), {"b": 2, "c": 3}),
    (valfix.varkw_no_annotation, (), {"a": "1"}, (), {"a": "1"}),
    (valfix.posonly_marker, ("1", "2"), {}, (1, 2), {}),
    (valfix.posonly_marker, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (valfix.kwonly_marker, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (valfix.kwonly_marker, (), {"a": "1", "b": "2"}, (), {"a": 1, "b": 2}),
    (valfix.only_markers, ("1",), {"b": "2", "c": "3"}, (1,), {"b": 2, "c": 3}),
    (valfix.only_markers, ("1", "2"), {"c": "3"}, (1, 2), {"c": 3}),
    (valfix.full, ("1", "2", "3", "4"), {"d": "5", "e": "6", "f": "7"}, (1, 2, 3, 4), {"d": 5, "e": 6, "f": 7}),
]


@pytest.mark.parametrize(
    ("func", "args", "kwargs", "expected_args", "expected_kwargs"),
    _parametrization,
)
def test_params_caster(func: Callable, args: tuple, kwargs: dict, expected_args: tuple, expected_kwargs: dict) -> None:
    """Test the whole parameters casting helper class.

    Parameters:
        func: The function to work with.
        args: The positional arguments to cast.
        kwargs: The keyword arguments to cast.
        expected_args: The expected positional arguments result.
        expected_kwargs: The expected keyword arguments result.
    """
    caster = _get_params_caster(func, *args, **kwargs)
    new_args, new_kwargs = caster.cast(*args, **kwargs)
    assert new_args == expected_args
    assert new_kwargs == expected_kwargs


def test_casting_based_on_default_value_type() -> None:
    """Test that we cast according to the default value type when there is no annotation."""

    def func(ctx, a=0):  # noqa: ANN202, ANN001
        ...

    caster = _get_params_caster(func, a="1")
    _, kwargs = caster.cast(a="1")
    assert kwargs == {"a": 1}


def test_validating_modern_annotations() -> None:
    """Test modern type annotations in function signatures."""

    def func(ctx, a: int | None = None):  # noqa: ANN202, ANN001
        ...

    caster = _get_params_caster(func, a=1)
    _, kwargs = caster.cast(a="1")
    assert kwargs == {"a": 1}
    caster = _get_params_caster(func, a=None)
    _, kwargs = caster.cast(a=None)
    assert kwargs == {"a": None}
    caster = _get_params_caster(func)
    _, kwargs = caster.cast()
    assert kwargs == {}
