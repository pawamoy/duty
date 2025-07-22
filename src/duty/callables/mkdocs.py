"""Callable for [MkDocs](https://github.com/mkdocs/mkdocs)."""

from __future__ import annotations

from failprint.lazy import lazy


def run(*args: str, quiet: bool = False, verbose: bool = False) -> None:
    """Run `mkdocs`.

    Parameters:
        *args: CLI arguments.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    from mkdocs.__main__ import cli as mkdocs  # noqa: PLC0415

    cli_args = list(args)

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    mkdocs(cli_args)


@lazy(name="mkdocs.build")
def build(
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    """Build the MkDocs documentation.

    Parameters:
        config_file: Provide a specific MkDocs config.
        clean: Remove old files from the site_dir before building (the default).
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        site_dir: The directory to output the result of the documentation build.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = []

    if clean is True:
        cli_args.append("--clean")
    elif clean is False:
        cli_args.append("--dirty")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    if site_dir:
        cli_args.append("--site_dir")
        cli_args.append(site_dir)

    run("build", *cli_args, quiet=quiet, verbose=verbose)


@lazy(name="mkdocs.gh_deploy")
def gh_deploy(
    *,
    config_file: str | None = None,
    clean: bool | None = None,
    message: str | None = None,
    remote_branch: str | None = None,
    remote_name: str | None = None,
    force: bool | None = None,
    no_history: bool | None = None,
    ignore_version: bool | None = None,
    shell: bool | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    """Deploy your documentation to GitHub Pages.

    Parameters:
        config_file: Provide a specific MkDocs config.
        clean: Remove old files from the site_dir before building (the default).
        message: A commit message to use when committing to the GitHub Pages remote branch.
            Commit {sha} and MkDocs {version} are available as expansions.
        remote_branch: The remote branch to commit to for GitHub Pages. This overrides the value specified in config.
        remote_name: The remote name to commit to for GitHub Pages. This overrides the value specified in config
        force: Force the push to the repository.
        no_history: Replace the whole Git history with one new commit.
        ignore_version: Ignore check that build is not being deployed with an older version of MkDocs.
        shell: Use the shell when invoking Git.
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        site_dir: The directory to output the result of the documentation build.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = []

    if clean is True:
        cli_args.append("--clean")
    elif clean is False:
        cli_args.append("--dirty")

    if message:
        cli_args.append("--message")
        cli_args.append(message)

    if remote_branch:
        cli_args.append("--remote-branch")
        cli_args.append(remote_branch)

    if remote_name:
        cli_args.append("--remote-name")
        cli_args.append(remote_name)

    if force:
        cli_args.append("--force")

    if no_history:
        cli_args.append("--no-history")

    if ignore_version:
        cli_args.append("--ignore-version")

    if shell:
        cli_args.append("--shell")

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    if site_dir:
        cli_args.append("--site_dir")
        cli_args.append(site_dir)

    run("gh-deploy", *cli_args, quiet=quiet, verbose=verbose)


@lazy(name="mkdocs.new")
def new(project_directory: str, *, quiet: bool = False, verbose: bool = False) -> None:
    """Create a new MkDocs project.

    Parameters:
        project_directory: Where to create the project.
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    run("new", project_directory, quiet=quiet, verbose=verbose)


@lazy(name="mkdocs.serve")
def serve(
    *,
    config_file: str | None = None,
    dev_addr: str | None = None,
    livereload: bool | None = None,
    dirtyreload: bool | None = None,
    watch_theme: bool | None = None,
    watch: list[str] | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    quiet: bool = False,
    verbose: bool = False,
) -> None:
    """Run the builtin development server.

    Parameters:
        config_file: Provide a specific MkDocs config.
        dev_addr: IP address and port to serve documentation locally (default: localhost:8000).
        livereload: Enable/disable the live reloading in the development server.
        dirtyreload: nable the live reloading in the development server, but only re-build files that have changed.
        watch_theme: Include the theme in list of files to watch for live reloading. Ignored when live reload is not used.
        watch: Directories or files to watch for live reloading.
        strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        theme: The theme to use when building your documentation.
        directory_urls: Use directory URLs when building pages (the default).
        quiet: Silence warnings.
        verbose: Enable verbose output.
    """
    cli_args = []

    if dev_addr:
        cli_args.append("--dev-addr")
        cli_args.append(dev_addr)

    if livereload is True:
        cli_args.append("--livereload")
    elif livereload is False:
        cli_args.append("--no-livereload")

    if dirtyreload:
        cli_args.append("--dirtyreload")

    if watch_theme:
        cli_args.append("--watch-theme")

    if watch:
        for path in watch:
            cli_args.append("--watch")
            cli_args.append(path)

    if config_file:
        cli_args.append("--config-file")
        cli_args.append(config_file)

    if strict is True:
        cli_args.append("--strict")

    if theme:
        cli_args.append("--theme")
        cli_args.append(theme)

    if directory_urls is True:
        cli_args.append("--use-directory-urls")
    elif directory_urls is False:
        cli_args.append("--no-directory-urls")

    run("serve", *cli_args, quiet=quiet, verbose=verbose)
