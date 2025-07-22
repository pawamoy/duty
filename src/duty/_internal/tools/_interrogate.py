from __future__ import annotations

from typing import Literal

from duty._internal.tools._base import Tool

_BADGE_STYLE = Literal["flat", "flat-square", "flat-square-modified", "for-the-badge", "plastic", "social"]


class interrogate(Tool):  # noqa: N801
    """Call [Interrogate](https://github.com/econchick/interrogate)."""

    cli_name = "interrogate"
    """The name of the executable on PATH."""

    def __init__(
        self,
        *src: str,
        verbose: int | None = None,
        quiet: bool | None = None,
        fail_under: float | None = None,
        exclude: str | None = None,
        ignore_init_method: bool | None = None,
        ignore_init_module: bool | None = None,
        ignore_magic: bool | None = None,
        ignore_module: bool | None = None,
        ignore_nested_functions: bool | None = None,
        ignore_nested_classes: bool | None = None,
        ignore_private: bool | None = None,
        ignore_property_decorators: bool | None = None,
        ignore_setters: bool | None = None,
        ignore_semiprivate: bool | None = None,
        ignore_regex: str | None = None,
        whitelist_regex: str | None = None,
        output: str | None = None,
        config: str | None = None,
        color: bool | None = None,
        omit_covered_files: bool | None = None,
        generate_badge: str | None = None,
        badge_format: Literal["png", "svg"] | None = None,
        badge_style: _BADGE_STYLE | None = None,
    ) -> None:
        """Run `interrogate`.

        Args:
            src: Format the directories and file paths.
            verbose: Level of verbosity.
            quiet: Do not print output.
            fail_under: Fail when coverage % is less than a given amount.
            exclude: Exclude PATHs of files and/or directories.
            ignore_init_method: Ignore `__init__` method of classes.
            ignore_init_module: Ignore `__init__.py` modules.
            ignore_magic: Ignore all magic methods of classes.
            ignore_module: Ignore module-level docstrings.
            ignore_nested_functions: Ignore nested functions and methods.
            ignore_nested_classes: Ignore nested classes.
            ignore_private: Ignore private classes, methods, and functions starting with two underscores.
            ignore_property_decorators: Ignore methods with property setter/getter decorators.
            ignore_setters: Ignore methods with property setter decorators.
            ignore_semiprivate: Ignore semiprivate classes, methods, and functions starting with a single underscore.
            ignore_regex: Regex identifying class, method, and function names to ignore.
            whitelist_regex: Regex identifying class, method, and function names to include.
            output: Write output to a given FILE.
            config: Read configuration from pyproject.toml or setup.cfg.
            color: Toggle color output on/off when printing to stdout.
            omit_covered_files: Omit reporting files that have 100% documentation coverage.
            generate_badge: Generate a shields.io status badge (an SVG image) in at a given file or directory.
            badge_format: File format for the generated badge.
            badge_style: Desired style of shields.io badge.
        """
        cli_args = list(src)

        if verbose:
            cli_args.append("--verbose")
            cli_args.append(str(verbose))

        if quiet:
            cli_args.append("--quiet")

        if fail_under:
            cli_args.append("--fail-under")
            cli_args.append(str(fail_under))

        if exclude:
            cli_args.append("--exclude")
            cli_args.append(exclude)

        if ignore_init_method:
            cli_args.append("--ignore-init-method")

        if ignore_init_module:
            cli_args.append("--ignore-init-module")

        if ignore_magic:
            cli_args.append("--ignore-magic")

        if ignore_module:
            cli_args.append("--ignore-module")

        if ignore_nested_functions:
            cli_args.append("--ignore-nested-functions")

        if ignore_nested_classes:
            cli_args.append("--ignore-nested-classes")

        if ignore_private:
            cli_args.append("--ignore-private")

        if ignore_property_decorators:
            cli_args.append("--ignore-property-decorators")

        if ignore_setters:
            cli_args.append("--ignore-setters")

        if ignore_semiprivate:
            cli_args.append("--ignore-semiprivate")

        if ignore_regex:
            cli_args.append("--ignore-regex")
            cli_args.append(ignore_regex)

        if whitelist_regex:
            cli_args.append("--whitelist-regex")
            cli_args.append(whitelist_regex)

        if output:
            cli_args.append("--output")
            cli_args.append(output)

        if omit_covered_files:
            cli_args.append("--omit-covered-files")

        if generate_badge:
            cli_args.append("--generate-badge")
            cli_args.append(generate_badge)

        if badge_format:
            cli_args.append("--badge-format")
            cli_args.append(badge_format)

        if badge_style:
            cli_args.append("--badge-style")
            cli_args.append(badge_style)

        if config:
            cli_args.append("--config")
            cli_args.append(config)

        if color is True:
            cli_args.append("--color")
        elif color is False:
            cli_args.append("--no-color")

        super().__init__(cli_args)

    def __call__(self) -> None:
        """Run the command."""
        from interrogate.cli import main as run_interrogate  # noqa: PLC0415

        return run_interrogate(self.cli_args)
