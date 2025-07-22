"""Tests for the `decorator` module."""

from __future__ import annotations

import inspect

import pytest

from duty._internal.context import Context
from duty._internal.decorator import duty as decorate
from duty._internal.exceptions import DutyFailure


def test_accept_one_posarg_when_decorating() -> None:
    """Accept only one positional argument when decorating."""
    with pytest.raises(ValueError, match="accepts only one positional argument"):
        decorate(0, 1)  # type: ignore[call-overload]


def test_skipping() -> None:
    """Wrap function that must be skipped."""
    duty = decorate(lambda ctx: ctx.run("false"), skip_if=True)  # type: ignore[call-overload]
    # no DutyFailure raised
    assert duty.run() is None
    with pytest.raises(DutyFailure):
        assert inspect.unwrap(duty)(Context({}))
