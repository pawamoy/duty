"""Tests for shell completions."""

from __future__ import annotations

from pathlib import Path

import pytest

from duty import main
from duty._internal._completion import Bash, Shell, Zsh


@pytest.fixture(name="bash_dir")
def _fixture_bash_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point Bash's user completion directory at a temporary directory."""
    completions_dir = tmp_path / "bash-completion"
    completions_dir.mkdir()
    monkeypatch.setenv("BASH_COMPLETION_USER_DIR", str(completions_dir))
    return completions_dir


@pytest.fixture(name="zsh_dir")
def _fixture_zsh_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point Zsh's site-functions directories at a temporary directory."""
    site_functions = tmp_path / "site-functions"
    site_functions.mkdir()
    monkeypatch.setattr(Zsh, "site_functions_dirs", (site_functions,))
    return site_functions


def test_supported_shells() -> None:
    """Shell implementations register themselves."""
    assert Shell.implementations == {"bash": Bash, "zsh": Zsh}


@pytest.mark.parametrize(("shell", "expected"), [("bash", "complete -F _complete_duty"), ("zsh", "#compdef duty")])
def test_print_completion_script(shell: str, expected: str, capsys: pytest.CaptureFixture) -> None:
    """Print the completion script of a given shell."""
    assert main(["--completion", shell]) == 0
    assert expected in capsys.readouterr().out


@pytest.mark.parametrize(("shell", "expected"), [("bash", "complete -F _complete_duty"), ("zsh", "#compdef duty")])
def test_print_completion_script_for_current_shell(
    shell: str,
    expected: str,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Print the completion script of the shell detected through the `SHELL` environment variable."""
    monkeypatch.setenv("SHELL", f"/bin/{shell}")
    assert main(["--completion"]) == 0
    assert expected in capsys.readouterr().out


def test_print_completion_script_unsupported_shell(capsys: pytest.CaptureFixture) -> None:
    """Fail nicely when asked for the completion script of an unsupported shell."""
    assert main(["--completion", "ksh"]) == 1
    captured = capsys.readouterr()
    assert "'ksh'" in captured.err
    assert "PRs welcome" in captured.err
    assert not captured.out


def test_print_completion_script_undetectable_shell(
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fail nicely when the current shell cannot be detected."""
    monkeypatch.delenv("SHELL", raising=False)
    assert main(["--completion"]) == 1
    assert "SHELL" in capsys.readouterr().err


def test_complete_bash(capsys: pytest.CaptureFixture) -> None:
    """Complete duty names for Bash, without descriptions."""
    assert main(["-d", "tests/fixtures/documented.py", "--complete", "bash", "--", "duty"]) == 0
    words = capsys.readouterr().out.splitlines()
    assert "documented" in words
    assert "undocumented" in words
    assert "--completion" in words
    assert not any(":" in word for word in words)


def test_complete_zsh(capsys: pytest.CaptureFixture) -> None:
    """Complete duty names for Zsh, with descriptions."""
    assert main(["-d", "tests/fixtures/documented.py", "--complete", "zsh", "--", "duty"]) == 0
    words = capsys.readouterr().out.splitlines()
    assert "documented:Run a documented duty." in words
    # Duties without docstrings have no description.
    assert "undocumented" in words
    # Only the first line of a docstring is used as description.
    assert not any("must never appear" in word for word in words)


def test_complete_duty_parameters(capsys: pytest.CaptureFixture) -> None:
    """Complete parameters of the duty being typed."""
    assert main(["-d", "tests/fixtures/documented.py", "--complete", "zsh", "--", "duty", "documented"]) == 0
    assert "param=" in capsys.readouterr().out.splitlines()


def test_complete_defaults_to_bash(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Default to Bash when no shell is passed, for backward-compatibility with older completion scripts."""
    monkeypatch.setenv("SHELL", "/bin/zsh")
    assert main(["-d", "tests/fixtures/documented.py", "--complete", "--", "duty"]) == 0
    words = capsys.readouterr().out.splitlines()
    assert "documented" in words
    assert not any(":" in word for word in words)


def test_complete_without_duties_file(capsys: pytest.CaptureFixture) -> None:
    """Complete global options even when no duties file can be loaded."""
    assert main(["-d", "absent.py", "--complete", "bash", "--", "duty"]) == 0
    assert "--completion" in capsys.readouterr().out.splitlines()


def test_completion_without_duties_file(capsys: pytest.CaptureFixture) -> None:
    """Print and install completion scripts even when no duties file can be loaded."""
    assert main(["-d", "absent.py", "--completion", "bash"]) == 0
    assert "complete -F _complete_duty" in capsys.readouterr().out


def test_complete_unsupported_shell(capsys: pytest.CaptureFixture) -> None:
    """Fail nicely when asked to complete for an unsupported shell."""
    assert main(["--complete", "ksh", "--", "duty"]) == 1
    captured = capsys.readouterr()
    assert "'ksh'" in captured.err
    assert not captured.out


def test_install_completion_bash(bash_dir: Path, capsys: pytest.CaptureFixture) -> None:
    """Install Bash completions in the user completion directory."""
    assert main(["--install-completion", "bash"]) == 0
    install_path = bash_dir / "completions" / "duty"
    assert install_path.is_symlink()
    assert install_path.resolve() == Bash().script_path.resolve()
    assert str(install_path) in capsys.readouterr().out


def test_install_completion_zsh(zsh_dir: Path, capsys: pytest.CaptureFixture) -> None:
    """Install Zsh completions in the site-functions directory."""
    assert main(["--install-completion", "zsh"]) == 0
    install_path = zsh_dir / "_duty"
    assert install_path.is_symlink()
    assert install_path.resolve() == Zsh().script_path.resolve()
    assert str(install_path) in capsys.readouterr().out


def test_install_completion_for_current_shell(zsh_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Install completions for the shell detected through the `SHELL` environment variable."""
    monkeypatch.setenv("SHELL", "/bin/zsh")
    assert main(["--install-completion"]) == 0
    assert (zsh_dir / "_duty").is_symlink()


def test_install_completion_replaces_existing_file(zsh_dir: Path) -> None:
    """Overwrite previously installed completions, so that they are always up-to-date."""
    install_path = zsh_dir / "_duty"
    install_path.write_text("outdated completions")
    assert main(["--install-completion", "zsh"]) == 0
    assert install_path.is_symlink()
    assert install_path.resolve() == Zsh().script_path.resolve()


def test_install_completion_without_duties_file(zsh_dir: Path) -> None:
    """Install completions even when no duties file can be loaded."""
    assert main(["-d", "absent.py", "--install-completion", "zsh"]) == 0
    assert (zsh_dir / "_duty").is_symlink()


def test_install_completion_unsupported_shell(capsys: pytest.CaptureFixture) -> None:
    """Fail nicely when asked to install completions for an unsupported shell."""
    assert main(["--install-completion", "ksh"]) == 1
    assert "PRs welcome" in capsys.readouterr().err


def test_install_completion_without_bash_completion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail nicely when Bash's user completion directory does not exist."""
    monkeypatch.setenv("BASH_COMPLETION_USER_DIR", str(tmp_path / "absent"))
    assert main(["--install-completion", "bash"]) == 1


def test_install_completion_without_zsh(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Fail nicely when Zsh's site-functions directory does not exist."""
    monkeypatch.setattr(Zsh, "site_functions_dirs", (tmp_path / "absent",))
    assert main(["--install-completion", "zsh"]) == 1


def test_install_completion_permission_denied(
    zsh_dir: Path,  # noqa: ARG001
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tell users to retry with higher privileges when writing completions is not permitted."""

    def raise_permission_error(*args: object, **kwargs: object) -> None:  # noqa: ARG001
        raise PermissionError

    monkeypatch.setattr(Path, "symlink_to", raise_permission_error)
    assert main(["--install-completion", "zsh"]) == 1
    assert "sudo duty --install-completion=zsh" in capsys.readouterr().err


def test_install_completion_os_error(
    zsh_dir: Path,  # noqa: ARG001
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Report unexpected filesystem errors instead of crashing."""

    def raise_os_error(*args: object, **kwargs: object) -> None:  # noqa: ARG001
        raise OSError("symlinks are not supported")

    monkeypatch.setattr(Path, "symlink_to", raise_os_error)
    assert main(["--install-completion", "zsh"]) == 1
    assert "symlinks are not supported" in capsys.readouterr().err


def test_bash_default_install_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Respect `BASH_COMPLETION_USER_DIR`, then `XDG_DATA_HOME`, then the default user data directory."""
    monkeypatch.delenv("BASH_COMPLETION_USER_DIR", raising=False)
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    (tmp_path / "bash-completion").mkdir()
    assert Bash().install_path == tmp_path / "bash-completion" / "completions" / "duty"

    monkeypatch.setenv("BASH_COMPLETION_USER_DIR", str(tmp_path))
    assert Bash().install_path == tmp_path / "completions" / "duty"

    monkeypatch.delenv("BASH_COMPLETION_USER_DIR")
    monkeypatch.delenv("XDG_DATA_HOME")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    (tmp_path / ".local/share/bash-completion").mkdir(parents=True)
    assert Bash().install_path == tmp_path / ".local/share/bash-completion/completions/duty"


def test_completion_scripts_are_packaged() -> None:
    """Both completion scripts are shipped within the `duty` package."""
    for shell in (Bash(), Zsh()):
        assert shell.script_path.is_file()
