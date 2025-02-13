"""Shell completion utilities."""

from __future__ import annotations

import abc
import os
import subprocess
import sys
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Final

if TYPE_CHECKING:
    from collections.abc import Sequence

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

CompletionCandidateType: TypeAlias = "tuple[str, str | None]"


class Shell(metaclass=abc.ABCMeta):
    """ABC for shell completion utils, inherit from it to implement tab-completion for different shells."""

    name: ClassVar[str]
    implementations: Final[dict[str, type[Any]]] = {}

    @abc.abstractmethod
    def parse_completion(self, candidates: Sequence[CompletionCandidateType]) -> str:
        """Parses a list of completion candidates for shell's completion command.

        Parameters:
            candidates: List of completion candidates with optional descriptions.

        Returns:
            String to be passed to shell completion command.
        """

    @abc.abstractmethod
    def install_completion(self) -> None:
        """Installs shell completion."""

    @cached_property
    def completion_script_path(self) -> Path:
        """Returns a path to the shell completion script file."""
        return Path(__file__).parent / f"completions.{self.name}"

    @cached_property
    def install_dir(self) -> Path:
        """Returns a path to the directory in which a shell completion script should be installed."""
        return Path.home() / ".duty"

    @classmethod
    def create(cls, shell_type: str) -> Self:
        """Creates an instance of Shell subclass, based on a shell name.

        Raises:
            NotImplementedError: If shell type is not supported.
        """
        try:
            return cls.implementations[shell_type]()
        except KeyError as exc:
            msg = f"Completions for {shell_type!r} shell are not available, feature requests and PRs welcome!"
            raise NotImplementedError(msg) from exc

    def __init_subclass__(cls) -> None:
        cls.implementations[cls.name] = cls


class Bash(Shell):
    """Completion utils for Bash."""

    name = "bash"

    bash_completion_user_dir = os.environ.get("BASH_COMPLETION_USER_DIR")
    xdg_data_home = os.environ.get("XDG_DATA_HOME")

    @cached_property
    def install_dir(self) -> Path:  # noqa: D102
        if self.bash_completion_user_dir:
            return Path(self.bash_completion_user_dir) / "completions"
        if self.xdg_data_home:
            return Path(self.xdg_data_home) / "bash-completion/completions"
        return Path.home() / ".local/share/bash-completion/completions"

    def parse_completion(self, candidates: Sequence[CompletionCandidateType]) -> str:  # noqa: D102
        return "\n".join(completion for completion, _ in candidates)

    def install_completion(self) -> None:  # noqa: D102
        self.install_dir.mkdir(parents=True, exist_ok=True)
        symlink_path = self.install_dir / "duty"
        print(self.completion_script_path)
        print(symlink_path)
        try:
            symlink_path.symlink_to(self.completion_script_path)
        except FileExistsError:
            print("Bash completions already installed.", file=sys.stderr)
        else:
            print(
                f"Bash completions successfully symlinked to {symlink_path!r}. "
                f"Please reload Bash for changes to take effect.",
            )


class Zsh(Shell):
    """Completion utils for Zsh."""

    name = "zsh"

    site_functions_dirs = (Path("/usr/local/share/zsh/site-functions"), Path("/usr/share/zsh/site-functions"))

    @cached_property
    def install_dir(self) -> Path:  # noqa: D102
        try:
            return next(d for d in self.site_functions_dirs if d.is_dir())
        except StopIteration as exc:
            raise OSError("Zsh site-functions directory not found!") from exc

    def parse_completion(self, candidates: Sequence[CompletionCandidateType]) -> str:  # noqa: D102
        def parse_candidate(item: CompletionCandidateType) -> str:
            completion, help_text = item
            # We only have space for one line of description,
            # so we remove descriptions of sub-command parameters from help_text
            # by removing everything after the first newline.
            return f"{completion}: {help_text or '-'}".split("\n", 1)[0]

        return "\n".join(parse_candidate(candidate) for candidate in candidates)

    def install_completion(self) -> None:  # noqa: D102
        try:
            symlink_path = self.install_dir / "_duty"
            symlink_path.symlink_to(self.completion_script_path)
        except PermissionError:
            # retry as sudo
            if os.geteuid() == 0:
                raise
            subprocess.run(  # noqa: S603
                ["sudo", sys.executable, sys.argv[0], "--install-completion=zsh"],  # noqa: S607
                check=True,
            )
        except FileExistsError:
            print("Zsh completions already installed.", file=sys.stderr)
        else:
            print(
                f"Zsh completions successfully symlinked to {symlink_path}. "
                f"Please reload Zsh for changes to take effect.",
            )
