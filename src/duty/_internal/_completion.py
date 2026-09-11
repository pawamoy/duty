# Shell completion utilities.
#
# To add support for a new shell, subclass `Shell`, set its `name` class
# attribute, and implement `parse_candidates` and `install_path`.
# Subclasses register themselves automatically.

from __future__ import annotations

import abc
import os
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

CompletionCandidate = tuple[str, "str | None"]
"""A completion candidate: a word, and an optional description."""


class CompletionError(Exception):
    """Error raised when shell completions cannot be printed or installed."""


def shell_name(value: str | bool) -> str:  # noqa: FBT001
    """Return the name of a shell.

    Parameters:
        value: A shell name, or `True` to detect it from the `SHELL` environment variable.

    Raises:
        CompletionError: When the shell cannot be detected.

    Returns:
        A lowercase shell name, such as `bash` or `zsh`.
    """
    if value is not True:
        return str(value).lower()
    # `SHELL` is the user's login shell, not the running one:
    # it can be wrong, for example when running Bash from Zsh.
    # That is why we recommend passing the shell explicitly.
    shell = os.environ.get("SHELL", "")
    if not shell:
        raise CompletionError(
            "Could not detect the current shell (the `SHELL` environment variable is not set). "
            "Please specify it explicitly, for example `--completion=bash`.",
        )
    return os.path.basename(shell).lower()


class Shell(abc.ABC):
    """Base class for shell-specific completion support."""

    name: ClassVar[str]
    """The shell name, as found in the `SHELL` environment variable."""

    implementations: ClassVar[dict[str, type[Shell]]] = {}
    """Registry of supported shells, mapping shell names to their implementations."""

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Register a shell implementation."""
        super().__init_subclass__(**kwargs)
        Shell.implementations[cls.name] = cls

    @classmethod
    def create(cls, name: str) -> Shell:
        """Create a shell instance from a shell name.

        Parameters:
            name: The shell name, such as `bash` or `zsh`.

        Raises:
            CompletionError: When the shell is not supported.

        Returns:
            A shell instance.
        """
        try:
            return cls.implementations[name]()
        except KeyError as error:
            supported = ", ".join(sorted(cls.implementations))
            raise CompletionError(
                f"Completions for the {name!r} shell are not available "
                f"(supported shells: {supported}), feature requests and PRs welcome!",
            ) from error

    @property
    def script_path(self) -> Path:
        """The path to our completion script for this shell."""
        # Completion scripts are packaged in the `duty` package, next to the `_internal` package.
        return Path(__file__).parent.parent / f"completions.{self.name}"

    @property
    @abc.abstractmethod
    def install_path(self) -> Path:
        """The path the completion script must be installed (symlinked) to.

        Raises:
            CompletionError: When no suitable installation directory was found.
        """

    @abc.abstractmethod
    def parse_candidates(self, candidates: Sequence[CompletionCandidate]) -> str:
        """Render completion candidates for this shell's completion function.

        Parameters:
            candidates: Completion candidates, with optional descriptions.

        Returns:
            The text to print for the shell's completion function to consume.
        """

    def install(self) -> Path:
        """Symlink our completion script into the shell's completion directory.

        An existing file or symlink is replaced, so that completions are always up-to-date.

        Raises:
            CompletionError: When completions could not be installed.

        Returns:
            The path the completion script was installed to.
        """
        install_path = self.install_path
        try:
            install_path.parent.mkdir(parents=True, exist_ok=True)
            install_path.unlink(missing_ok=True)
            install_path.symlink_to(self.script_path)
        except PermissionError as error:
            raise CompletionError(
                f"Permission denied when writing to {install_path}. "
                f"Try again with higher privileges: `sudo duty --install-completion={self.name}`. "
                f"Alternatively, write the completion script somewhere you have access to: "
                f"`duty --completion={self.name} > /path/to/completions/{install_path.name}`.",
            ) from error
        except OSError as error:
            raise CompletionError(f"Could not install completions in {install_path}: {error}") from error
        return install_path


class Bash(Shell):
    """Completion support for Bash."""

    name = "bash"

    @property
    def install_path(self) -> Path:
        """The path of the `duty` completion script within Bash's user completion directory.

        Raises:
            CompletionError: When the user completion directory was not found.
        """
        if user_dir := os.environ.get("BASH_COMPLETION_USER_DIR"):
            completions_dir = Path(user_dir)
        elif data_home := os.environ.get("XDG_DATA_HOME"):
            completions_dir = Path(data_home) / "bash-completion"
        else:
            completions_dir = Path.home() / ".local/share/bash-completion"
        if not completions_dir.is_dir():
            raise CompletionError(
                f"Bash completion directory not found (searched in {completions_dir}). "
                "Make sure `bash-completion` is installed.",
            )
        return completions_dir / "completions" / "duty"

    def parse_candidates(self, candidates: Sequence[CompletionCandidate]) -> str:
        """Render completion candidates for `compgen`, one word per line (Bash has no descriptions).

        Parameters:
            candidates: Completion candidates, with optional descriptions.

        Returns:
            The candidate words, one per line.
        """
        return "\n".join(word for word, _ in candidates)


class Zsh(Shell):
    """Completion support for Zsh."""

    name = "zsh"

    site_functions_dirs: ClassVar[Iterable[Path]] = (
        Path("/usr/local/share/zsh/site-functions"),
        Path("/usr/share/zsh/site-functions"),
    )
    """Directories that Zsh adds to its `fpath` by default."""

    @property
    def install_path(self) -> Path:
        """The path of the `duty` completion script within Zsh's site-functions directory.

        Raises:
            CompletionError: When no site-functions directory was found.
        """
        for directory in self.site_functions_dirs:
            if directory.is_dir():
                return directory / "_duty"
        searched = ", ".join(str(directory) for directory in self.site_functions_dirs)
        raise CompletionError(
            f"Zsh site-functions directory not found (searched in {searched}). Make sure Zsh is installed.",
        )

    def parse_candidates(self, candidates: Sequence[CompletionCandidate]) -> str:
        """Render completion candidates for `_describe`, as `word:description` lines.

        Parameters:
            candidates: Completion candidates, with optional descriptions.

        Returns:
            The candidates and their descriptions, one per line.
        """
        return "\n".join(self._parse_candidate(word, description) for word, description in candidates)

    @staticmethod
    def _parse_candidate(word: str, description: str | None) -> str:
        # Colons separate words from their descriptions, so they must be escaped within words.
        word = word.replace(":", "\\:")
        if not description:
            return word
        # Descriptions are displayed on a single line, so we only keep the first one.
        first_line = description.split("\n", 1)[0]
        return f"{word}:{first_line}"
