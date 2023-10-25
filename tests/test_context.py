"""Tests for the `context` module."""

from __future__ import annotations

from collections import namedtuple
from pathlib import Path

import pytest

from duty import context
from duty.exceptions import DutyFailure

RunResult = namedtuple("RunResult", "code output")  # noqa: PYI024


def test_allow_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the `allow_overrides` option.

    Parameters:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({"a": 1}, {"a": 2})
    records = []
    monkeypatch.setattr(context, "failprint_run", lambda _, **opts: RunResult(records.append(opts), ""))  # type: ignore[func-returns-value]
    ctx.run("")
    ctx.run("", allow_overrides=False)
    ctx.run("", allow_overrides=True)
    ctx.run("", allow_overrides=False, a=3)
    assert records[0]["a"] == 2
    assert records[1]["a"] == 1
    assert records[2]["a"] == 2
    assert records[3]["a"] == 3


def test_options_context_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test changing options using the context manager.

    Parameters:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({"a": 1}, {"a": 2})
    records = []
    monkeypatch.setattr(context, "failprint_run", lambda _, **opts: RunResult(records.append(opts), ""))  # type: ignore[func-returns-value]

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


def test_workdir(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the `workdir` option.

    Parameters:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({})
    monkeypatch.setattr(context, "failprint_run", lambda _: RunResult(len(Path.cwd().parts), ""))
    records = []
    with pytest.raises(DutyFailure) as failure:
        ctx.run("")
    records.append(failure.value.code)
    with pytest.raises(DutyFailure) as failure:
        ctx.run("", workdir="..")
    records.append(failure.value.code)
    assert records[0] == records[1] + 1


def test_workdir_as_context_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the `workdir` option as a context manager, and the `cd` context manager.

    Parameters:
        monkeypatch: A Pytest fixture to monkeypatch objects.
    """
    ctx = context.Context({})
    monkeypatch.setattr(context, "failprint_run", lambda _: RunResult(len(Path.cwd().parts), ""))
    records = []
    with pytest.raises(DutyFailure) as failure, ctx.options(workdir=".."):
        ctx.run("")
    records.append(failure.value.code)
    with pytest.raises(DutyFailure) as failure, ctx.cd("../.."):
        ctx.run("")
    records.append(failure.value.code)
    with pytest.raises(DutyFailure) as failure, ctx.cd(".."), ctx.options(workdir="../.."):
        ctx.run("")
    records.append(failure.value.code)
    with pytest.raises(DutyFailure) as failure, ctx.cd("../../.."):
        ctx.run("", workdir="..")
    records.append(failure.value.code)

    base = records[0]
    assert records == [base, base - 1, base - 2, base - 3]
