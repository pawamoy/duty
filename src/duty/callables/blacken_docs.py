"""Callable for [blacken-docs](https://github.com/adamchainz/blacken-docs)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Pattern, Sequence

from duty.callables import lazy


@lazy("blacken_docs")
def run(
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
) -> int:
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

    Returns:
        Success/failure.
    """
    import black
    from blacken_docs import format_file

    exts = ("md", "py") if exts is None else tuple(ext.lstrip(".") for ext in exts)
    if exclude:
        exclude = tuple(re.compile(regex, re.I) if isinstance(regex, str) else regex for regex in exclude)
    filepaths = set()
    for path in paths:
        path = Path(path)
        if path.is_file():
            filepaths.add(path.as_posix())
        else:
            for ext in exts:
                filepaths |= {filepath.as_posix() for filepath in path.rglob(f"*.{ext}")}

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
    retv = 0
    for filepath in sorted(filepaths):
        retv |= format_file(
            filepath,
            black_mode,
            skip_errors=skip_errors,
            rst_literal_blocks=rst_literal_blocks,
        )
    return retv
