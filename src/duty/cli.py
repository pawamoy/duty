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
import sys
from importlib import util as importlib_util
from typing import Dict, List, Optional, Tuple

from duty import logic

SelectionType = List[Tuple[logic.Duty, Dict[str, str]]]


def load_duties(path: str) -> Dict[str, logic.Duty]:
    """
    Load duties from a Python file.

    Arguments:
        path: The path to the Python file to load.

    Returns:
        The loaded duties.
    """
    logic.duties.clear()
    spec = importlib_util.spec_from_file_location("duty.loaded", path)
    duties = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(duties)  # type: ignore
    return logic.duties


def parse_selection(args: List[str], duties: Dict[str, logic.Duty]) -> SelectionType:
    """
    Parse the arguments given on the command line to return a selection of actual duties.

    Arguments:
        args: Arguments given on the command line.
        duties: The user registered duties.

    Raises:
        ValueError: When the arguments are incorrect.

    Returns:
        A selection of duties and their keyword arguments.
    """
    selection = []
    duty: logic.Duty = None  # type: ignore
    for arg in args:
        if "=" in arg:
            if not duty:
                raise ValueError(f"argument without a duty: {arg}")
            duty_args.update((arg.split("=", 1),))  # type: ignore  # this is correct
        else:
            if duty:  # noqa: WPS513 (cannot replace by elif)
                selection.append((duty, duty_args))
            duty_args: Dict[str, str] = {}
            duty = duties[arg]
    selection.append((duty, duty_args))
    return selection


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="duty")
    parser.add_argument(
        "-d",
        "--duties-file",
        nargs=1,
        default="duties.py",
        help="Python file where the duties are defined.",
    )
    parser.add_argument("DUTIES", metavar="DUTY", nargs="+")
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `duty` or `python -m duty`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)

    duties = load_duties(opts.duties_file)

    try:
        selection = parse_selection(opts.DUTIES, duties)
    except KeyError as error:
        print(f"Unknown duty: {error}", file=sys.stderr)  # noqa: WPS421 (print)
        return 1
    except ValueError as error:
        print(f"Incorrect arguments: {error}", file=sys.stderr)  # noqa: WPS421 (print)
        return 1

    for duty, duty_args in selection:
        try:
            duty.run(**duty_args)
        except logic.DutyFailure as failure:
            return failure.code

    return 0
