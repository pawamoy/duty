from __future__ import annotations

import os
import subprocess
import sys
from functools import cache

from duty._internal.tools._base import Tool


@cache
def _find_ruff() -> str:
    from ruff.__main__ import find_ruff_bin  # noqa: PLC0415

    try:
        return find_ruff_bin()
    except FileNotFoundError:
        paths = os.environ["PATH"]
        for path in paths.split(os.pathsep):
            ruff = os.path.join(path, "ruff")
            if os.path.exists(ruff):
                return ruff
        py_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
        pypackages_bin = os.path.join("__pypackages__", py_version, "bin")
        ruff = os.path.join(pypackages_bin, "ruff")
        if os.path.exists(ruff):
            return ruff
    return "ruff"


class ruff(Tool):  # noqa: N801
    """Call [Ruff](https://github.com/astral-sh/ruff)."""

    cli_name = "ruff"
    """The name of the executable on PATH."""

    @classmethod
    def check(
        cls,
        *files: str,
        config: str | None = None,
        fix: bool | None = None,
        show_source: bool | None = None,
        show_fixes: bool | None = None,
        diff: bool | None = None,
        watch: bool | None = None,
        fix_only: bool | None = None,
        output_format: str | None = None,
        statistics: bool | None = None,
        add_noqa: bool | None = None,
        show_files: bool | None = None,
        show_settings: bool | None = None,
        select: list[str] | None = None,
        ignore: list[str] | None = None,
        extend_select: list[str] | None = None,
        per_file_ignores: dict[str, list[str]] | None = None,
        fixable: list[str] | None = None,
        unfixable: list[str] | None = None,
        exclude: list[str] | None = None,
        extend_exclude: list[str] | None = None,
        respect_gitignore: bool | None = None,
        force_exclude: bool | None = None,
        no_cache: bool | None = None,
        isolated: bool | None = None,
        cache_dir: str | None = None,
        stdin_filename: str | None = None,
        exit_zero: bool | None = None,
        exit_non_zero_on_fix: bool | None = None,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """Run Ruff on the given files or directories.

        Parameters:
            fix: Attempt to automatically fix lint violations.
            config: Path to the `pyproject.toml` or `ruff.toml` file to use for configuration.
            show_source: Show violations with source code.
            show_fixes: Show an enumeration of all autofixed lint violations.
            diff: Avoid writing any fixed files back; instead, output a diff for each changed file to stdout.
            watch: Run in watch mode by re-running whenever files change.
            fix_only: Fix any fixable lint violations, but don't report on leftover violations. Implies `--fix`.
            output_format: Output serialization format for violations (env: RUFF_FORMAT=) (possible values: text, json, junit, grouped, github, gitlab, pylint).
            statistics: Show counts for every rule with at least one violation.
            add_noqa: Enable automatic additions of `noqa` directives to failing lines.
            show_files: See the files Ruff will be run against with the current settings.
            show_settings: See the settings Ruff will use to lint a given Python file.
            select: Comma-separated list of rule codes to enable (or ALL, to enable all rules).
            ignore: Comma-separated list of rule codes to disable.
            extend_select: Like --select, but adds additional rule codes on top of the selected ones.
            per_file_ignores: List of mappings from file pattern to code to exclude.
            fixable: List of rule codes to treat as eligible for autofix. Only applicable when autofix itself is enabled (e.g., via `--fix`).
            unfixable: List of rule codes to treat as ineligible for autofix. Only applicable when autofix itself is enabled (e.g., via `--fix`).
            exclude: List of paths, used to omit files and/or directories from analysis.
            extend_exclude: Like --exclude, but adds additional files and directories on top of those already excluded.
            respect_gitignore: Respect file exclusions via `.gitignore` and other standard ignore files.
            force_exclude: Enforce exclusions, even for paths passed to Ruff directly on the command-line.
            no_cache: Disable cache reads.
            isolated: Ignore all configuration files.
            cache_dir: Path to the cache directory (env: RUFF_CACHE_DIR=).
            stdin_filename: The name of the file when passing it through stdin.
            exit_zero: Exit with status code "0", even upon detecting lint violations.
            exit_non_zero_on_fix: Exit with a non-zero status code if any files were modified via autofix, even if no lint violations remain.
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["check", *files]

        if fix:
            cli_args.append("--fix")

        if show_source:
            cli_args.append("--show-source")

        if show_fixes:
            cli_args.append("--show-fixes")

        if diff:
            cli_args.append("--diff")

        if watch:
            cli_args.append("--watch")

        if fix_only:
            cli_args.append("--fix-only")

        if output_format:
            cli_args.append("--format")
            cli_args.append(output_format)

        if config:
            cli_args.append("--config")
            cli_args.append(config)

        if statistics:
            cli_args.append("--statistics")

        if add_noqa:
            cli_args.append("--add-noqa")

        if show_files:
            cli_args.append("--show-files")

        if show_settings:
            cli_args.append("--show-settings")

        if select:
            cli_args.append("--select")
            cli_args.append(",".join(select))

        if ignore:
            cli_args.append("--ignore")
            cli_args.append(",".join(ignore))

        if extend_select:
            cli_args.append("--extend-select")
            cli_args.append(",".join(extend_select))

        if per_file_ignores:
            cli_args.append("--per-file-ignores")
            cli_args.append(
                " ".join(f"{path}:{','.join(codes)}" for path, codes in per_file_ignores.items()),
            )

        if fixable:
            cli_args.append("--fixable")
            cli_args.append(",".join(fixable))

        if unfixable:
            cli_args.append("--unfixable")
            cli_args.append(",".join(unfixable))

        if exclude:
            cli_args.append("--exclude")
            cli_args.append(",".join(exclude))

        if extend_exclude:
            cli_args.append("--extend-exclude")
            cli_args.append(",".join(extend_exclude))

        if respect_gitignore:
            cli_args.append("--respect-gitignore")

        if force_exclude:
            cli_args.append("--force-exclude")

        if no_cache:
            cli_args.append("--no-cache")

        if isolated:
            cli_args.append("--isolated")

        if cache_dir:
            cli_args.append("--cache-dir")
            cli_args.append(cache_dir)

        if stdin_filename:
            cli_args.append("--stdin-filename")
            cli_args.append(stdin_filename)

        if exit_zero:
            cli_args.append("--exit-zero")

        if exit_non_zero_on_fix:
            cli_args.append("--exit-non-zero-on-fix")

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    @classmethod
    def format(
        cls,
        *files: str,
        config: str | None = None,
        check: bool | None = None,
        diff: bool | None = None,
        target_version: str | None = None,
        preview: bool | None = None,
        exclude: list[str] | None = None,
        extend_exclude: list[str] | None = None,
        respect_gitignore: bool | None = None,
        force_exclude: bool | None = None,
        no_cache: bool | None = None,
        isolated: bool | None = None,
        cache_dir: str | None = None,
        stdin_filename: str | None = None,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """Run Ruff formatter on the given files or directories.

        Parameters:
            check: Avoid writing any formatted files back; instead, exit with a non-zero status code if any files would have been modified, and zero otherwise
            config: Path to the `pyproject.toml` or `ruff.toml` file to use for configuration
            diff: Avoid writing any fixed files back; instead, output a diff for each changed file to stdout
            target_version: The minimum Python version that should be supported [possible values: py37, py38, py39, py310, py311, py312]
            preview: Enable preview mode; enables unstable formatting
            exclude: List of paths, used to omit files and/or directories from analysis
            extend_exclude: Like --exclude, but adds additional files and directories on top of those already excluded
            respect_gitignore: Respect file exclusions via `.gitignore` and other standard ignore files
            force_exclude: Enforce exclusions, even for paths passed to Ruff directly on the command-line
            no_cache: Disable cache reads
            isolated: Ignore all configuration files
            cache_dir: Path to the cache directory [env: RUFF_CACHE_DIR=]
            stdin_filename: The name of the file when passing it through stdin
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["format", *files]

        if check:
            cli_args.append("--check")

        if diff:
            cli_args.append("--diff")

        if config:
            cli_args.append("--config")
            cli_args.append(config)

        if target_version:
            cli_args.append("--target-version")
            cli_args.append(target_version)

        if preview:
            cli_args.append("--preview")

        if exclude:
            cli_args.append("--exclude")
            cli_args.append(",".join(exclude))

        if extend_exclude:
            cli_args.append("--extend-exclude")
            cli_args.append(",".join(extend_exclude))

        if respect_gitignore:
            cli_args.append("--respect-gitignore")

        if force_exclude:
            cli_args.append("--force-exclude")

        if no_cache:
            cli_args.append("--no-cache")

        if isolated:
            cli_args.append("--isolated")

        if cache_dir:
            cli_args.append("--cache-dir")
            cli_args.append(cache_dir)

        if stdin_filename:
            cli_args.append("--stdin-filename")
            cli_args.append(stdin_filename)

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    @classmethod
    def rule(
        cls,
        rule: str,
        *,
        output_format: str | None = None,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """Explain a rule.

        Parameters:
            rule: A rule code, or `--all`.
            output_format: Output format (default: pretty, possible values: text, json, pretty).
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["rule", rule]

        if output_format:
            cli_args.append("--format")
            cli_args.append(output_format)

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    @classmethod
    def config(
        cls,
        *,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """List or describe the available configuration options.

        Parameters:
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["config"]

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    @classmethod
    def linter(
        cls,
        *,
        output_format: str | None = None,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """List all supported upstream linters.

        Parameters:
            output_format: Output format (default: pretty) (possible values: text, json, pretty).
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["linter"]

        if output_format:
            cli_args.append("--format")
            cli_args.append(output_format)

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    @classmethod
    def clean(
        cls,
        *,
        verbose: bool = False,
        quiet: bool = False,
        silent: bool = False,
    ) -> ruff:
        """Clear any caches in the current directory and any subdirectories.

        Parameters:
            verbose: Enable verbose logging.
            quiet: Print lint violations, but nothing else.
            silent: Disable all logging (but still exit with status code "1" upon detecting lint violations).
        """
        cli_args = ["clean"]

        if verbose:
            cli_args.append("--verbose")

        if quiet:
            cli_args.append("--quiet")

        if silent:
            cli_args.append("--silent")

        return cls(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        process = subprocess.run(  # noqa: S603
            [_find_ruff(), *self.cli_args],
            capture_output=True,
            text=True,
            check=False,
        )
        print(process.stdout)  # noqa: T201
        return process.returncode
