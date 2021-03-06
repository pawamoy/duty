"""Tests for the `context` module."""

import os
from collections import namedtuple
from pathlib import Path

import pytest

from duty import context
from duty.exceptions import DutyFailure

_RunResult = namedtuple("RunResult", "code output")


def test_allow_overrides(monkeypatch):
    """
    Test the `allow_overrides` option.

    Arguments:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({"a": 1}, {"a": 2})
    records = []
    monkeypatch.setattr(context, "failprint_run", lambda _, **opts: _RunResult(records.append(opts), ""))
    ctx.run("")
    ctx.run("", allow_overrides=False)
    ctx.run("", allow_overrides=True)
    ctx.run("", allow_overrides=False, a=3)
    assert records[0]["a"] == 2
    assert records[1]["a"] == 1
    assert records[2]["a"] == 2
    assert records[3]["a"] == 3


def test_options_context_manager(monkeypatch):
    """
    Test changing options using the context manager.

    Arguments:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({"a": 1}, {"a": 2})
    records = []
    monkeypatch.setattr(context, "failprint_run", lambda _, **opts: _RunResult(records.append(opts), ""))

    with ctx.options(a=3):
        ctx.run("")  # should be overridden by 2
        with ctx.options(a=4, allow_overrides=False):
            ctx.run("")  # should be 4
            ctx.run("", allow_overrides=True)  # should be 2
        ctx.run("", allow_overrides=False)  # should be 3

    assert records[0]["a"] == 2
    assert records[1]["a"] == 4
    assert records[2]["a"] == 2
    assert records[3]["a"] == 3


def test_workdir(monkeypatch):
    """
    Test the `workdir` option.

    Arguments:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({})
    monkeypatch.setattr(context, "failprint_run", lambda _: _RunResult(len(Path(os.getcwd()).parts), ""))
    records = []
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        ctx.run("")
    records.append(failure.value.code)  # noqa: WPS441
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        ctx.run("", workdir="..")
    records.append(failure.value.code)  # noqa: WPS441
    assert records[0] == records[1] + 1


def test_workdir_as_context_manager(monkeypatch):
    """
    Test the `workdir` option as a context manager, and the `cd` context manager.

    Arguments:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({})
    monkeypatch.setattr(context, "failprint_run", lambda _: _RunResult(len(Path(os.getcwd()).parts), ""))
    records = []
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        with ctx.options(workdir=".."):
            ctx.run("")
    records.append(failure.value.code)  # noqa: WPS441
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        with ctx.cd("../.."):
            ctx.run("")
    records.append(failure.value.code)  # noqa: WPS441
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        with ctx.cd(".."):
            with ctx.options(workdir="../.."):
                ctx.run("")
    records.append(failure.value.code)  # noqa: WPS441
    with pytest.raises(DutyFailure) as failure:  # noqa: WPS440,PT012
        with ctx.cd("../../.."):
            ctx.run("", workdir="..")
    records.append(failure.value.code)  # noqa: WPS441

    base = records[0]
    assert records == [base, base - 1, base - 2, base - 3]
