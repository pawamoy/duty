"""Tests about running duties."""

from __future__ import annotations

from typing import NoReturn
from unittest.mock import NonCallableMock

import pytest

from duty._internal.collection import Collection, Duty
from duty._internal.decorator import duty as decorate
from duty._internal.exceptions import DutyFailure

INTERRUPT_CODE = 130


def test_run_duty() -> None:
    """Run a duty."""
    duty = Duty("name", "description", lambda ctx: 1)
    assert duty.run() is None  # type: ignore[func-returns-value]
    assert duty(duty.context) is None  # type: ignore[func-returns-value]


def test_run_pre_post_duties_lambdas() -> None:
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


def test_run_pre_post_duties_instances() -> None:
    """Run pre- and post- duties as duties."""
    pre_calls = []
    post_calls = []

    pre_duty = Duty("pre", "", lambda ctx: pre_calls.append(True))
    post_duty = Duty("post", "", lambda ctx: post_calls.append(True))

    duty = Duty(
        name="name",
        description="description",
        function=lambda ctx: None,
        pre=[pre_duty],
        post=[post_duty],
    )

    duty.run()

    assert pre_calls[0] is True
    assert post_calls[0] is True


def test_run_pre_post_duties_refs() -> None:
    """Run pre- and post- duties as duties references."""
    pre_calls = []
    post_calls = []

    collection = Collection()
    collection.add(decorate(lambda ctx: pre_calls.append(True), name="pre"))  # type: ignore[call-overload]
    collection.add(decorate(lambda ctx: post_calls.append(True), name="post"))  # type: ignore[call-overload]

    duty = Duty("name", "description", lambda ctx: None, collection=collection, pre=["pre"], post=["post"])
    duty.run()

    assert pre_calls[0] is True
    assert post_calls[0] is True


def test_dont_run_other_pre_post_duties() -> None:
    """Don't run other types of pre- and post- duties."""
    pre_duty = NonCallableMock()
    post_duty = NonCallableMock()

    duty = Duty("name", "description", lambda ctx: 0, pre=[pre_duty], post=[post_duty])
    duty.run()

    assert not pre_duty.called
    assert not post_duty.called


def test_code_when_keyboard_interrupt() -> None:
    """Return a code 130 on keyboard interruption."""

    def interrupt() -> NoReturn:
        raise KeyboardInterrupt

    with pytest.raises(DutyFailure) as excinfo:
        Duty("name", "description", lambda ctx: ctx.run(interrupt)).run()
    assert excinfo.value.code == INTERRUPT_CODE


def test_dont_raise_duty_failure() -> None:
    """Don't raise a duty failure on success."""
    duty = Duty("n", "d", lambda ctx: ctx.run(lambda: 0))
    assert not duty.run()  # type: ignore[func-returns-value]


def test_cant_find_duty_without_collection() -> None:
    """Check that we can't find a duty with its name without a collection."""
    duty = decorate(lambda ctx: None, name="duty1", post=["duty2"])  # type: ignore[call-overload]
    with pytest.raises(RuntimeError):
        duty.run()
