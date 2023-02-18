"""Module that contains the command line application."""

# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m duty` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `duty.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `duty.__main__` in `sys.modules`.

from __future__ import annotations

import argparse
import inspect
import sys
import textwrap
from typing import Any

from failprint.cli import ArgParser, add_flags

from duty.collection import Collection, Duty
from duty.exceptions import DutyFailure
from duty.validation import validate

empty = inspect.Signature.empty


def get_parser() -> ArgParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    usage = "duty [GLOBAL_OPTS...] [DUTY [DUTY_OPTS...] [DUTY_PARAMS...]...]"
    description = "A simple task runner."
    parser = ArgParser(add_help=False, usage=usage, description=description)

    parser.add_argument(
        "-d",
        "--duties-file",
        default="duties.py",
        help="Python file where the duties are defined.",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list",
        help="List the available duties.",
    )
    parser.add_argument(
        "-h",
        "--help",
        dest="help",
        nargs="*",
        metavar="DUTY",
        help="Show this help message and exit. Pass duties names to print their help.",
    )

    add_flags(parser, set_defaults=False)
    parser.add_argument("remainder", nargs=argparse.REMAINDER)

    parser._optionals.title = "Global options"  # noqa: SLF001

    return parser


def split_args(args: list[str], names: list[str]) -> list[list[str]]:
    """Split command line arguments into duty commands.

    Parameters:
        args: The CLI arguments.
        names: The known duty names.

    Raises:
        ValueError: When a duty name is missing before an argument,
            or when the duty name is unknown.

    Returns:
        The split commands.
    """
    arg_lists = []
    current_arg_list: list[str] = []

    for arg in args:
        if arg in names:
            # We found a duty name.
            if current_arg_list:
                # Append the previous arg list to the result and reset it.
                arg_lists.append(current_arg_list)
                current_arg_list = []
            current_arg_list.append(arg)
        elif current_arg_list:
            # We found an argument.
            current_arg_list.append(arg)
        else:
            # We found an argument but no duty name.
            raise ValueError(f"> Missing duty name before argument '{arg}', or unknown duty name")

    # Don't forget the last arg list.
    if current_arg_list:
        arg_lists.append(current_arg_list)

    return arg_lists


def get_duty_parser(duty: Duty) -> ArgParser:
    """Get a duty-specific options parser.

    Parameters:
        duty: The duty to parse for.

    Returns:
        A duty-specific parser.
    """
    parser = ArgParser(
        prog=f"duty {duty.name}",
        add_help=False,
        description=duty.description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_flags(parser, set_defaults=False)
    return parser


def specified_options(opts: argparse.Namespace, exclude: set[str] | None = None) -> dict:
    """Cast an argparse Namespace into a dictionary of options.

    Remove all options that were not specified (equal to None).

    Parameters:
        opts: The namespace to cast.
        exclude: Names of options to exclude from the result.

    Returns:
        A dictionary of specified-only options.
    """
    exclude = exclude or set()
    options = opts.__dict__.items()
    return {opt: value for opt, value in options if value is not None and opt not in exclude}


def parse_options(duty: Duty, args: list[str]) -> tuple[dict, list[str]]:
    """Parse options for a duty.

    Parameters:
        duty: The duty to parse for.
        args: The CLI args passed for this duty.

    Returns:
        The parsed opts, and the remaining arguments.
    """
    parser = get_duty_parser(duty)
    opts, remainder = parser.parse_known_args(args)
    return specified_options(opts), remainder


def parse_args(duty: Duty, args: list[str]) -> tuple:
    """Parse the positional and keyword arguments of a duty.

    Parameters:
        duty: The duty to parse for.
        args: The list of arguments.

    Returns:
        The positional and keyword arguments.
    """
    posargs = []
    kwargs = {}

    for arg in args:
        if "=" in arg:
            # we found a keyword argument
            arg_name, arg_value = arg.split("=", 1)
            kwargs[arg_name] = arg_value
        else:
            # we found a positional argument
            posargs.append(arg)

    return validate(duty.function, *posargs, **kwargs)


def parse_commands(arg_lists: list[list[str]], global_opts: dict[str, Any], collection: Collection) -> list[tuple]:
    """Parse argument lists into ready-to-run duties.

    Parameters:
        arg_lists: Lists of arguments lists.
        global_opts: The global options.
        collection: The duties collection.

    Returns:
        A list of tuples composed of:

            - a duty
            - its positional arguments
            - its keyword arguments
    """
    commands = []
    for arg_list in arg_lists:
        duty = collection.get(arg_list[0])
        opts, remainder = parse_options(duty, arg_list[1:])
        duty.options_override = {**global_opts, **opts}
        commands.append((duty, *parse_args(duty, remainder)))
    return commands


def print_help(parser: ArgParser, opts: argparse.Namespace, collection: Collection) -> None:
    """Print general help or duties help.

    Parameters:
        parser: The main parser.
        opts: The main parsed options.
        collection: A collection of duties.
    """
    if opts.help:
        for duty_name in opts.help:
            try:
                duty = collection.get(duty_name)
            except KeyError:
                print(f"> Unknown duty '{duty_name}'")
            else:
                print(get_duty_parser(duty).format_help())
    else:
        print(parser.format_help())
        print("Available duties:")
        print(textwrap.indent(collection.format_help(), prefix="  "))


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `duty` or `python -m duty`.

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)
    remainder = opts.remainder

    collection = Collection(opts.duties_file)
    collection.load()

    if opts.help is not None:
        print_help(parser, opts, collection)
        return 0

    if opts.list:
        print(textwrap.indent(collection.format_help(), prefix="  "))
        return 0

    try:
        arg_lists = split_args(remainder, collection.names())
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if not arg_lists:
        print("> Please choose at least one duty", file=sys.stderr)
        return 1

    global_opts = specified_options(opts, exclude={"duties_file", "list", "help", "remainder"})
    try:
        commands = parse_commands(arg_lists, global_opts, collection)
    except TypeError as error:
        print(f"> {error}", file=sys.stderr)
        return 1

    for duty, posargs, kwargs in commands:
        try:
            duty.run(*posargs, **kwargs)
        except DutyFailure as failure:
            return failure.code

    return 0
