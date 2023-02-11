"""Tests for the `decorator` module."""

import inspect

import pytest

from duty.context import Context
from duty.decorator import duty as decorate
from duty.exceptions import DutyFailure


def test_accept_one_posarg_when_decorating():
    """Accept only one positional argument when decorating."""
    with pytest.raises(ValueError, match="accepts only one positional argument"):
        decorate(0, 1)


def test_skipping():
    """Wrap function that must be skipped."""
    duty = decorate(lambda ctx: ctx.run("false"), skip_if=True)
    # no DutyFailure raised
    assert duty.run() is None
    with pytest.raises(DutyFailure):
        assert inspect.unwrap(duty)(Context({}))
