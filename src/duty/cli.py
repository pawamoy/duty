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
import importlib.util
from typing import Dict, List, Optional

from duty import logic


def load_duties(path: str) -> Dict[str, logic.Duty]:
    """
    Load duties from a Python file.

    Arguments:
        path: The path to the Python file to load.

    Returns:
        The loaded duties.
    """
    logic.duties.clear()
    spec = importlib.util.spec_from_file_location("duty.loaded", path)
    duties = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(duties)  # type: ignore
    return logic.duties


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="duty")
    parser.add_argument(
        "-d", "--duties-file", nargs=1, default="duties.py", help="Python file where the duties are defined."
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

    selection = []
    duty_name: str = ""
    for arg in opts.DUTIES:
        if "=" in arg:
            duty_args.update(dict([arg.split("=", 1)]))
        else:
            if duty_name:
                selection.append((duty_name, duty_args))
            duty_args: Dict[str, str] = {}
            duty_name = arg
    selection.append((duty_name, duty_args))

    for duty_name, duty_args in selection:
        try:
            duties[duty_name].run(**duty_args)
        except logic.DutyFailure as failure:
            return failure.code

    return 0
