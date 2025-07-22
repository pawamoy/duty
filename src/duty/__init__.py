"""duty package.

A simple task runner.
"""

from __future__ import annotations

from duty._internal.cli import get_parser, main
from duty._internal.decorator import duty
from duty._internal.tools import Tool, lazy

__all__: list[str] = [
    "Tool",
    "duty",
    "get_parser",
    "lazy",
    "main",
]
