from __future__ import annotations

import os
import subprocess
from functools import cache

from duty._internal.tools._base import Tool


@cache
def _find_ty() -> str:
    from ty.__main__ import find_ty_bin  # noqa: PLC0415

    try:
        return find_ty_bin()
    except FileNotFoundError:
        paths = os.environ["PATH"]
        for path in paths.split(os.pathsep):
            ty = os.path.join(path, "ty")
            if os.path.exists(ty):
                return ty
    return "ty"


class ty(Tool):  # noqa: N801
    """Call [ty](https://github.com/astral-sh/ty)."""

    cli_name = "ty"
    """The name of the executable on PATH."""

    @classmethod
    def check(
        cls,
        *paths: str,
        add_ignore: bool | None = None,
        project: str | None = None,
        python: str | None = None,
        typeshed: str | None = None,
        extra_search_path: list[str] | None = None,
        python_version: str | None = None,
        python_platform: str | None = None,
        verbose: bool = False,
        quiet: bool = False,
        config: list[str] | None = None,
        config_file: str | None = None,
        output_format: str | None = None,
        error_on_warning: bool | None = None,
        exit_zero: bool | None = None,
        watch: bool | None = None,
        error: list[str] | None = None,
        warn: list[str] | None = None,
        ignore: list[str] | None = None,
        respect_ignore_files: bool | None = None,
        force_exclude: bool | None = None,
        exclude: list[str] | None = None,
        no_progress: bool | None = None,
        color: str | None = None,
    ) -> ty:
        """Run ty on the given files or directories.

        Parameters:
            paths: Files or directories to type check.
            add_ignore: Adds `ty: ignore` comments to suppress all rule diagnostics.
            project: Run the command within the given project directory.
            python: Path to your project's Python environment or interpreter.
            typeshed: Custom directory to use for stdlib typeshed stubs.
            extra_search_path: Additional path to use as a module-resolution source (can be passed multiple times).
            python_version: Python version to assume when resolving types (possible values: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14).
            python_platform: Target platform to assume when resolving types.
            verbose: Use verbose output (or `-vv` and `-vvv` for more verbose output).
            quiet: Use quiet output (or `-qq` for silent output).
            config: A TOML `<KEY> = <VALUE>` pair overriding a specific configuration option.
            config_file: The path to a `ty.toml` file to use for configuration.
            output_format: The format to use for printing diagnostic messages (possible values: full, concise, gitlab, github).
            error_on_warning: Use exit code 1 if there are any warning-level diagnostics.
            exit_zero: Always use exit code 0, even when there are error-level diagnostics.
            watch: Watch files for changes and recheck files related to the changed files.
            error: Treat the given rule as having severity 'error'. Can be specified multiple times.
            warn: Treat the given rule as having severity 'warn'. Can be specified multiple times.
            ignore: Disables the rule. Can be specified multiple times.
            respect_ignore_files: Respect file exclusions via `.gitignore` and other standard ignore files.
            force_exclude: Enforce exclusions, even for paths passed to ty directly on the command-line.
            exclude: Glob patterns for files to exclude from type checking.
            no_progress: Hide all progress outputs.
            color: Control when colored output is used (possible values: auto, always, never).
        """
        cli_args = ["check", *paths]

        if add_ignore:
            cli_args.append("--add-ignore")

        if project:
            cli_args.append("--project")
            cli_args.append(project)

        if python:
            cli_args.append("--python")
            cli_args.append(python)

        if typeshed:
            cli_args.append("--typeshed")
            cli_args.append(typeshed)

        if extra_search_path:
            for path in extra_search_path:
                cli_args.append("--extra-search-path")
                cli_args.append(path)

        if python_version:
            cli_args.append("--python-version")
            cli_args.append(python_version)

        if python_platform:
            cli_args.append("--python-platform")
            cli_args.append(python_platform)

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if config:
            for config_option in config:
                cli_args.append("--config")
                cli_args.append(config_option)

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if output_format:
            cli_args.append("--output-format")
            cli_args.append(output_format)

        if error_on_warning:
            cli_args.append("--error-on-warning")

        if exit_zero:
            cli_args.append("--exit-zero")

        if watch:
            cli_args.append("--watch")

        if error:
            for rule in error:
                cli_args.append("--error")
                cli_args.append(rule)

        if warn:
            for rule in warn:
                cli_args.append("--warn")
                cli_args.append(rule)

        if ignore:
            for rule in ignore:
                cli_args.append("--ignore")
                cli_args.append(rule)

        if respect_ignore_files:
            cli_args.append("--respect-ignore-files")

        if force_exclude:
            cli_args.append("--force-exclude")

        if exclude:
            for pattern in exclude:
                cli_args.append("--exclude")
                cli_args.append(pattern)

        if no_progress:
            cli_args.append("--no-progress")

        if color:
            cli_args.append("--color")
            cli_args.append(color)

        return cls(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        process = subprocess.run(  # noqa: S603
            [_find_ty(), *self.cli_args],
            capture_output=True,
            text=True,
            check=False,
        )
        print(process.stdout)  # noqa: T201
        return process.returncode
