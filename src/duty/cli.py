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
from typing import List, Optional


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    return argparse.ArgumentParser(prog="duty")


def main(args: Optional[List[str]] = None) -> int:
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
    except TypeError as error:  # noqa: WPS440 (variable overlap)
        print(f"> {error}", file=sys.stderr)
        return 1

    for duty, posargs, kwargs in commands:
        try:
            duty.run(*posargs, **kwargs)
        except DutyFailure as failure:
            return failure.code

    return 0
