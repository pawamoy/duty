# YORE: Bump 2: Remove file.

from __future__ import annotations

from typing import Literal

from failprint import lazy


def run(*args: str, version: bool = False, debug_info: bool = False) -> None:
    """Run `griffe`.

    Parameters:
        *args: CLI arguments.
        version: Show program's version number and exit.
        debug_info: Print debug information.
    """
    from griffe.cli import main as griffe  # noqa: PLC0415

    cli_args = []

    # --version and --debug-info must appear first.
    if version:
        cli_args.append("--version")

    if debug_info:
        cli_args.append("--debug-info")

    cli_args.extend(args)

    griffe(cli_args)


@lazy(name="griffe.check")
def check(
    package: str,
    *,
    against: str | None = None,
    base_ref: str | None = None,
    color: bool = False,
    verbose: bool = False,
    format: Literal["oneline", "verbose", "markdown", "github"] | None = None,  # noqa: A002
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> None:
    """Check for API breakages or possible improvements.

    Parameters:
        package: Package to find, load and check, as path.
        against: Older Git reference (commit, branch, tag) to check against. Default: load latest tag.
        base_ref: Git reference (commit, branch, tag) to check. Default: load current code.
        color: Force enable/disable colors in the output.
        verbose: Verbose output.
        format: Output format.
        search: Paths to search packages into.
        sys_path: Whether to append `sys.path` to search paths specified with `-s`.
        find_stubs_packages: Whether to look for stubs-only packages and merge them with concrete ones.
        extensions: A comma-separated list or a JSON list of extensions to load.
        inspection: Whether to disallow or force inspection (dynamic analysis).
            By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
        log_level: Set the log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
        version: Show program's version number and exit.
        debug_info: Print debug information.
    """
    cli_args = []

    if package:
        cli_args.append(package)

    if against:
        cli_args.append("--against")
        cli_args.append(against)

    if base_ref:
        cli_args.append("--base-ref")
        cli_args.append(base_ref)

    if color is True:
        cli_args.append("--color")
    elif color is False:
        cli_args.append("--no-color")

    if verbose:
        cli_args.append("--verbose")

    if format:
        cli_args.append("--format")
        cli_args.append(format)

    if search:
        for path in search:
            cli_args.append("--search")
            cli_args.append(path)

    if sys_path:
        cli_args.append("--sys-path")

    if find_stubs_packages:
        cli_args.append("--find-stubs-packages")

    if extensions:
        cli_args.append("--extensions")
        if isinstance(extensions, str):
            cli_args.append(extensions)
        else:
            cli_args.append(",".join(extensions))

    if inspection is True:
        cli_args.append("--force-inspection")
    elif inspection is False:
        cli_args.append("--no-inspection")

    if log_level:
        cli_args.append("--log-level")
        cli_args.append(log_level)

    run("check", *cli_args, version=version, debug_info=debug_info)


@lazy(name="griffe.dump")
def dump(
    *packages: str,
    full: bool = False,
    output: str | None = None,
    docstyle: str | None = None,
    docopts: str | None = None,
    resolve_aliases: bool = False,
    resolve_implicit: bool = False,
    resolve_external: bool | None = None,
    stats: bool = False,
    search: list[str] | None = None,
    sys_path: bool = False,
    find_stubs_packages: bool = False,
    extensions: str | list[str] | None = None,
    inspection: bool | None = None,
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None,
    version: bool = False,
    debug_info: bool = False,
) -> None:
    """Load package-signatures and dump them as JSON.

    Parameters:
        packages: Packages to find, load and dump.
        full: Whether to dump full data in JSON.
        output: Output file. Supports templating to output each package in its own file, with `{package}`.
        docstyle: The docstring style to parse.
        docopts: The options for the docstring parser.
        resolve_aliases: Whether to resolve aliases.
        resolve_implicit: Whether to resolve implicitely exported aliases as well. Aliases are explicitely exported when defined in `__all__`.
        resolve_external: Whether to resolve aliases pointing to external/unknown modules (not loaded directly).
            Default is to resolve only from one module to its private sibling (`ast` -> `_ast`).
        stats: Show statistics at the end.
        search: Paths to search packages into.
        sys_path: Whether to append `sys.path` to search paths specified with `-s`.
        find_stubs_packages: Whether to look for stubs-only packages and merge them with concrete ones.
        extensions: A comma-separated list or a JSON list of extensions to load.
        inspection: Whether to disallow or force inspection (dynamic analysis).
            By default, Griffe tries to use static analysis and falls back to dynamic analysis when it can't.
        log_level: Set the log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
        version: Show program's version number and exit.
        debug_info: Print debug information.
    """
    cli_args = list(packages)

    if full:
        cli_args.append("--full")

    if output:
        cli_args.append("--output")
        cli_args.append(output)

    if docstyle:
        cli_args.append("--docstyle")
        cli_args.append(docstyle)

    if docopts:
        cli_args.append("--docopts")
        cli_args.append(docopts)

    if resolve_aliases:
        cli_args.append("--resolve-aliases")

    if resolve_implicit:
        cli_args.append("--resolve-implicit")

    if resolve_external is True:
        cli_args.append("--resolve-external")
    elif resolve_external is False:
        cli_args.append("--no-resolve-external")

    if stats:
        cli_args.append("--stats")

    if search:
        for path in search:
            cli_args.append("--search")
            cli_args.append(path)

    if sys_path:
        cli_args.append("--sys-path")

    if find_stubs_packages:
        cli_args.append("--find-stubs-packages")

    if extensions:
        cli_args.append("--extensions")
        if isinstance(extensions, str):
            cli_args.append(extensions)
        else:
            cli_args.append(",".join(extensions))

    if inspection is True:
        cli_args.append("--force-inspection")
    elif inspection is False:
        cli_args.append("--no-inspection")

    if log_level:
        cli_args.append("--log-level")
        cli_args.append(log_level)

    run("check", *cli_args, version=version, debug_info=debug_info)
