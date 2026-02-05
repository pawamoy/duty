from __future__ import annotations

from duty._internal.tools._base import Tool


class zensical(Tool):  # noqa: N801
    """Call [Zensical](https://zensical.org)."""

    cli_name = "zensical"
    """The name of the executable on PATH."""

    @classmethod
    def build(
        cls,
        *,
        config_file: str | None = None,
        clean: bool | None = None,
        strict: bool | None = None,
    ) -> zensical:
        """Build the Zensical documentation.

        Parameters:
            config_file: Provide a specific MkDocs config.
            clean: Remove old files from the site_dir before building (the default).
            strict: Enable strict mode. This will cause MkDocs to abort the build on any warnings.
        """
        cli_args = ["build"]

        if clean is True:
            cli_args.append("--clean")
        elif clean is False:
            cli_args.append("--dirty")

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if strict is True:
            cli_args.append("--strict")

        return cls(cli_args)

    @classmethod
    def new(cls, project_directory: str) -> zensical:
        """Create a new Zensical project.

        Parameters:
            project_directory: Where to create the project.
        """
        cli_args = ["new", project_directory]
        return cls(cli_args)

    @classmethod
    def serve(
        cls,
        *,
        config_file: str | None = None,
        dev_addr: str | None = None,
        open_preview: bool | None = None,
        strict: bool | None = None,
    ) -> zensical:
        """Run the builtin development server.

        Parameters:
            config_file: Provide a specific Zensical config.
            dev_addr: IP address and port to serve documentation locally (default: localhost:8000).
            open_preview: Open preview in default browser.
            strict: Enable strict mode. This will cause Zensical to abort the build on any warnings.
        """
        cli_args = ["serve"]

        if dev_addr:
            cli_args.append("--dev-addr")
            cli_args.append(dev_addr)

        if open_preview is True:
            cli_args.append("--open")

        if config_file:
            cli_args.append("--config-file")
            cli_args.append(config_file)

        if strict is True:
            cli_args.append("--strict")

        return cls(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from zensical.main import cli as run_zensical  # noqa: PLC0415

        return run_zensical(self.cli_args)
