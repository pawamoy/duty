from __future__ import annotations

from typing import Any

from duty._internal.tools._base import Tool


class twine(Tool):  # noqa: N801
    """Call [Twine](https://github.com/pypa/twine)."""

    cli_name = "twine"
    """The name of the executable on PATH."""

    @classmethod
    def check(
        cls,
        *dists: str,
        strict: bool = False,
        version: bool = False,
        no_color: bool = False,
    ) -> twine:
        """Checks whether your distribution's long description will render correctly on PyPI.

        Parameters:
            dists: The distribution files to check, usually `dist/*`.
            strict: Fail on warnings.
            version: Show program's version number and exit.
            no_color: Disable colored output.
        """
        cli_args = ["check", *dists]

        if version:
            cli_args.append("--version")

        if no_color:
            cli_args.append("--no-color")

        if strict is True:
            cli_args.append("--strict")

        return cls(cli_args)

    @classmethod
    def register(
        cls,
        package: str,
        *,
        repository: str = "pypi",
        repository_url: str | None = None,
        attestations: bool = False,
        sign: bool = False,
        sign_with: str | None = None,
        identity: str | None = None,
        username: str | None = None,
        password: str | None = None,
        non_interactive: bool = False,
        comment: str | None = None,
        config_file: str | None = None,
        skip_existing: bool = False,
        cert: str | None = None,
        client_cert: str | None = None,
        verbose: bool = False,
        disable_progress_bar: bool = False,
        version: bool = False,
        no_color: bool = False,
    ) -> twine:
        """Pre-register a name with a repository before uploading a distribution.

        Pre-registration is not supported on PyPI, so the register command
        is only necessary if you are using a different repository that requires it.

        Parameters:
            package: File from which we read the package metadata.
            repository: The repository (package index) to upload the package to.
                Should be a section in the config file (default: `pypi`).
                Can also be set via `TWINE_REPOSITORY` environment variable.
            repository_url: The repository (package index) URL to upload the package to. This overrides `--repository`.
                Can also be set via `TWINE_REPOSITORY_URL` environment variable.
            attestations: Upload each file's associated attestations.
            sign: Sign files to upload using GPG.
            sign_with: GPG program used to sign uploads (default: `gpg`).
            identity: GPG identity used to sign files.
            username: The username to authenticate to the repository (package index) as.
                Can also be set via `TWINE_USERNAME` environment variable.
            password: The password to authenticate to the repository (package index) with.
                Can also be set via `TWINE_PASSWORD` environment variable.
            non_interactive: Do not interactively prompt for username/password if the required credentials are missing.
                Can also be set via `TWINE_NON_INTERACTIVE` environment variable.
            comment: The comment to include with the distribution file.
            config_file: The `.pypirc` config file to use.
            skip_existing: Continue uploading files if one already exists.
                Only valid when uploading to PyPI. Other implementations may not support this.
            cert: Path to alternate CA bundle (can also be set via `TWINE_CERT` environment variable).
            client_cert: Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
            verbose: Show verbose output.
            disable_progress_bar: Disable the progress bar.
            version: Show program's version number and exit.
            no_color: Disable colored output.
        """
        cli_args = ["register", package]

        if version:
            cli_args.append("--version")

        if no_color:
            cli_args.append("--no-color")

        if repository:
            cli_args.append("--repository")
            cli_args.append(repository)

        if repository_url:
            cli_args.append("--repository-url")
            cli_args.append(repository_url)

        if attestations:
            cli_args.append("--attestations")

        if sign:
            cli_args.append("--sign")

        if sign_with:
            cli_args.append("--sign-with")
            cli_args.append(sign_with)

        if identity:
            cli_args.append("--identity")
            cli_args.append(identity)

        if username:
            cli_args.append("--username")
            cli_args.append(username)

        if password:
            cli_args.append("--password")
            cli_args.append(password)

        if non_interactive:
            cli_args.append("--non-interactive")

        if comment:
            cli_args.append("--repository")

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if skip_existing:
            cli_args.append("--skip-existing")

        if cert:
            cli_args.append("--cert")
            cli_args.append(cert)

        if client_cert:
            cli_args.append("--client-cert")
            cli_args.append(client_cert)

        if verbose:
            cli_args.append("--verbose")

        if disable_progress_bar:
            cli_args.append("--disable-progress-bar")

        return cls(cli_args)

    @classmethod
    def upload(
        cls,
        *dists: str,
        repository: str = "pypi",
        repository_url: str | None = None,
        attestations: bool = False,
        sign: bool = False,
        sign_with: str | None = None,
        identity: str | None = None,
        username: str | None = None,
        password: str | None = None,
        non_interactive: bool = False,
        comment: str | None = None,
        config_file: str | None = None,
        skip_existing: bool = False,
        cert: str | None = None,
        client_cert: str | None = None,
        verbose: bool = False,
        disable_progress_bar: bool = False,
        version: bool = False,
        no_color: bool = False,
    ) -> twine:
        """Uploads one or more distributions to a repository.

        Parameters:
            dists: The distribution files to check, usually `dist/*`.
            repository: The repository (package index) to upload the package to.
                Should be a section in the config file (default: `pypi`).
                Can also be set via `TWINE_REPOSITORY` environment variable.
            repository_url: The repository (package index) URL to upload the package to. This overrides `--repository`.
                Can also be set via `TWINE_REPOSITORY_URL` environment variable.
            attestations: Upload each file's associated attestations.
            sign: Sign files to upload using GPG.
            sign_with: GPG program used to sign uploads (default: `gpg`).
            identity: GPG identity used to sign files.
            username: The username to authenticate to the repository (package index) as.
                Can also be set via `TWINE_USERNAME` environment variable.
            password: The password to authenticate to the repository (package index) with.
                Can also be set via `TWINE_PASSWORD` environment variable.
            non_interactive: Do not interactively prompt for username/password if the required credentials are missing.
                Can also be set via `TWINE_NON_INTERACTIVE` environment variable.
            comment: The comment to include with the distribution file.
            config_file: The `.pypirc` config file to use.
            skip_existing: Continue uploading files if one already exists.
                Only valid when uploading to PyPI. Other implementations may not support this.
            cert: Path to alternate CA bundle (can also be set via `TWINE_CERT` environment variable).
            client_cert: Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
            verbose: Show verbose output.
            disable_progress_bar: Disable the progress bar.
            version: Show program's version number and exit.
            no_color: Disable colored output.
        """
        cli_args = ["upload", *dists]

        if version:
            cli_args.append("--version")

        if no_color:
            cli_args.append("--no-color")

        if repository:
            cli_args.append("--repository")
            cli_args.append(repository)

        if repository_url:
            cli_args.append("--repository-url")
            cli_args.append(repository_url)

        if attestations:
            cli_args.append("--attestations")

        if sign:
            cli_args.append("--sign")

        if sign_with:
            cli_args.append("--sign-with")
            cli_args.append(sign_with)

        if identity:
            cli_args.append("--identity")
            cli_args.append(identity)

        if username:
            cli_args.append("--username")
            cli_args.append(username)

        if password:
            cli_args.append("--password")
            cli_args.append(password)

        if non_interactive:
            cli_args.append("--non-interactive")

        if comment:
            cli_args.append("--repository")

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if skip_existing:
            cli_args.append("--skip-existing")

        if cert:
            cli_args.append("--cert")
            cli_args.append(cert)

        if client_cert:
            cli_args.append("--client-cert")
            cli_args.append(client_cert)

        if verbose:
            cli_args.append("--verbose")

        if disable_progress_bar:
            cli_args.append("--disable-progress-bar")

        return cls(cli_args)

    def __call__(self) -> Any:
        """Run the command.

        Returns:
            The return value of the corresponding Twine command / entrypoint.
        """
        from twine.cli import dispatch as run_twine  # noqa: PLC0415

        return run_twine(self.cli_args)
