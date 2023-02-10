"""
Duty package.

A simple task runner.
"""
from __future__ import annotations

from duty.decorator import duty

__all__: list[str] = ["duty"]  # noqa: WPS410 (the only __variable__ we use)
