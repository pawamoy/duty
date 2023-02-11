from __future__ import annotations

import re
from pathlib import Path
from typing import Pattern, Sequence

import black
from blacken_docs import format_file


def run(
    *paths: Path,
    exts: Sequence[str] | None = None,
    exclude: Sequence[str | Pattern] | None = None,
    blacken_docs_skip_errors: bool = False,
    blacken_docs_rst_literal_blocks: bool = False,
    black_line_length: int = black.DEFAULT_LINE_LENGTH,
    black_string_normalization: bool = True,
    black_is_pyi: bool = False,
    black_is_ipynb: bool = False,
    black_skip_source_first_line: bool = False,
    black_magic_trailing_comma: bool = True,
    black_experimental_string_processing: bool = False,
    black_python_cell_magics: set[str] | None = None,
    black_preview: bool = False,
) -> int:
    if exts is None:
        exts = ("md", "py")
    else:
        exts = tuple(ext.lstrip(".") for ext in exts)
    if exclude:
        exclude = tuple(re.compile(regex, re.I) if isinstance(regex, str) else regex for regex in exclude)
    filepaths = set()
    for path in paths:
        if path.is_file():
            filepaths.add(path.as_posix())
        else:
            for ext in exts:
                filepaths |= {filepath.as_posix() for filepath in path.rglob(f"*.{ext}")}

    black_mode = black.Mode(
        line_length=black_line_length,
        string_normalization=black_string_normalization,
        is_pyi=black_is_pyi,
        is_ipynb=black_is_ipynb,
        skip_source_first_line=black_skip_source_first_line,
        magic_trailing_comma=black_magic_trailing_comma,
        experimental_string_processing=black_experimental_string_processing,
        python_cell_magics=black_python_cell_magics or set(),
        preview=black_preview,
    )
    retv = 0
    for filepath in sorted(filepaths):
        retv |= format_file(
            filepath,
            black_mode,
            skip_errors=blacken_docs_skip_errors,
            rst_literal_blocks=blacken_docs_rst_literal_blocks,
        )
    return retv
