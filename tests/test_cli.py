"""Tests for the `cli` module."""

import pytest

from duty import cli


def test_no_duty(capsys):
    """
    Run no duties.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main([]) == 1
    captured = capsys.readouterr()
    assert "choose at least one duty" in captured.err


def test_show_help(capsys):
    """
    Show help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "duty" in captured.out


def test_select_duties():
    """Run a duty."""
    assert cli.main(["-d", "tests/fixtures/basic.py", "hello"]) == 0


def test_unknown_duty():
    """Don't run an unknown duty."""
    assert cli.main(["-d", "tests/fixtures/basic.py", "byebye"]) == 1


def test_incorrect_arguments():
    """Use incorrect arguments."""
    assert cli.main(["-d", "tests/fixtures/basic.py", "hello=1"]) == 1


# we use 300 because it's slightly above the valid maximum 255
@pytest.mark.parametrize("code", range(-100, 300, 7))  # noqa: WPS432 (magic number 300)
def test_duty_failure(code):
    """
    Check exit code.

    Arguments:
        code: Code to match.
    """
    assert cli.main(["-d", "tests/fixtures/code.py", "exit_with", f"code={code}"]) == code


def test_multiple_duties(capsys):
    """
    Run multiple duties.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/multiple.py", "first_duty", "second_duty"]) == 0
    captured = capsys.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out


def test_duty_arguments(capsys):  # noqa: WPS218 (too many assert statements)
    """
    Run duty with arguments.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/arguments.py", "say_hello", "cat=fabric"]) == 0
    captured = capsys.readouterr()
    assert "cat fabric" in captured.out
    assert "dog dog" in captured.out

    assert cli.main(["-d", "tests/fixtures/arguments.py", "say_hello", "dog=paramiko", "cat=invoke"]) == 0
    captured = capsys.readouterr()
    assert "cat invoke" in captured.out
    assert "dog paramiko" in captured.out


def test_list_duties(capsys):
    """
    List duties.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/list.py", "-l"]) == 0
    captured = capsys.readouterr()
    assert "Tong..." in captured.out
    assert "DEUM!" in captured.out
