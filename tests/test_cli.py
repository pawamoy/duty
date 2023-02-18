"""Tests for the `cli` module."""

import pytest

from duty import cli


def test_no_duty(capsys):
    """Run no duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main([]) == 1
    captured = capsys.readouterr()
    assert "choose at least one duty" in captured.err


def test_show_help(capsys):
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-h"]) == 0
    captured = capsys.readouterr()
    assert "duty" in captured.out


def test_show_help_for_given_duties(capsys):
    """Show help for given duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/basic.py", "-h", "hello"]) == 0
    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_show_help_unknown_duty(capsys):
    """Show help for an unknown duty.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/basic.py", "-h", "not-here"]) == 0
    captured = capsys.readouterr()
    assert "Unknown duty" in captured.out


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
@pytest.mark.parametrize("code", range(-100, 300, 7))
def test_duty_failure(code):
    """Check exit code.

    Parameters:
        code: Code to match.
    """
    assert cli.main(["-d", "tests/fixtures/code.py", "exit_with", f"code={code}"]) == code


def test_multiple_duties(capsys):
    """Run multiple duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/multiple.py", "first_duty", "second_duty"]) == 0
    captured = capsys.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out


def test_duty_arguments(capsys):
    """Run duty with arguments.

    Parameters:
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
    """List duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/list.py", "-l"]) == 0
    captured = capsys.readouterr()
    assert "Tong..." in captured.out
    assert "DEUM!" in captured.out


def test_global_options():
    """Test global options."""
    assert cli.main(["-d", "tests/fixtures/code.py", "-z", "exit_with", "1"]) == 0


def test_global_and_local_options():
    """Test global and local options."""
    assert cli.main(["-d", "tests/fixtures/code.py", "-z", "exit_with", "-Z", "1"]) == 1


def test_options_precedence():
    """Test options precedence."""
    # @duty(nofail=True) is overridden by ctx.run(nofail=False)
    assert cli.main(["-d", "tests/fixtures/precedence.py", "precedence"]) == 1

    # ctx.run(nofail=False) is overridden by local option -z
    assert cli.main(["-d", "tests/fixtures/precedence.py", "precedence", "-z"]) == 0

    # ctx.run(nofail=False) is overridden by global option -z
    assert cli.main(["-d", "tests/fixtures/precedence.py", "-z", "precedence"]) == 0

    # global option -z is overridden by local option -z
    assert cli.main(["-d", "tests/fixtures/precedence.py", "-z", "precedence", "-Z"]) == 1


# test options precedence (CLI option, env var, ctx.run, @duty
# test positional arguments
# test extra keyword arguments
# test complete (global options + local options + multi duties + positional args + keyword args + extra keyword args)


@pytest.mark.parametrize(
    ("param", "expected"),
    [
        ("", 1),
        ("n", 1),
        ("N", 1),
        ("no", 1),
        ("NO", 1),
        ("false", 1),
        ("FALSE", 1),
        ("off", 1),
        ("OFF", 1),
        ("zero=", 1),
        ("zero=0", 1),
        ("zero=n", 1),
        ("zero=N", 1),
        ("zero=no", 1),
        ("zero=NO", 1),
        ("zero=false", 1),
        ("zero=FALSE", 1),
        ("zero=off", 1),
        ("zero=OFF", 1),
        ("y", 0),
        ("Y", 0),
        ("yes", 0),
        ("YES", 0),
        ("on", 0),
        ("ON", 0),
        ("true", 0),
        ("TRUE", 0),
        ("anything else", 0),
        ("-1", 0),
        ("1", 0),
        ("zero=y", 0),
        ("zero=Y", 0),
        ("zero=yes", 0),
        ("zero=YES", 0),
        ("zero=on", 0),
        ("zero=ON", 0),
        ("zero=true", 0),
        ("zero=TRUE", 0),
        ("zero=anything else", 0),
        ("zero=-1", 0),
        ("zero=1", 0),
    ],
)
def test_cast_bool_parameter(param, expected):
    """Test parameters casting as boolean.

    Parameters:
        param: Pytest parametrization fixture.
        expected: Pytest parametrization fixture.
    """
    assert cli.main(["-d", "tests/fixtures/booleans.py", "boolean", param]) == expected


def test_invalid_params(capsys):
    """Check that invalid parameters are early and correctly detected.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert cli.main(["-d", "tests/fixtures/booleans.py", "boolean", "zore=off"]) == 1
    captured = capsys.readouterr()
    assert "unexpected keyword argument 'zore'" in captured.err

    assert cli.main(["-d", "tests/fixtures/code.py", "exit_with"]) == 1
    captured = capsys.readouterr()
    assert "missing 1 required positional argument: 'code'" in captured.err
