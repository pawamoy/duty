"""Shell completion testing utilities."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, Literal

import pytest

if TYPE_CHECKING:
    from duty.completion import Shell


def needs_platform(*platforms: Literal["linux", "darwin", "win32"]) -> pytest.MarkDecorator:
    """Skip test if the current platform doesn't match one of `platforms`."""
    return pytest.mark.skipif(
        not sys.platform not in platforms,
        reason=f"Test requires one of these platforms: {', '.join(platforms)}",
    )


def needs_shell(shell: type[Shell]) -> pytest.MarkDecorator:
    """Skip test if the current shell doesn't match `shell`."""
    shell_environ = os.environ.get("SHELL")
    return pytest.mark.skipif(
        not (shell_environ and os.path.basename(shell_environ) == shell.name),
        reason=f"Test requires {shell.name} shell and SHELL environment variable set",
    )


needs_isolated_container = pytest.mark.skipif(
    not os.getenv("_DUTY_ISOLATED_TEST_CONTAINER"),
    reason="Test requires to be run in an isolated container",
)
