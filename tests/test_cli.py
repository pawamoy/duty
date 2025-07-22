"""Tests for the CLI."""

from __future__ import annotations

import pytest

from duty import main
from duty._internal import debug


def test_no_duty(capsys: pytest.CaptureFixture) -> None:
    """Run no duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main([]) == 1
    captured = capsys.readouterr()
    assert "Available duties" in captured.out


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main(["-h"]) == 0
    captured = capsys.readouterr()
    assert "duty" in captured.out


def test_show_help_for_given_duties(capsys: pytest.CaptureFixture) -> None:
    """Show help for given duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/basic.py", "-h", "hello"]) == 0
    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_show_help_unknown_duty(capsys: pytest.CaptureFixture) -> None:
    """Show help for an unknown duty.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/basic.py", "-h", "not-here"]) == 0
    captured = capsys.readouterr()
    assert "Unknown duty" in captured.out


def test_select_duties() -> None:
    """Run a duty."""
    assert main(["-d", "tests/fixtures/basic.py", "hello"]) == 0


def test_unknown_duty() -> None:
    """Don't run an unknown duty."""
    assert main(["-d", "tests/fixtures/basic.py", "byebye"]) == 1


def test_incorrect_arguments() -> None:
    """Use incorrect arguments."""
    assert main(["-d", "tests/fixtures/basic.py", "hello=1"]) == 1


# we use 300 because it's slightly above the valid maximum 255
@pytest.mark.parametrize("code", range(-100, 300, 7))
def test_duty_failure(code: int) -> None:
    """Check exit code.

    Parameters:
        code: Code to match.
    """
    assert main(["-d", "tests/fixtures/code.py", "exit_with", f"code={code}"]) == code


def test_multiple_duties(capfd: pytest.CaptureFixture) -> None:
    """Run multiple duties.

    Parameters:
        capfd: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/multiple.py", "first_duty", "second_duty"]) == 0
    captured = capfd.readouterr()
    assert "first" in captured.out
    assert "second" in captured.out


def test_duty_arguments(capfd: pytest.CaptureFixture) -> None:
    """Run duty with arguments.

    Parameters:
        capfd: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/arguments.py", "say_hello", "cat=fabric"]) == 0
    captured = capfd.readouterr()
    assert "cat fabric" in captured.out
    assert "dog dog" in captured.out

    assert main(["-d", "tests/fixtures/arguments.py", "say_hello", "dog=paramiko", "cat=invoke"]) == 0
    captured = capfd.readouterr()
    assert "cat invoke" in captured.out
    assert "dog paramiko" in captured.out


def test_list_duties(capsys: pytest.CaptureFixture) -> None:
    """List duties.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/list.py", "-l"]) == 0
    captured = capsys.readouterr()
    assert "Tong..." in captured.out
    assert "DEUM!" in captured.out


def test_global_options() -> None:
    """Test global options."""
    assert main(["-d", "tests/fixtures/code.py", "-z", "exit_with", "1"]) == 0


def test_global_and_local_options() -> None:
    """Test global and local options."""
    assert main(["-d", "tests/fixtures/code.py", "-z", "exit_with", "-Z", "1"]) == 1


def test_options_precedence() -> None:
    """Test options precedence."""
    # @duty(nofail=True) is overridden by ctx.run(nofail=False)
    assert main(["-d", "tests/fixtures/precedence.py", "precedence"]) == 1

    # ctx.run(nofail=False) is overridden by local option -z
    assert main(["-d", "tests/fixtures/precedence.py", "precedence", "-z"]) == 0

    # ctx.run(nofail=False) is overridden by global option -z
    assert main(["-d", "tests/fixtures/precedence.py", "-z", "precedence"]) == 0

    # global option -z is overridden by local option -z
    assert main(["-d", "tests/fixtures/precedence.py", "-z", "precedence", "-Z"]) == 1


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
def test_cast_bool_parameter(param: str, expected: int) -> None:
    """Test parameters casting as boolean.

    Parameters:
        param: Pytest parametrization fixture.
        expected: Pytest parametrization fixture.
    """
    assert main(["-d", "tests/fixtures/booleans.py", "boolean", param]) == expected


def test_invalid_params(capsys: pytest.CaptureFixture) -> None:
    """Check that invalid parameters are early and correctly detected.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    assert main(["-d", "tests/fixtures/booleans.py", "boolean", "zore=off"]) == 1
    captured = capsys.readouterr()
    assert "unexpected keyword argument 'zore'" in captured.err

    assert main(["-d", "tests/fixtures/code.py", "exit_with"]) == 1
    captured = capsys.readouterr()
    assert "missing 1 required positional argument: 'code'" in captured.err


def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["-V"])
    captured = capsys.readouterr()
    assert debug._get_version() in captured.out


def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured
