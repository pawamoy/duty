"""Shell completion utilities."""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

CompletionCandidateType = tuple[str, Optional[str]]


class CompletionParser:
    """Shell completion parser."""

    @classmethod
    def parse(cls, candidates: list[CompletionCandidateType], shell: str) -> str:
        """Parses a list of completion candidates for the selected shell's completion command.

        Parameters:
            candidates: List of completion candidates with optional descriptions.
            shell: Shell for which to parse the candidates.

        Raises:
            NotImplementedError: When parser is not implemented for selected shell.

        Returns:
            String to be passed to shell completion command.
        """
        try:
            return getattr(cls, f"_{shell}")(candidates)
        except AttributeError as exc:
            msg = f"Completion parser method for {shell!r} shell is not implemented!"
            raise NotImplementedError(msg) from exc

    @staticmethod
    def _zsh(candidates: list[CompletionCandidateType]) -> str:
        def parse_candidate(item: CompletionCandidateType) -> str:
            completion, help_text = item
            # We only have space for one line of description,
            # so we remove descriptions of sub-command parameters from help_text
            # by removing everything after the first newline.
            return f"{completion}: {help_text or '-'}".split("\n", 1)[0]

        return "\n".join(parse_candidate(candidate) for candidate in candidates)

    @staticmethod
    def _bash(candidates: list[CompletionCandidateType]) -> str:
        return "\n".join(completion for completion, _ in candidates)


class CompletionInstaller:
    """Shell completion installer."""

    @classmethod
    def install(cls, shell: str) -> None:
        """Installs shell completions for selected shell.

        Raises:
            NotImplementedError: When installer is not implemented for selected shell.
        """
        try:
            return getattr(cls, f"_{shell}")()
        except AttributeError as exc:
            msg = f"Completion installer method for {shell!r} shell is not implemented!"
            raise NotImplementedError(msg) from exc

    @staticmethod
    def get_completion_script_path(shell: str) -> Path:
        """Gets the path of a shell completion script for the selected shell."""
        completions_file_path = Path(__file__).parent / f"completions.{shell}"
        if not completions_file_path.exists():
            msg = f"Completions for {shell!r} shell are not available, feature requests and PRs welcome!"
            raise NotImplementedError(msg)
        return completions_file_path

    @classmethod
    def _zsh(cls) -> None:
        site_functions_dirs = (Path("/usr/local/share/zsh/site-functions"), Path("/usr/share/zsh/site-functions"))
        try:
            completions_dir = next(d for d in site_functions_dirs if d.is_dir())
        except StopIteration as exc:
            raise OSError("Zsh site-functions directory not found!") from exc

        try:
            symlink_path = completions_dir / "_duty"
            symlink_path.symlink_to(cls.get_completion_script_path("zsh"))
        except PermissionError:
            # retry as sudo
            if os.geteuid() == 0:
                raise
            subprocess.run(  # noqa: S603
                ["sudo", sys.executable, sys.argv[0], "--install-completion=zsh"],  # noqa: S607
                check=True,
            )
        except FileExistsError:
            print("Zsh completions already installed.")
        else:
            print(
                f"Zsh completions successfully symlinked to {symlink_path}. "
                f"Please reload Zsh for changes to take effect.",
            )

    @classmethod
    def _bash(cls) -> None:
        bash_completion_user_dir = os.environ.get("BASH_COMPLETION_USER_DIR")
        xdg_data_home = os.environ.get("XDG_DATA_HOME")

        if bash_completion_user_dir:
            completion_dir = Path(bash_completion_user_dir) / "completions"
        elif xdg_data_home:
            completion_dir = Path(xdg_data_home) / "bash-completion/completions"
        else:
            completion_dir = Path.home() / ".local/share/bash-completion/completions"

        completion_dir.mkdir(parents=True, exist_ok=True)
        symlink_path = completion_dir / "duty"
        try:
            symlink_path.symlink_to(cls.get_completion_script_path("bash"))
        except FileExistsError:
            print("Bash completions already installed.")
        else:
            print(
                f"Bash completions successfully symlinked to {symlink_path!r}. "
                f"Please reload Bash for changes to take effect.",
            )
