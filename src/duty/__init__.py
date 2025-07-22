"""duty package.

A simple task runner.
"""

from __future__ import annotations

from failprint import lazy

from duty._internal.cli import (
    empty,
    get_duty_parser,
    get_parser,
    main,
    parse_args,
    parse_commands,
    parse_options,
    print_help,
    specified_options,
    split_args,
)
from duty._internal.collection import Collection, Duty, DutyListType, default_duties_file
from duty._internal.context import CmdType, Context
from duty._internal.decorator import create_duty, duty
from duty._internal.exceptions import DutyFailure
from duty._internal.tools._base import LazyStderr, LazyStdout, Tool
from duty._internal.validation import ParamsCaster, cast_arg, to_bool, validate

__all__: list[str] = [
    "CmdType",
    "Collection",
    "Context",
    "Duty",
    "DutyFailure",
    "DutyListType",
    "LazyStderr",
    "LazyStdout",
    "ParamsCaster",
    "Tool",
    "cast_arg",
    "create_duty",
    "default_duties_file",
    "duty",
    "empty",
    "get_duty_parser",
    "get_parser",
    "lazy",
    "main",
    "parse_args",
    "parse_commands",
    "parse_options",
    "print_help",
    "specified_options",
    "split_args",
    "to_bool",
    "validate",
]
