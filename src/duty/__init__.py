"""duty package.

A simple task runner.
"""

from __future__ import annotations

from duty._internal.cli import get_parser, main
from duty.decorator import duty

__all__: list[str] = ["duty", "get_parser", "main"]
