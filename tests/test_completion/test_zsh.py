"""Zsh completion tests."""

from pathlib import Path

import pytest

from duty import cli
from duty.completion import Zsh
from tests.test_completion.utils import needs_platform, needs_shell

completion_test_cases = (
    ("tests/fixtures/basic.py", "", "TODO"),
    ("tests/fixtures/multiple.py", "", "TODO"),
    ("tests/fixtures/code.py", "exit", "TODO"),
    ("tests/fixtures/code.py", "exit-with", "TODO"),
)
parametrize_completions = pytest.mark.parametrize(
    ("duties_file", "partial", "expected"),
    completion_test_cases,
    ids=range(len(completion_test_cases)),
)


def assert_completion_loaded() -> None:
    """Asserts that zsh has completions for duty."""
    # TODO

    # Cleanup
    Zsh().install_path.unlink(missing_ok=True)


@needs_shell(Zsh)
@needs_platform("linux", "darwin")
def test_install(capsys: pytest.CaptureFixture) -> None:
    """Test zsh completion installation."""
    assert cli.main(["--install-completion", "zsh"]) == 0
    captured = capsys.readouterr()
    assert "Zsh completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Zsh().install_path.unlink(missing_ok=True)


@needs_shell(Zsh)
@needs_platform("linux", "darwin")
def test_install_no_param(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test zsh completion installation with no shell parameter provided."""
    monkeypatch.setenv("SHELL", "/bin/zsh")
    assert cli.main(["--install-completion"]) == 0
    captured = capsys.readouterr()
    assert "Zsh completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Zsh().install_path.unlink(missing_ok=True)


@needs_shell(Zsh)
@needs_platform("linux", "darwin")
def test_install_path_exists(capsys: pytest.CaptureFixture) -> None:
    """Test zsh completion installation with symlink/file already present."""
    Zsh().install_path.touch()
    assert cli.main(["--install-completion", "zsh"]) == 0
    captured = capsys.readouterr()
    assert "Zsh completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Zsh().install_path.unlink(missing_ok=True)


def test_completion(capsys: pytest.CaptureFixture) -> None:
    """Test printing out zsh completion script."""
    assert cli.main(["--completion", "zsh"]) == 0
    captured = capsys.readouterr()
    assert "_describe 'duty' subcmds" in captured.out


def test_completion_no_param(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test printing out zsh completion script with no shell parameter provided."""
    monkeypatch.setenv("SHELL", "/bin/zsh")
    assert cli.main(["--completion"]) == 0
    captured = capsys.readouterr()
    assert "_describe 'duty' subcmds" in captured.out


@parametrize_completions
def test_complete(duties_file: str, partial: str, expected: str, capsys: pytest.CaptureFixture) -> None:
    """Test zsh completion."""
    assert cli.main(["-d", duties_file, "--complete", "zsh", "--", "duty", partial]) == 0
    captured = capsys.readouterr()
    assert expected in captured.out


@parametrize_completions
@needs_shell(Zsh)
@needs_platform("linux", "darwin")
def test_completion_function(duties_file: str, partial: str, expected: str) -> None:
    """Test zsh `_complete_duty` function."""
    # TODO: Temporary hack, as for now completions don't respect the `-d` flag - to be fixed in another PR.
    duties_path = Path() / "duties.py"
    duties_path.unlink(missing_ok=True)
    duties_path.symlink_to(duties_file)
    # TODO

    # Cleanup
    Zsh().install_path.unlink(missing_ok=True)
