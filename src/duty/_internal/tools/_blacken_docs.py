from __future__ import annotations

import re
from pathlib import Path
from re import Pattern
from typing import TYPE_CHECKING

from duty._internal.tools._base import Tool

if TYPE_CHECKING:
    from collections.abc import Sequence


class blacken_docs(Tool):  # noqa: N801
    """Call [blacken-docs](https://github.com/adamchainz/blacken-docs)."""

    cli_name = "blacken-docs"
    """The name of the executable on PATH."""

    def __init__(
        self,
        *paths: str | Path,
        exts: Sequence[str] | None = None,
        exclude: Sequence[str | Pattern] | None = None,
        skip_errors: bool = False,
        rst_literal_blocks: bool = False,
        line_length: int | None = None,
        string_normalization: bool = True,
        is_pyi: bool = False,
        is_ipynb: bool = False,
        skip_source_first_line: bool = False,
        magic_trailing_comma: bool = True,
        python_cell_magics: set[str] | None = None,
        preview: bool = False,
        check_only: bool = False,
    ) -> None:
        """Run `blacken-docs`.

        Parameters:
            *paths: Directories and files to format.
            exts: List of extensions to select files with.
            exclude: List of regular expressions to exclude files.
            skip_errors: Don't exit non-zero for errors from Black (normally syntax errors).
            rst_literal_blocks: Also format literal blocks in reStructuredText files (more below).
            line_length: How many characters per line to allow.
            string_normalization: Normalize string quotes or prefixes.
            is_pyi: Format all input files like typing stubs regardless of file extension.
            is_ipynb: Format all input files like Jupyter Notebooks regardless of file extension.
            skip_source_first_line: Skip the first line of the source code.
            magic_trailing_comma: Use trailing commas as a reason to split lines.
            python_cell_magics: When processing Jupyter Notebooks, add the given magic to the list
                of known python-magics (capture, prun, pypy, python, python3, time, timeit).
                Useful for formatting cells with custom python magics.
            preview: Enable potentially disruptive style changes that may be added
                to Black's main functionality in the next major release.
            check_only: Don't modify files but indicate when changes are necessary
                with a message and non-zero return code.

        Returns:
            Success/failure.
        """
        super().__init__(py_args=dict(locals()))

    @property
    def cli_command(self) -> str:
        """The equivalent CLI command."""
        raise ValueError("This command cannot be translated to a CLI command.")

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        import black  # noqa: PLC0415
        from blacken_docs import format_file  # noqa: PLC0415

        # Restore locals.
        exts = self.py_args["exts"]
        exclude = self.py_args["exclude"]
        paths = self.py_args["paths"]
        line_length = self.py_args["line_length"]
        string_normalization = self.py_args["string_normalization"]
        is_pyi = self.py_args["is_pyi"]
        is_ipynb = self.py_args["is_ipynb"]
        skip_source_first_line = self.py_args["skip_source_first_line"]
        magic_trailing_comma = self.py_args["magic_trailing_comma"]
        python_cell_magics = self.py_args["python_cell_magics"]
        preview = self.py_args["preview"]
        skip_errors = self.py_args["skip_errors"]
        rst_literal_blocks = self.py_args["rst_literal_blocks"]
        check_only = self.py_args["check_only"]

        # Build filepaths.
        exts = ("md", "py") if exts is None else tuple(ext.lstrip(".") for ext in exts)
        if exclude:
            exclude = tuple(re.compile(regex, re.I) if isinstance(regex, str) else regex for regex in exclude)
        filepaths = set()
        for path in paths:
            path = Path(path)  # noqa: PLW2901
            if path.is_file():
                filepaths.add(path.as_posix())
            else:
                for ext in exts:
                    filepaths |= {filepath.as_posix() for filepath in path.rglob(f"*.{ext}")}

        # Initiate black.
        black_mode = black.Mode(
            line_length=line_length or black.DEFAULT_LINE_LENGTH,
            string_normalization=string_normalization,
            is_pyi=is_pyi,
            is_ipynb=is_ipynb,
            skip_source_first_line=skip_source_first_line,
            magic_trailing_comma=magic_trailing_comma,
            python_cell_magics=python_cell_magics or set(),
            preview=preview,
        )

        # Run blacken-docs.
        retv = 0
        for filepath in sorted(filepaths):
            retv |= format_file(
                filepath,
                black_mode,
                skip_errors=skip_errors,
                rst_literal_blocks=rst_literal_blocks,
                check_only=check_only,
            )
        return retv
