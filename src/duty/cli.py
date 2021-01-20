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

"""Module that contains the command line application."""

import argparse
import inspect
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple

from failprint.cli import ArgParser, add_flags

from duty.collection import Collection, Duty
from duty.exceptions import DutyFailure


def get_parser() -> ArgParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = ArgParser(prog="duty")
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
    return parser


def split_args(args: List[str], names: List[str]) -> List[List[str]]:  # noqa: WPS231 (complex)
    """
    Split command line arguments into duty commands.

    Arguments:
        args: The CLI arguments.
        names: The known duty names.

    Raises:
        ValueError: When a duty name is missing before an argument,
            or when the duty name is unknown.

    Returns:
        The split commands.
    """
    arg_lists = []
    current_arg_list: List[str] = []

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


def parse_options(duty: Duty, args: List[str]) -> Tuple[argparse.Namespace, List[str]]:
    """
    Parse options for a duty.

    Arguments:
        duty: The duty to parse for.
        args: The CLI args passed for this duty.

    Returns:
        The parsed opts, and the remaining arguments.
    """
    parser = add_flags(ArgParser(prog=f"duty {duty.name}"), set_defaults=False)
    opts, remainder = parser.parse_known_args(args)
    opts = opts.__dict__.items()  # noqa: WPS609
    opts = {_: value for _, value in opts if value is not None}
    return opts, remainder


def to_bool(value: str) -> bool:
    """
    Convert a string to a boolean.

    Arguments:
        value: The string to convert.

    Returns:
        True or False.
    """
    return value.lower() not in {"0", "no", "n", "false"}


def arg_type(annotation: Any) -> Callable:
    """
    Return a type-caster for the given annotation.

    Arguments:
        annotation: A typing annotation.

    Returns:
        A callable.
    """
    if annotation is bool:
        return to_bool
    return annotation


def get_args_types(duty: Duty) -> Tuple[Any, Any, Dict[str, Any]]:
    """
    Get the type of each argument of the duty's function.

    Arguments:
        duty: The duty to get arguments types from.

    Returns:
        A tuple composed of:

        - the type for positional arguments,
        - the type for unknown keyword arguments,
        - a dict containing the type for each known argument
    """
    empty = inspect.Signature.empty
    signature = inspect.signature(duty.function)

    posargs_type: Callable = empty  # type: ignore
    kwargs_type: Callable = empty  # type: ignore
    args_type: Dict[str, Any] = {}

    for parameter in list(signature.parameters.values())[1:]:
        if parameter.kind is parameter.VAR_POSITIONAL:
            posargs_type = arg_type(parameter.annotation)
        elif parameter.kind is parameter.VAR_KEYWORD:
            kwargs_type = arg_type(parameter.annotation)
        elif parameter.annotation is not empty:
            args_type[parameter.name] = arg_type(parameter.annotation)

    return posargs_type, kwargs_type, args_type


def parse_args(duty: Duty, args: List[str]) -> Tuple:  # noqa: WPS231 (complex)
    """
    Parse the positional and keyword arguments of a duty.

    Arguments:
        duty: The duty to parse for.
        args: The list of arguments.

    Returns:
        The positional and keyword arguments.
    """
    posargs = []
    kwargs = {}
    posargs_type, kwargs_type, args_type = get_args_types(duty)
    empty = inspect.Signature.empty

    for arg in args:
        if "=" in arg:
            # We found a keyword argument.
            arg_name, arg_value = arg.split("=", 1)
            if arg_name in args_type:
                # The keyword argument is known,
                # we have a type for it: cast it.
                arg_value = args_type[arg_name](arg_value)
            elif kwargs_type is not empty:
                # The keyword argument is unkown.
                # If we have a global kwargs type,
                # use it to cast the argument value.
                arg_value = kwargs_type(arg_value)
            kwargs[arg_name] = arg_value
        else:
            # We found a positional argument.
            # If we have a global posargs type,
            # use it to cast the argument value.
            if posargs_type is not empty:
                arg = posargs_type(arg)
            posargs.append(arg)

    return posargs, kwargs


def parse_commands(arg_lists, collection) -> List[Tuple]:
    """
    Parse argument lists into ready-to-run duties.

    Arguments:
        arg_lists: Lists of arguments lists.
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
        duty.options.update(opts)
        commands.append((duty, *parse_args(duty, remainder)))
    return commands


def main(args: Optional[List[str]] = None) -> int:  # noqa: WPS212 (return statements)
    """
    Run the main program.

    This function is executed when you type `duty` or `python -m duty`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts, remainder = parser.parse_known_args(args=args)

    collection = Collection(opts.duties_file)
    collection.load()

    if opts.list:
        collection.show()
        return 0

    try:
        arg_lists = split_args(remainder, collection.names())
    except ValueError as error:
        print(error, file=sys.stderr)  # noqa: WPS421 (print)
        return 1

    if not arg_lists:
        print("> Please choose at least one duty", file=sys.stderr)  # noqa: WPS421 (print)
        return 1

    commands = parse_commands(arg_lists, collection)

    for duty, posargs, kwargs in commands:
        try:
            duty.run(*posargs, **kwargs)
        except DutyFailure as failure:
            return failure.code

    return 0
