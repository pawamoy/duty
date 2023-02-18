"""Tests for the `validation` module."""

import sys
from inspect import Parameter

import pytest

from duty.validation import ParamsCaster, cast_arg, to_bool
from tests.fixtures import validation as validation_fixture

if sys.version_info >= (3, 8, 0):
    from tests.fixtures import validation_38 as validation_fixture_38


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
def test_bool_casting(value, expected):
    """Check that we correctly cast string values to booleans.

    Parameters:
        value: The value to cast.
        expected: The expected result.
    """
    assert to_bool(value) == expected


class CustomType1:
    """Dummy type to test type-casting."""

    def __init__(self, value):  # noqa: D107
        self.value = value

    def __eq__(self, other):
        return self.value == other.value


class CustomType2:
    """Dummy type to test type-casting."""

    def __init__(self, value, extra):  # noqa: D107
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
def test_cast_arg(arg, annotation, expected):
    """Check that arguments are properly casted given an annotation.

    Parameters:
        arg: The argument value to cast.
        annotation: The annotation to use.
        expected: The expected result.
    """
    assert cast_arg(arg, annotation) == expected


_parametrization = [
    (validation_fixture.no_params, (), {}, (), {}),
    (validation_fixture.pos_or_kw_param, ("1",), {}, (1,), {}),
    (validation_fixture.pos_or_kw_param, (), {"a": "1"}, (), {"a": 1}),
    (validation_fixture.pos_or_kw_params, ("1", "2"), {}, (1, 2), {}),
    (validation_fixture.pos_or_kw_params, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (validation_fixture.pos_or_kw_params, (), {"a": "1", "b": "2"}, (), {"a": 1, "b": 2}),
    (validation_fixture.varpos_param, (), {}, (), {}),
    (validation_fixture.varpos_param, ("1", "2"), {}, (1, 2), {}),
    (validation_fixture.pos_and_varpos_param, ("1",), {}, (1,), {}),
    (validation_fixture.pos_and_varpos_param, ("1", "2"), {}, (1, 2), {}),
    (validation_fixture.pos_and_varpos_param, ("1", "2", "3"), {}, (1, 2, 3), {}),
    (validation_fixture.kwonly_param, (), {"b": "1"}, (), {"b": 1}),
    (validation_fixture.kwonly_param, ("2",), {"b": "1"}, (2,), {"b": 1}),
    (
        validation_fixture.kwonly_param,
        (
            "2",
            "3",
        ),
        {"b": "1"},
        (2, 3),
        {"b": 1},
    ),
    (validation_fixture.varkw_param, ("1",), {}, (1,), {}),
    (validation_fixture.varkw_param, ("1",), {"b": "2"}, (1,), {"b": 2}),
    (validation_fixture.varkw_param, ("1",), {"b": "2", "c": "3"}, (1,), {"b": 2, "c": 3}),
    (validation_fixture.varkw_no_annotation, (), {"a": "1"}, (), {"a": "1"}),
    (validation_fixture.no_params, (), {"a": "1"}, (), {"a": "1"}),
]

if sys.version_info >= (3, 8, 0):
    _parametrization.extend(
        [
            (validation_fixture_38.posonly_marker, ("1", "2"), {}, (1, 2), {}),
            (validation_fixture_38.posonly_marker, ("1",), {"b": "2"}, (1,), {"b": 2}),
            (validation_fixture_38.kwonly_marker, ("1",), {"b": "2"}, (1,), {"b": 2}),
            (validation_fixture_38.kwonly_marker, (), {"a": "1", "b": "2"}, (), {"a": 1, "b": 2}),
            (validation_fixture_38.only_markers, ("1",), {"b": "2", "c": "3"}, (1,), {"b": 2, "c": 3}),
            (validation_fixture_38.only_markers, ("1", "2"), {"c": "3"}, (1, 2), {"c": 3}),
            (
                validation_fixture_38.full,
                ("1", "2", "3", "4"),
                {"d": "5", "e": "6", "f": "7"},
                (1, 2, 3, 4),
                {"d": 5, "e": 6, "f": 7},
            ),
            (
                validation_fixture_38.full,
                ("1", "3", "4"),
                {"b": "2", "d": "5"},
                (1, 3, 4),
                {"b": 2, "d": 5},
            ),
        ],
    )


@pytest.mark.parametrize(
    ("func", "args", "kwargs", "expected_args", "expected_kwargs"),
    _parametrization,
)
def test_params_caster(func, args, kwargs, expected_args, expected_kwargs):
    """Test the whole parameters casting helper class.

    Parameters:
        func: The function to work with.
        args: The positional arguments to cast.
        kwargs: The keyword arguments to cast.
        expected_args: The expected positional arguments result.
        expected_kwargs: The expected keyword arguments result.
    """
    caster = ParamsCaster(func)
    new_args, new_kwargs = caster.cast(*args, **kwargs)
    assert new_args == expected_args
    assert new_kwargs == expected_kwargs
