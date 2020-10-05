"""Tests for the `logic` module."""

from unittest.mock import NonCallableMock

import pytest

from duty.logic import Duty, DutyFailure
from duty.logic import duty as decorate
from duty.logic import get_duty

INTERRUPT_CODE = 130


def test_instantiate_duty():
    """Instantiate a duty."""
    assert Duty("name", "description", lambda: None)
    assert Duty("name", "description", lambda: None, pre=[0, 1], post=[2])


def test_run_duty():
    """Run a duty."""
    duty = Duty("name", "description", lambda ctx: None)
    assert duty.run() is None
    assert duty() is None


def test_run_pre_post_duties_lambdas():
    """Run pre- and post- duties as lambdas."""
    pre_calls = []
    post_calls = []

    duty = Duty(
        "name",
        "description",
        lambda ctx: None,
        pre=[lambda ctx: pre_calls.append(True)],
        post=[lambda ctx: post_calls.append(True)],
    )

    duty.run()

    assert pre_calls[0] is True
    assert post_calls[0] is True


def test_run_pre_post_duties_instances():
    """Run pre- and post- duties as duties."""
    pre_calls = []
    post_calls = []

    pre_duty = Duty("pre", "", lambda ctx: pre_calls.append(True))
    post_duty = Duty("post", "", lambda ctx: post_calls.append(True))

    duty = Duty("name", "description", lambda ctx: None, pre=[pre_duty], post=[post_duty])

    duty.run()

    assert pre_calls[0] is True
    assert post_calls[0] is True


def test_run_pre_post_duties_refs():
    """Run pre- and post- duties as duties references."""
    pre_calls = []
    post_calls = []

    decorate(lambda ctx: pre_calls.append(True), name="pre")
    decorate(lambda ctx: post_calls.append(True), name="post")

    duty = Duty("name", "description", lambda ctx: None, pre=["pre"], post=["post"])

    duty.run()

    assert pre_calls[0] is True
    assert post_calls[0] is True


def test_dont_run_other_pre_post_duties():
    """Don't run other types of pre- and post- duties."""
    pre_duty = NonCallableMock()
    post_duty = NonCallableMock()

    duty = Duty("name", "description", lambda ctx: 0, pre=[pre_duty], post=[post_duty])
    duty.run()

    assert not pre_duty.called
    assert not post_duty.called


def test_code_when_keyboard_interrupt():
    """Return a code 130 on keyboard interruption."""  # noqa: DAR401,D202 (ctrl-c not raised, black)

    def interrupt():  # noqa: WPS430 (nested function)
        raise KeyboardInterrupt

    with pytest.raises(DutyFailure) as excinfo:
        Duty("name", "description", lambda ctx: ctx.run(interrupt)).run()
    assert excinfo.value.code == INTERRUPT_CODE  # noqa: WPS441 (after block)


def test_dont_raise_duty_failure():
    """Don't raise a duty failure on success."""
    assert not Duty("n", "d", lambda ctx: ctx.run(lambda: 0))()  # noqa: WPS430,WPS522 (lambdas)


def test_dont_get_duty():
    """Don't find a duty."""
    with pytest.raises(KeyError):
        get_duty("hello")


def test_register_aliases():
    """Register a duty and its aliases."""
    decorate(lambda ctx: None, name="hello", aliases=["HELLO", "_hello_", ".hello."])
    assert get_duty("hello")
    assert get_duty("HELLO")
    assert get_duty("_hello_")
    assert get_duty(".hello.")


def test_replace_name_and_set_alias():
    """Replace underscores by dashes in duties names."""
    decorate(lambda ctx: None, name="snake_case")
    assert get_duty("snake_case") is get_duty("snake-case")


def test_accept_one_posarg_when_decorating():
    """Accept only one positional argument when decorating."""
    with pytest.raises(ValueError, match="accepts only one positional argument"):
        decorate(0, 1)
