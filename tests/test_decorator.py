# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
