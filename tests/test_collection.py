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


def test_clear_collection():
    """Check that duties and their aliases are correctly cleared from a collection."""
    collection = Collection()
    collection.add(decorate(lambda ctx: None, name="duty_1"))
    collection.clear()
    with pytest.raises(KeyError):
        collection.get("duty-1")


def test_add_duty_to_multiple_collections():
    """Check what happens when adding the same duty to multiple collections."""
    collection1 = Collection()
    collection2 = Collection()

    duty = decorate(lambda ctx: None, name="duty")

    collection1.add(duty)
    collection2.add(duty)

    duty1 = collection1.get("duty")
    duty2 = collection2.get("duty")

    assert duty1 is not duty2
    assert duty1.collection is collection1
    assert duty2.collection is collection2
