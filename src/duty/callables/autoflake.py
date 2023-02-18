"""Callable for [autoflake](https://github.com/PyCQA/autoflake)."""

from __future__ import annotations

from duty.callables import _io, lazy


@lazy("autoflake")
def run(
    *files: str,
    config: str | None = None,
    check: bool | None = None,
    check_diff: bool | None = None,
    imports: list[str] | None = None,
    remove_all_unused_imports: bool | None = None,
    recursive: bool | None = None,
    jobs: int | None = None,
    exclude: list[str] | None = None,
    expand_star_imports: bool | None = None,
    ignore_init_module_imports: bool | None = None,
    remove_duplicate_keys: bool | None = None,
    remove_unused_variables: bool | None = None,
    remove_rhs_for_unused_variables: bool | None = None,
    ignore_pass_statements: bool | None = None,
    ignore_pass_after_docstring: bool | None = None,
    quiet: bool | None = None,
    verbose: bool | None = None,
    stdin_display_name: str | None = None,
    in_place: bool | None = None,
    stdout: bool | None = None,
) -> int:
    r"""Run `autoflake`.

    Parameters:
        *files: Files to format.
        config: Explicitly set the config file instead of auto determining based on file location.
        check: Return error code if changes are needed.
        check_diff: Return error code if changes are needed, also display file diffs.
        imports: By default, only unused standard library imports are removed; specify a comma-separated list of additional modules/packages.
        remove_all_unused_imports: Remove all unused imports (not just those from the standard library).
        recursive: Drill down directories recursively.
        jobs: Number of parallel jobs; match CPU count if value is 0 (default: 0).
        exclude: Exclude file/directory names that match these comma-separated globs.
        expand_star_imports: Expand wildcard star imports with undefined names; this only triggers if there is only one star import in the file; this is skipped if there are any uses of `__all__` or `del` in the file.
        ignore_init_module_imports: Exclude `__init__.py` when removing unused imports.
        remove_duplicate_keys: Remove all duplicate keys in objects.
        remove_unused_variables: Remove unused variables.
        remove_rhs_for_unused_variables: Remove RHS of statements when removing unused variables (unsafe).
        ignore_pass_statements: Ignore all pass statements.
        ignore_pass_after_docstring: Ignore pass statements after a newline ending on `\"\"\"`.
        quiet: Suppress output if there are no issues.
        verbose: Print more verbose logs (you can repeat `-v` to make it more verbose).
        stdin_display_name: The name used when processing input from stdin.
        in_place: Make changes to files instead of printing diffs.
        stdout: Print changed text to stdout. defaults to true when formatting stdin, or to false otherwise.
    """
    from autoflake import _main as autoflake

    cli_args = list(files)

    if check:
        cli_args.append("--check")

    if check_diff:
        cli_args.append("--check-diff")

    if imports:
        cli_args.append("--imports")
        cli_args.append(",".join(imports))

    if remove_all_unused_imports:
        cli_args.append("--remove-all-unused-imports")

    if recursive:
        cli_args.append("--recursive")

    if jobs:
        cli_args.append("--jobs")
        cli_args.append(str(jobs))

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(",".join(exclude))

    if expand_star_imports:
        cli_args.append("--expand-star-imports")

    if ignore_init_module_imports:
        cli_args.append("--ignore-init-module-imports")

    if remove_duplicate_keys:
        cli_args.append("--remove-duplicate-keys")

    if remove_unused_variables:
        cli_args.append("--remove-unused-variables")

    if remove_rhs_for_unused_variables:
        cli_args.append("remove-rhs-for-unused-variables")

    if ignore_pass_statements:
        cli_args.append("--ignore-pass-statements")

    if ignore_pass_after_docstring:
        cli_args.append("--ignore-pass-after-docstring")

    if quiet:
        cli_args.append("--quiet")

    if verbose:
        cli_args.append("--verbose")

    if stdin_display_name:
        cli_args.append("--stdin-display-name")
        cli_args.append(stdin_display_name)

    if config:
        cli_args.append("--config")
        cli_args.append(config)

    if in_place:
        cli_args.append("--in-place")

    if stdout:
        cli_args.append("--stdout")

    return autoflake(
        cli_args,
        standard_out=_io._LazyStdout(),  # noqa: SLF001
        standard_error=_io._LazyStderr(),  # noqa: SLF001
    )
