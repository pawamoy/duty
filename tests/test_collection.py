"""Tests for the `collection` module."""

import pytest

from duty.collection import Collection, Duty
from duty.decorator import duty as decorate


def test_instantiate_duty():
    """Instantiate a duty."""
    assert Duty("name", "description", lambda: None)
    assert Duty("name", "description", lambda: None, pre=[0, 1], post=[2])


def test_dont_get_duty():
    """Don't find a duty."""
    collection = Collection()
    with pytest.raises(KeyError):
        collection.get("hello")


def test_register_aliases():
    """Register a duty and its aliases."""
    duty = decorate(lambda ctx: None, name="hello", aliases=["HELLO", "_hello_", ".hello."])
    collection = Collection()
    collection.add(duty)
    assert collection.get("hello")
    assert collection.get("HELLO")
    assert collection.get("_hello_")
    assert collection.get(".hello.")


def test_replace_name_and_set_alias():
    """Replace underscores by dashes in duties names."""
    collection = Collection()
    collection.add(decorate(lambda ctx: None, name="snake_case"))
    assert collection.get("snake_case") is collection.get("snake-case")
