from mkdocs.__main__ import cli as mkdocs


def run(*args, quiet: bool = False, verbose: bool = False):
    cli_args = list(args)

    if quiet and "-q" not in cli_args:
        cli_args.append("--quiet")

    if verbose and "-v" not in cli_args:
        cli_args.append("--verbose")

    mkdocs(cli_args)


def build(
    clean: bool | None = None,
    config_file: str | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
):
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


def gh_deploy(
    clean: bool | None = None,
    message: str | None = None,
    remote_branch: str | None = None,
    remote_name: str | None = None,
    force: bool | None = None,
    no_history: bool | None = None,
    ignore_version: bool | None = None,
    shell: bool | None = None,
    config_file: str | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    site_dir: str | None = None,
    quiet: bool = False,
    verbose: bool = False,
):
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


def new(project_directory: str, quiet: bool = False, verbose: bool = False):
    run("new", project_directory, quiet=quiet, verbose=verbose)


def serve(
    dev_addr: str | None = None,
    livereload: bool | None = None,
    dirtyreload: bool | None = None,
    watch_theme: bool | None = None,
    watch: list[str] | None = None,
    config_file: str | None = None,
    strict: bool | None = None,
    theme: str | None = None,
    directory_urls: bool | None = None,
    quiet: bool = False,
    verbose: bool = False,
):
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
