from __future__ import annotations

from duty._internal.tools._base import Tool


class yore(Tool):  # noqa: N801
    """Call [Yore](https://github.com/pawamoy/yore)."""

    cli_name = "yore"
    """The name of the executable on PATH."""

    @classmethod
    def check(
        cls,
        *paths: str,
        bump: str | None = None,
        eol_within: str | None = None,
        bol_within: str | None = None,
    ) -> yore:
        """Check Yore comments against Python EOL dates or the provided next version of your project.

        Parameters:
            paths: Path to files or directories to check.
            bump: The next version of your project.
            eol_within: The time delta to start checking before the End of Life of a Python version.
                It is provided in a human-readable format, like `2 weeks` or `1 month`.
                Spaces are optional, and the unit can be shortened to a single letter:
                `d` for days, `w` for weeks, `m` for months, and `y` for years.
            bol_within: The time delta to start checking before the Beginning of Life of a Python version.
                It is provided in a human-readable format, like `2 weeks` or `1 month`.
                Spaces are optional, and the unit can be shortened to a single letter:
                `d` for days, `w` for weeks, `m` for months, and `y` for years.
        """
        cli_args = ["check", *paths]

        if bump:
            cli_args.append("--bump")
            cli_args.append(bump)

        if eol_within:
            cli_args.append("--eol-within")
            cli_args.append(eol_within)

        if bol_within:
            cli_args.append("--bol-within")
            cli_args.append(bol_within)

        return cls(cli_args)

    @classmethod
    def fix(
        cls,
        *paths: str,
        bump: str | None = None,
        eol_within: str | None = None,
        bol_within: str | None = None,
    ) -> yore:
        """Fix your code by transforming it according to the Yore comments.

        Parameters:
            paths: Path to files or directories to fix.
            bump: The next version of your project.
            eol_within: The time delta to start fixing before the End of Life of a Python version.
                It is provided in a human-readable format, like `2 weeks` or `1 month`.
                Spaces are optional, and the unit can be shortened to a single letter:
                `d` for days, `w` for weeks, `m` for months, and `y` for years.
            bol_within: The time delta to start fixing before the Beginning of Life of a Python version.
                It is provided in a human-readable format, like `2 weeks` or `1 month`.
                Spaces are optional, and the unit can be shortened to a single letter:
                `d` for days, `w` for weeks, `m` for months, and `y` for years.
        """
        cli_args = ["fix", *paths]

        if bump:
            cli_args.append("--bump")
            cli_args.append(bump)

        if eol_within:
            cli_args.append("--eol-within")
            cli_args.append(eol_within)

        if bol_within:
            cli_args.append("--bol-within")
            cli_args.append(bol_within)

        return cls(cli_args)

    def __call__(self) -> int:
        """Run the command.

        Returns:
            The exit code of the command.
        """
        from yore import main as run_yore  # noqa: PLC0415

        return run_yore(self.cli_args)
