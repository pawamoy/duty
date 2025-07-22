# YORE: Bump 2: Remove file.

from __future__ import annotations

import sys
from typing import Literal

from failprint import lazy


@lazy(name="flake8")
def run(
    *paths: str,
    config: str | None = None,
    verbose: bool | None = None,
    output_file: str | None = None,
    append_config: str | None = None,
    isolated: bool | None = None,
    enable_extensions: list[str] | None = None,
    require_plugins: list[str] | None = None,
    quiet: bool | None = None,
    color: Literal["auto", "always", "never"] | None = None,
    count: bool | None = None,
    exclude: list[str] | None = None,
    extend_exclude: list[str] | None = None,
    filename: list[str] | None = None,
    stdin_display_name: str | None = None,
    error_format: str | None = None,
    hang_closing: bool | None = None,
    ignore: list[str] | None = None,
    extend_ignore: list[str] | None = None,
    per_file_ignores: dict[str, list[str]] | None = None,
    max_line_length: int | None = None,
    max_doc_length: int | None = None,
    indent_size: int | None = None,
    select: list[str] | None = None,
    extend_select: list[str] | None = None,
    disable_noqa: bool | None = None,
    show_source: bool | None = None,
    no_show_source: bool | None = None,
    statistics: bool | None = None,
    exit_zero: bool | None = None,
    jobs: int | None = None,
    tee: bool | None = None,
    benchmark: bool | None = None,
    bug_report: bool | None = None,
) -> int:
    """Run `flake8`.

    Parameters:
        *paths: Paths to check.
        config: Path to the config file that will be the authoritative config source.
            This will cause Flake8 to ignore all other configuration files.
        verbose: Print more information about what is happening in flake8.
            This option is repeatable and will increase verbosity each time it is repeated.
        output_file: Redirect report to a file.
        append_config: Provide extra config files to parse in addition to the files found by Flake8 by default.
            These files are the last ones read and so they take the highest precedence when multiple files provide the same option.
        isolated: Ignore all configuration files.
        enable_extensions: Enable plugins and extensions that are otherwise disabled by default.
        require_plugins: Require specific plugins to be installed before running.
        quiet: Report only file names, or nothing. This option is repeatable.
        color: Whether to use color in output. Defaults to `auto`.
        count: Print total number of errors to standard output and set the exit code to 1 if total is not empty.
        exclude: Comma-separated list of files or directories to exclude (default: ['.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox', '.nox', '.eggs', '*.egg']).
        extend_exclude: Comma-separated list of files or directories to add to the list of excluded ones.
        filename: Only check for filenames matching the patterns in this comma-separated list (default: ['*.py']).
        stdin_display_name: The name used when reporting errors from code passed via stdin. This is useful for editors piping the file contents to flake8 (default: stdin).
        error_format: Format errors according to the chosen formatter.
        hang_closing: Hang closing bracket instead of matching indentation of opening bracket's line.
        ignore: Comma-separated list of error codes to ignore (or skip). For example, ``--ignore=E4,E51,W234`` (default: E121,E123,E126,E226,E24,E704,W503,W504).
        extend_ignore: Comma-separated list of error codes to add to the list of ignored ones. For example, ``--extend-ignore=E4,E51,W234``.
        per_file_ignores: A pairing of filenames and violation codes that defines which violations to ignore in a particular file. The filenames can be specified in a manner similar to the ``--exclude`` option and the violations work similarly to the ``--ignore`` and ``--select`` options.
        max_line_length: Maximum allowed line length for the entirety of this run (default: 79).
        max_doc_length: Maximum allowed doc line length for the entirety of this run (default: None).
        indent_size: Number of spaces used for indentation (default: 4).
        select: Comma-separated list of error codes to enable. For example, ``--select=E4,E51,W234`` (default: E,F,W,C90).
        extend_select: Comma-separated list of error codes to add to the list of selected ones. For example, ``--extend-select=E4,E51,W234``.
        disable_noqa: Disable the effect of "# noqa". This will report errors on lines with "# noqa" at the end.
        show_source: Show the source generate each error or warning.
        no_show_source: Negate --show-source.
        statistics: Count errors.
        exit_zero: Exit with status code "0" even if there are errors.
        jobs: Number of subprocesses to use to run checks in parallel. This is ignored on Windows. The default, "auto", will auto-detect the number of processors available to use (default: auto).
        tee: Write to stdout and output-file.
        benchmark: Print benchmark information about this run of Flake8.
        bug_report: Print information necessary when preparing a bug report.

    Returns:
        Success/failure.
    """
    from flake8.main import main as flake8  # noqa: PLC0415

    cli_args = list(paths)

    if verbose:
        cli_args.append("--verbose")

    if output_file:
        cli_args.append("--output-file")
        cli_args.append(output_file)

    if append_config:
        cli_args.append("--append-config")
        cli_args.append(append_config)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if isolated:
        cli_args.append("--isolated")

    if enable_extensions:
        cli_args.append("--enable-extensions")
        cli_args.append(",".join(enable_extensions))

    if require_plugins:
        cli_args.append("--require-plugins")
        cli_args.append(",".join(require_plugins))

    if quiet:
        cli_args.append("--quiet")

    if color:
        cli_args.append("--color")
        cli_args.append(color)

    if count:
        cli_args.append("--count")

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(",".join(extend_exclude))

    if filename:
        cli_args.append("--filename")
        cli_args.append(",".join(filename))

    if stdin_display_name:
        cli_args.append("--stdin-display-name")
        cli_args.append(stdin_display_name)

    if error_format:
        cli_args.append("--format")
        cli_args.append(error_format)

    if hang_closing:
        cli_args.append("--hang-closing")

    if ignore:
        cli_args.append("--ignore")
        cli_args.append(",".join(ignore))

    if extend_ignore:
        cli_args.append("--extend-ignore")
        cli_args.append(",".join(extend_ignore))

    if per_file_ignores:
        cli_args.append("--per-file-ignores")
        cli_args.append(
            " ".join(f"{path}:{','.join(codes)}" for path, codes in per_file_ignores.items()),
        )

    if max_line_length:
        cli_args.append("--max-line-length")
        cli_args.append(str(max_line_length))

    if max_doc_length:
        cli_args.append("--max-doc-length")
        cli_args.append(str(max_doc_length))

    if indent_size:
        cli_args.append("--indent-size")
        cli_args.append(str(indent_size))

    if select:
        cli_args.append("--select")
        cli_args.append(",".join(select))

    if extend_select:
        cli_args.append("--extend-select")
        cli_args.append(",".join(extend_select))

    if disable_noqa:
        cli_args.append("--disable-noqa")

    if show_source:
        cli_args.append("--show-source")

    if no_show_source:
        cli_args.append("--no-show-source")

    if statistics:
        cli_args.append("--statistics")

    if exit_zero:
        cli_args.append("--exit-zero")

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if tee:
        cli_args.append("--tee")

    if benchmark:
        cli_args.append("--benchmark")

    if bug_report:
        cli_args.append("--bug-report")

    old_sys_argv = sys.argv
    sys.argv = ["flake*", *cli_args]
    try:
        return flake8()
    finally:
        sys.argv = old_sys_argv
