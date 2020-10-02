"""
Duty package.

A simple task runner.
"""

from typing import List

from duty.logic import duty

__all__: List[str] = ["duty"]  # noqa: WPS410 (the only __variable__ we use)
