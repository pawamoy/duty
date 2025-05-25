"""Bash completion tests."""

import os
import subprocess
from pathlib import Path

import pytest

from duty import cli
from duty.completion import Bash
from tests.test_completion.utils import needs_platform, needs_shell

completion_test_cases = (
    ("tests/fixtures/basic.py", "", "hello\n--"),
    ("tests/fixtures/multiple.py", "", "first-duty\nfirst_duty\nsecond-duty\nsecond_duty\n--"),
    ("tests/fixtures/code.py", "exit", "exit-with\nexit_with\n--"),
    ("tests/fixtures/code.py", "exit-with", "exit-with\nexit_with\ncode=\n--"),
)
parametrize_completions = pytest.mark.parametrize(
    ("duties_file", "partial", "expected"),
    completion_test_cases,
    ids=range(len(completion_test_cases)),
)


def assert_completion_loaded() -> None:
    """Asserts that bash has completions for duty."""
    result = subprocess.run(["/bin/bash", "-c", "complete -p duty"], capture_output=True, check=True, encoding="utf-8")  # noqa: S603
    assert "complete -o default -F _complete_duty duty" in result.stdout
    # Cleanup
    Bash().install_path.unlink(missing_ok=True)


@needs_shell(Bash)
@needs_platform("linux", "darwin")
def test_install(capsys: pytest.CaptureFixture) -> None:
    """Test bash completion installation."""
    assert cli.main(["--install-completion", "bash"]) == 0
    captured = capsys.readouterr()
    assert "Bash completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Bash().install_path.unlink(missing_ok=True)


@needs_shell(Bash)
@needs_platform("linux", "darwin")
def test_install_no_param(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test bash completion installation with no shell parameter provided."""
    monkeypatch.setenv("SHELL", "/bin/bash")
    assert cli.main(["--install-completion"]) == 0
    captured = capsys.readouterr()
    assert "Bash completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Bash().install_path.unlink(missing_ok=True)


@needs_shell(Bash)
@needs_platform("linux", "darwin")
def test_install_path_exists(capsys: pytest.CaptureFixture) -> None:
    """Test bash completion installation with symlink/file already present."""
    Bash().install_path.touch()
    assert cli.main(["--install-completion", "bash"]) == 0
    captured = capsys.readouterr()
    assert "Bash completions successfully symlinked" in captured.out
    assert_completion_loaded()
    # Cleanup
    Bash().install_path.unlink(missing_ok=True)


def test_completion(capsys: pytest.CaptureFixture) -> None:
    """Test printing out bash completion script."""
    assert cli.main(["--completion", "bash"]) == 0
    captured = capsys.readouterr()
    assert "complete -F _complete_duty -o default duty" in captured.out


def test_completion_no_param(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test printing out bash completion script with no shell parameter provided."""
    monkeypatch.setenv("SHELL", "/bin/bash")
    assert cli.main(["--completion"]) == 0
    captured = capsys.readouterr()
    assert "complete -F _complete_duty" in captured.out


@parametrize_completions
def test_complete(duties_file: str, partial: str, expected: str, capsys: pytest.CaptureFixture) -> None:
    """Test bash completion."""
    assert cli.main(["-d", duties_file, "--complete", "bash", "--", "duty", partial]) == 0
    captured = capsys.readouterr()
    assert expected in captured.out


@parametrize_completions
def test_complete_no_param(
    duties_file: str,
    partial: str,
    expected: str,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test bash completion with no shell parameter provided.

    `--complete` with no shell parameter should always default to bash for backward compatibility with 1.5.0 version.
    """
    monkeypatch.setenv("SHELL", "anything")
    assert cli.main(["-d", duties_file, "--complete", "--", "duty", partial]) == 0
    captured = capsys.readouterr()
    assert expected in captured.out


@parametrize_completions
@needs_shell(Bash)
@needs_platform("linux", "darwin")
def test_completion_function(duties_file: str, partial: str, expected: str) -> None:
    """Test bash `_complete_duty` function."""
    # TODO: Temporary hack, as for now completions don't respect the `-d` flag - to be fixed in another PR.
    duties_path = Path() / "duties.py"
    duties_path.unlink(missing_ok=True)
    duties_path.symlink_to(duties_file)

    commands = (
        f"source {Bash().completion_script_path}",
        "_complete_duty",
        'echo "${COMPREPLY[@]}"',
    )
    comp_words = f"duty {partial}"
    result = subprocess.run(  # noqa: S603
        ["/bin/bash", "-c", " && ".join(commands)],
        capture_output=True,
        check=True,
        encoding="utf-8",
        env={**os.environ, "COMP_WORDS": comp_words},
    )
    # In this test case, output is a bash array, so we expect spaces instead of newlines.
    assert expected.replace("\n", " ") in result.stdout
    # Cleanup
    Bash().install_path.unlink(missing_ok=True)
