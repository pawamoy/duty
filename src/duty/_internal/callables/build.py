# YORE: Bump 2: Remove file.

from __future__ import annotations

from typing import Literal

from failprint import lazy


@lazy(name="build")
def run(
    srcdir: str | None = None,
    *,
    version: bool = False,
    verbose: bool = False,
    sdist: bool = False,
    wheel: bool = False,
    outdir: str | None = None,
    skip_dependency_check: bool = False,
    no_isolation: bool = False,
    installer: Literal["pip", "uv"] | None = None,
    config_setting: list[str] | None = None,
) -> None:
    """Run `build`.

    Parameters:
        srcdir: Source directory (defaults to current directory).
        version: Show program's version number and exit.
        verbose: Increase verbosity
        sdist: Build a source distribution (disables the default behavior).
        wheel: Build a wheel (disables the default behavior).
        outdir: Output directory (defaults to `{srcdir}/dist`).
        skip_dependency_check: Do not check that build dependencies are installed.
        no_isolation: Disable building the project in an isolated virtual environment.
            Build dependencies must be installed separately when this option is used.
        installer: Python package installer to use (defaults to pip).
        config_setting: Settings to pass to the backend. Multiple settings can be provided.
    """
    from build.__main__ import main as build  # noqa: PLC0415

    cli_args = []

    if srcdir:
        cli_args.append(srcdir)

    if version:
        cli_args.append("--version")

    if verbose:
        cli_args.append("--verbose")

    if sdist:
        cli_args.append("--sdist")

    if wheel:
        cli_args.append("--wheel")

    if outdir:
        cli_args.append("--outdir")
        cli_args.append(outdir)

    if skip_dependency_check:
        cli_args.append("--skip-dependency-check")

    if no_isolation:
        cli_args.append("--no-isolation")

    if installer:
        cli_args.append("--installer")
        cli_args.append(installer)

    if config_setting:
        for setting in config_setting:
            cli_args.append(f"--config-setting={setting}")

    build(cli_args)
