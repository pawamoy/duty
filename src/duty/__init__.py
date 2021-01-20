"""
Duty package.

A simple task runner.
"""

from typing import List

from duty.decorator import duty

__all__: List[str] = ["duty"]  # noqa: WPS410 (the only __variable__ we use)
