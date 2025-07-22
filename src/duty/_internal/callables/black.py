# YORE: Bump 2: Remove file.

from __future__ import annotations

from failprint import lazy


@lazy(name="black")
def run(
    *src: str,
    config: str | None = None,
    code: str | None = None,
    line_length: int | None = None,
    target_version: str | None = None,
    check: bool | None = None,
    diff: bool | None = None,
    color: bool | None = None,
    fast: bool | None = None,
    pyi: bool | None = None,
    ipynb: bool | None = None,
    python_cell_magics: str | None = None,
    skip_source_first_line: bool | None = None,
    skip_string_normalization: bool | None = None,
    skip_magic_trailing_comma: bool | None = None,
    experimental_string_processing: bool | None = None,
    preview: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    required_version: str | None = None,
    include: str | None = None,
    exclude: str | None = None,
    extend_exclude: str | None = None,
    force_exclude: str | None = None,
    stdin_filename: str | None = None,
    workers: int | None = None,
) -> None:
    r"""Run `black`.

    Parameters:
        src: Format the directories and file paths.
        config: Read configuration from this file path.
        code: Format the code passed in as a string.
        line_length: How many characters per line to allow [default: 120].
        target_version: Python versions that should be supported by Black's output.
            By default, Black will try to infer this from the project metadata in pyproject.toml.
            If this does not yield conclusive results, Black will use per-file auto-detection.
        check: Don't write the files back, just return the status. Return code 0 means nothing would change.
            Return code 1 means some files would be reformatted. Return code 123 means there was an internal error.
        diff: Don't write the files back, just output a diff for each file on stdout.
        color: Show colored diff. Only applies when `--diff` is given.
        fast: If --fast given, skip temporary sanity checks. [default: --safe]
        pyi: Format all input files like typing stubs regardless of file extension
            (useful when piping source on standard input).
        ipynb: Format all input files like Jupyter Notebooks regardless of file extension
            (useful when piping source on standard input).
        python_cell_magics: When processing Jupyter Notebooks, add the given magic to the list of known python-magics
            (capture, prun, pypy, python, python3, time, timeit). Useful for formatting cells with custom python magics.
        skip_source_first_line: Skip the first line of the source code.
        skip_string_normalization: Don't normalize string quotes or prefixes.
        skip_magic_trailing_comma: Don't use trailing commas as a reason to split lines.
        preview: Enable potentially disruptive style changes that may be added
            to Black's main functionality in the next major release.
        quiet: Don't emit non-error messages to stderr. Errors are still emitted; silence those with 2>/dev/null.
        verbose: Also emit messages to stderr about files that were not changed or were ignored due to exclusion patterns.
        required_version: Require a specific version of Black to be running (useful for unifying results
            across many environments e.g. with a pyproject.toml file).
            It can be either a major version number or an exact version.
        include: A regular expression that matches files and directories that should be included on recursive searches.
            An empty value means all files are included regardless of the name. Use forward slashes for directories
            on all platforms (Windows, too). Exclusions are calculated first, inclusions later [default: (\.pyi?|\.ipynb)$].
        exclude: A regular expression that matches files and directories that should be excluded on recursive searches.
            An empty value means no paths are excluded. Use forward slashes for directories on all platforms (Windows, too).
            Exclusions are calculated first, inclusions later [default: /(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|
            \.tox|\.venv|venv|\.svn|\.ipynb_checkpoints|_build|buck-out|build|dist|__pypackages__)/].
        extend_exclude: Like --exclude, but adds additional files and directories on top of the excluded ones
            (useful if you simply want to add to the default).
        force_exclude: Like --exclude, but files and directories matching this regex will be excluded
            even when they are passed explicitly as arguments.
        stdin_filename: The name of the file when passing it through stdin. Useful to make sure Black will respect
            --force-exclude option on some editors that rely on using stdin.
        workers: Number of parallel workers [default: number CPUs in the system].
    """
    from black import main as black  # noqa: PLC0415

    cli_args = list(src)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if code:
        cli_args.append("--code")
        cli_args.append(code)

    if line_length:
        cli_args.append("--line-length")
        cli_args.append(str(line_length))

    if target_version:
        cli_args.append("--target-version")
        cli_args.append(target_version)

    if check:
        cli_args.append("--check")

    if diff:
        cli_args.append("--diff")

    if color is True:
        cli_args.append("--color")
    elif color is False:
        cli_args.append("--no-color")

    if fast:
        cli_args.append("--fast")

    if pyi:
        cli_args.append("--pyi")

    if ipynb:
        cli_args.append("--ipynb")

    if python_cell_magics:
        cli_args.append("--python-cell-magics")
        cli_args.append(python_cell_magics)

    if skip_source_first_line:
        cli_args.append("--skip_source_first_line")

    if skip_string_normalization:
        cli_args.append("--skip_string_normalization")

    if skip_magic_trailing_comma:
        cli_args.append("--skip_magic_trailing_comma")

    if experimental_string_processing:
        cli_args.append("--experimental_string_processing")

    if preview:
        cli_args.append("--preview")

    if quiet:
        cli_args.append("--quiet")

    if verbose:
        cli_args.append("--verbose")

    if required_version:
        cli_args.append("--required-version")
        cli_args.append(required_version)

    if include:
        cli_args.append("--include")
        cli_args.append(include)

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(exclude)

    if extend_exclude:
        cli_args.append("--extend-exclude")
        cli_args.append(extend_exclude)

    if force_exclude:
        cli_args.append("--force-exclude")
        cli_args.append(force_exclude)

    if stdin_filename:
        cli_args.append("--stdin-filename")
        cli_args.append(stdin_filename)

    if workers:
        cli_args.append("--workers")
        cli_args.append(str(workers))

    return black(cli_args, prog_name="black")
