"""Tests for the `decorator` module."""

import pytest

from duty.decorator import duty as decorate


def test_accept_one_posarg_when_decorating():
    """Accept only one positional argument when decorating."""
    with pytest.raises(ValueError, match="accepts only one positional argument"):
        decorate(0, 1)
