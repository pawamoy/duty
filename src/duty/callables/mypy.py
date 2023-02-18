"""Callable for [Mypy](https://github.com/python/mypy)."""

from __future__ import annotations

import sys

from duty.callables import lazy
from duty.callables._io import _LazyStderr, _LazyStdout

# TODO: remove once support for Python 3.7 is dropped
if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


@lazy("mypy")
def run(
    *paths: str,
    config_file: str | None = None,
    enable_incomplete_feature: bool | None = None,
    verbose: bool | None = None,
    warn_unused_configs: bool | None = None,
    no_namespace_packages: bool | None = None,
    ignore_missing_imports: bool | None = None,
    follow_imports: Literal["normal", "silent", "skip", "error"] | None = None,
    python_executable: str | None = None,
    no_site_packages: bool | None = None,
    no_silence_site_packages: bool | None = None,
    python_version: str | None = None,
    py2: bool | None = None,
    platform: str | None = None,
    always_true: list[str] | None = None,
    always_false: list[str] | None = None,
    disallow_any_unimported: bool | None = None,
    disallow_any_expr: bool | None = None,
    disallow_any_decorated: bool | None = None,
    disallow_any_explicit: bool | None = None,
    disallow_any_generics: bool | None = None,
    disallow_subclassing_any: bool | None = None,
    disallow_untyped_calls: bool | None = None,
    disallow_untyped_defs: bool | None = None,
    disallow_incomplete_defs: bool | None = None,
    check_untyped_defs: bool | None = None,
    disallow_untyped_decorators: bool | None = None,
    implicit_optional: bool | None = None,
    no_strict_optional: bool | None = None,
    warn_redundant_casts: bool | None = None,
    warn_unused_ignores: bool | None = None,
    no_warn_no_return: bool | None = None,
    warn_return_any: bool | None = None,
    warn_unreachable: bool | None = None,
    allow_untyped_globals: bool | None = None,
    allow_redefinition: bool | None = None,
    no_implicit_reexport: bool | None = None,
    strict_equality: bool | None = None,
    strict_concatenate: bool | None = None,
    strict: bool | None = None,
    disable_error_code: str | None = None,
    enable_error_code: str | None = None,
    show_error_context: bool | None = None,
    show_column_numbers: bool | None = None,
    show_error_end: bool | None = None,
    hide_error_codes: bool | None = None,
    pretty: bool | None = None,
    no_color_output: bool | None = None,
    no_error_summary: bool | None = None,
    show_absolute_path: bool | None = None,
    no_incremental: bool | None = None,
    cache_dir: str | None = None,
    sqlite_cache: bool | None = None,
    cache_fine_grained: bool | None = None,
    skip_version_check: bool | None = None,
    skip_cache_mtime_checks: bool | None = None,
    pdb: bool | None = None,
    show_traceback: bool | None = None,
    raise_exceptions: bool | None = None,
    custom_typing_module: str | None = None,
    disable_recursive_aliases: bool | None = None,
    custom_typeshed_dir: str | None = None,
    warn_incomplete_stub: bool | None = None,
    shadow_file: tuple[str, str] | None = None,
    any_exprs_report: str | None = None,
    cobertura_xml_report: str | None = None,
    html_report: str | None = None,
    linecount_report: str | None = None,
    linecoverage_report: str | None = None,
    lineprecision_report: str | None = None,
    txt_report: str | None = None,
    xml_report: str | None = None,
    xslt_html_report: str | None = None,
    xslt_txt_report: str | None = None,
    junit_xml: str | None = None,
    find_occurrences: str | None = None,
    scripts_are_modules: bool | None = None,
    install_types: bool | None = None,
    non_interactive: bool | None = None,
    explicit_package_bases: bool | None = None,
    exclude: str | None = None,
    module: str | None = None,
    package: str | None = None,
    command: str | None = None,
) -> None:
    r"""Run mypy.

    Parameters:
        *paths: Path to scan.
        config_file: Configuration file, must have a [mypy] section (defaults to mypy.ini, .mypy.ini,
        enable_incomplete_feature: Enable support of incomplete/experimental features for early preview.
        verbose: More verbose messages.
            pyproject.toml, setup.cfg, /home/pawamoy/.config/mypy/config, ~/.config/mypy/config, ~/.mypy.ini).
        warn_unused_configs: Warn about unused '[mypy-<pattern>]' or '[[tool.mypy.overrides]]' config sections
            (inverse: --no-warn-unused-configs).
        no_namespace_packages: Support namespace packages (PEP 420, __init__.py-less) (inverse: --namespace-packages).
        ignore_missing_imports: Silently ignore imports of missing modules.
        follow_imports: How to treat imports (default normal).
        python_executable: Python executable used for finding PEP 561 compliant installed packages and stubs.
        no_site_packages: Do not search for installed PEP 561 compliant packages.
        no_silence_site_packages: Do not silence errors in PEP 561 compliant installed packages.
        python_version: Type check code assuming it will be running on Python x.y.
        py2: Use Python 2 mode (same as --python-version 2.7).
        platform: Type check special-cased code for the given OS platform (defaults to sys.platform).
        always_true: Additional variable to be considered True (may be repeated).
        always_false: Additional variable to be considered False (may be repeated).
        disallow_any_unimported: Disallow Any types resulting from unfollowed imports.
        disallow_any_expr: Disallow all expressions that have type Any.
        disallow_any_decorated: Disallow functions that have Any in their signature after decorator transformation.
        disallow_any_explicit: Disallow explicit Any in type positions.
        disallow_any_generics: Disallow usage of generic types that do not specify explicit type parameters
            (inverse: --allow-any-generics).
        disallow_subclassing_any: Disallow subclassing values of type 'Any' when defining classes
            (inverse: --allow-subclassing-any).
        disallow_untyped_calls: Disallow calling functions without type annotations from functions with type annotations
            (inverse: --allow-untyped-calls).
        disallow_untyped_defs: Disallow defining functions without type annotations or with incomplete type annotations
            (inverse: --allow-untyped-defs).
        disallow_incomplete_defs: Disallow defining functions with incomplete type annotations
            (inverse: --allow-incomplete-defs).
        check_untyped_defs: Type check the interior of functions without type annotations
            (inverse: --no-check-untyped-defs).
        disallow_untyped_decorators: Disallow decorating typed functions with untyped decorators
            (inverse: --allow-untyped-decorators).
        implicit_optional: Assume arguments with default values of None are Optional(inverse: --no-implicit-optional).
        no_strict_optional: Disable strict Optional checks (inverse: --strict-optional).
        warn_redundant_casts: Warn about casting an expression to its inferred type (inverse: --no-warn-redundant-casts).
        warn_unused_ignores: Warn about unneeded '# type: ignore' comments (inverse: --no-warn-unused-ignores).
        no_warn_no_return: Do not warn about functions that end without returning (inverse: --warn-no-return).
        warn_return_any: Warn about returning values of type Any from non-Any typed functions (inverse: --no-warn-return-any).
        warn_unreachable: Warn about statements or expressions inferred to be unreachable (inverse: --no-warn-unreachable).
        allow_untyped_globals: Suppress toplevel errors caused by missing annotations (inverse: --disallow-untyped-globals).
        allow_redefinition: Allow unconditional variable redefinition with a new type (inverse: --disallow-redefinition).
        no_implicit_reexport: Treat imports as private unless aliased (inverse: --implicit-reexport).
        strict_equality: Prohibit equality, identity, and container checks for non-overlapping types
            (inverse: --no-strict-equality).
        strict_concatenate: Make arguments prepended via Concatenate be truly positional-only (inverse: --no-strict-concatenate).
        strict: Strict mode; enables the following flags: --warn-unused-configs, --disallow-any-generics,
            --disallow-subclassing-any, --disallow-untyped-calls, --disallow-untyped-defs, --disallow-incomplete-defs,
            --check-untyped-defs, --disallow-untyped-decorators, --warn-redundant-casts, --warn-unused-ignores,
            --warn-return-any, --no-implicit-reexport, --strict-equality, --strict-concatenate.
        disable_error_code: Disable a specific error code.
        enable_error_code: Enable a specific error code.
        show_error_context: Precede errors with "note:" messages explaining context (inverse: --hide-error-context).
        show_column_numbers: Show column numbers in error messages (inverse: --hide-column-numbers).
        show_error_end: Show end line/end column numbers in error messages. This implies --show-column-numbers
            (inverse: --hide-error-end).
        hide_error_codes: Hide error codes in error messages (inverse: --show-error-codes).
        pretty: Use visually nicer output in error messages: Use soft word wrap, show source code snippets,
            and show error location markers (inverse: --no-pretty).
        no_color_output: Do not colorize error messages (inverse: --color-output).
        no_error_summary: Do not show error stats summary (inverse: --error-summary).
        show_absolute_path: Show absolute paths to files (inverse: --hide-absolute-path).
        no_incremental: Disable module cache (inverse: --incremental).
        cache_dir: Store module cache info in the given folder in incremental mode (defaults to '.mypy_cache').
        sqlite_cache: Use a sqlite database to store the cache (inverse: --no-sqlite-cache).
        cache_fine_grained: Include fine-grained dependency information in the cache for the mypy daemon.
        skip_version_check: Allow using cache written by older mypy version.
        skip_cache_mtime_checks: Skip cache internal consistency checks based on mtime.
        pdb: Invoke pdb on fatal error.
        show_traceback: Show traceback on fatal error.
        raise_exceptions: Raise exception on fatal error.
        custom_typing_module: Use a custom typing module.
        disable_recursive_aliases: Disable experimental support for recursive type aliases.
        custom_typeshed_dir: Use the custom typeshed in DIR.
        warn_incomplete_stub: Warn if missing type annotation in typeshed, only relevant with --disallow-untyped-defs
            or --disallow-incomplete-defs enabled (inverse: --no-warn-incomplete-stub).
        shadow_file: When encountering SOURCE_FILE, read and type check the contents of SHADOW_FILE instead..
        any_exprs_report: Report any expression.
        cobertura_xml_report: Report Cobertura.
        html_report: Report HTML.
        linecount_report: Report line count.
        linecoverage_report: Report line coverage.
        lineprecision_report: Report line precision.
        txt_report: Report text.
        xml_report: Report XML.
        xslt_html_report: Report XLST HTML.
        xslt_txt_report: Report XLST text.
        junit_xml: Write junit.xml to the given file.
        find_occurrences: Print out all usages of a class member (experimental).
        scripts_are_modules: Script x becomes module x instead of __main__.
        install_types: Install detected missing library stub packages using pip (inverse: --no-install-types).
        non_interactive: Install stubs without asking for confirmation and hide errors, with --install-types
            (inverse: --interactive).
        explicit_package_bases: Use current directory and MYPYPATH to determine module names of files passed
            (inverse: --no-explicit-package-bases).
        exclude: Regular expression to match file names, directory names or paths which mypy should ignore while
            recursively discovering files to check, e.g. --exclude '/setup\.py$'.
            May be specified more than once, eg. --exclude a --exclude b.
        module: Type-check module; can repeat for more modules.
        package: Type-check package recursively; can be repeated.
        command: Type-check program passed in as string.
    """
    from mypy.main import main as mypy

    cli_args = list(paths)

    if enable_incomplete_feature:
        cli_args.append("--enable-incomplete-feature")

    if verbose:
        cli_args.append("--verbose")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if warn_unused_configs:
        cli_args.append("--warn-unused-configs")

    if no_namespace_packages:
        cli_args.append("--no-namespace-packages")

    if ignore_missing_imports:
        cli_args.append("--ignore-missing-imports")

    if follow_imports:
        cli_args.append("--follow-imports")
        cli_args.append(follow_imports)

    if python_executable:
        cli_args.append("--python-executable")
        cli_args.append(python_executable)

    if no_site_packages:
        cli_args.append("--no-site-packages")

    if no_silence_site_packages:
        cli_args.append("--no-silence-site-packages")

    if python_version:
        cli_args.append("--python-version")
        cli_args.append(python_version)

    if py2:
        cli_args.append("--py2")

    if platform:
        cli_args.append("--platform")
        cli_args.append(platform)

    if always_true:
        for posarg in always_true:
            cli_args.append("--always-true")
            cli_args.append(posarg)

    if always_false:
        for posarg in always_false:
            cli_args.append("--always-false")
            cli_args.append(posarg)

    if disallow_any_unimported:
        cli_args.append("--disallow-any-unimported")

    if disallow_any_expr:
        cli_args.append("--disallow-any-expr")

    if disallow_any_decorated:
        cli_args.append("--disallow-any-decorated")

    if disallow_any_explicit:
        cli_args.append("--disallow-any-explicit")

    if disallow_any_generics:
        cli_args.append("--disallow-any-generics")

    if disallow_subclassing_any:
        cli_args.append("--disallow-subclassing-any")

    if disallow_untyped_calls:
        cli_args.append("--disallow-untyped-calls")

    if disallow_untyped_defs:
        cli_args.append("--disallow-untyped-defs")

    if disallow_incomplete_defs:
        cli_args.append("--disallow-incomplete-defs")

    if check_untyped_defs:
        cli_args.append("--check-untyped-defs")

    if disallow_untyped_decorators:
        cli_args.append("--disallow-untyped-decorators")

    if implicit_optional:
        cli_args.append("--implicit-optional")

    if no_strict_optional:
        cli_args.append("--no-strict-optional")

    if warn_redundant_casts:
        cli_args.append("--warn-redundant-casts")

    if warn_unused_ignores:
        cli_args.append("--warn-unused-ignores")

    if no_warn_no_return:
        cli_args.append("--no-warn-no-return")

    if warn_return_any:
        cli_args.append("--warn-return-any")

    if warn_unreachable:
        cli_args.append("--warn-unreachable")

    if allow_untyped_globals:
        cli_args.append("--allow-untyped-globals")

    if allow_redefinition:
        cli_args.append("--allow-redefinition")

    if no_implicit_reexport:
        cli_args.append("--no-implicit-reexport")

    if strict_equality:
        cli_args.append("--strict-equality")

    if strict_concatenate:
        cli_args.append("--strict-concatenate")

    if strict:
        cli_args.append("--strict")

    if disable_error_code:
        cli_args.append("--disable-error-code")
        cli_args.append(disable_error_code)

    if enable_error_code:
        cli_args.append("--enable-error-code")
        cli_args.append(enable_error_code)

    if show_error_context:
        cli_args.append("--show-error-context")

    if show_column_numbers:
        cli_args.append("--show-column-numbers")

    if show_error_end:
        cli_args.append("--show-error-end")

    if hide_error_codes:
        cli_args.append("--hide-error-codes")

    if pretty:
        cli_args.append("--pretty")

    if no_color_output:
        cli_args.append("--no-color-output")

    if no_error_summary:
        cli_args.append("--no-error-summary")

    if show_absolute_path:
        cli_args.append("--show-absolute-path")

    if no_incremental:
        cli_args.append("--no-incremental")

    if cache_dir:
        cli_args.append("--cache-dir")
        cli_args.append(cache_dir)

    if sqlite_cache:
        cli_args.append("--sqlite-cache")

    if cache_fine_grained:
        cli_args.append("--cache-fine-grained")

    if skip_version_check:
        cli_args.append("--skip-version-check")

    if skip_cache_mtime_checks:
        cli_args.append("--skip-cache-mtime-checks")

    if pdb:
        cli_args.append("--pdb")

    if show_traceback:
        cli_args.append("--show-traceback")

    if raise_exceptions:
        cli_args.append("--raise-exceptions")

    if custom_typing_module:
        cli_args.append("--custom-typing-module")
        cli_args.append(custom_typing_module)

    if disable_recursive_aliases:
        cli_args.append("--disable-recursive-aliases")

    if custom_typeshed_dir:
        cli_args.append("--custom-typeshed-dir")
        cli_args.append(custom_typeshed_dir)

    if warn_incomplete_stub:
        cli_args.append("--warn-incomplete-stub")

    if shadow_file:
        cli_args.append("--shadow-file")
        cli_args.extend(shadow_file)

    if any_exprs_report:
        cli_args.append("--any-exprs-report")
        cli_args.append(any_exprs_report)

    if cobertura_xml_report:
        cli_args.append("--cobertura-xml-report")
        cli_args.append(cobertura_xml_report)

    if html_report:
        cli_args.append("--html-report")
        cli_args.append(html_report)

    if linecount_report:
        cli_args.append("--linecount-report")
        cli_args.append(linecount_report)

    if linecoverage_report:
        cli_args.append("--linecoverage-report")
        cli_args.append(linecoverage_report)

    if lineprecision_report:
        cli_args.append("--lineprecision-report")
        cli_args.append(lineprecision_report)

    if txt_report:
        cli_args.append("--txt-report")
        cli_args.append(txt_report)

    if xml_report:
        cli_args.append("--xml-report")
        cli_args.append(xml_report)

    if xslt_html_report:
        cli_args.append("--xslt-html-report")
        cli_args.append(xslt_html_report)

    if xslt_txt_report:
        cli_args.append("--xslt-txt-report")
        cli_args.append(xslt_txt_report)

    if junit_xml:
        cli_args.append("--junit-xml")
        cli_args.append(junit_xml)

    if find_occurrences:
        cli_args.append("--find-occurrences")
        cli_args.append(find_occurrences)

    if scripts_are_modules:
        cli_args.append("--scripts-are-modules")

    if install_types:
        cli_args.append("--install-types")

    if non_interactive:
        cli_args.append("--non-interactive")

    if explicit_package_bases:
        cli_args.append("--explicit-package-bases")

    if exclude:
        cli_args.append("--exclude")
        cli_args.append(exclude)

    if module:
        cli_args.append("--module")
        cli_args.append(module)

    if package:
        cli_args.append("--package")
        cli_args.append(package)

    if command:
        cli_args.append("--command")
        cli_args.append(command)

    mypy(
        args=cli_args,
        stdout=_LazyStdout(),
        stderr=_LazyStderr(),
        clean_exit=True,
    )
