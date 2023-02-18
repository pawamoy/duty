"""Callable for [Safety](https://github.com/pyupio/safety)."""

from __future__ import annotations

import importlib
import sys
from io import StringIO
from typing import Sequence, cast

from duty.callables import lazy

# TODO: remove once support for Python 3.7 is dropped
if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


@lazy("safety.check")
def check(
    requirements: str | Sequence[str],
    *,
    ignore_vulns: dict[str, str] | None = None,
    formatter: Literal["json", "bare", "text"] = "text",
    full_report: bool = True,
) -> bool:
    """Run the safety check command.

    This function makes sure we load the original, unpatched version of safety.

    Parameters:
        requirements: Python "requirements" (list of pinned dependencies).
        ignore_vulns: Vulnerabilities to ignore.
        formatter: Report format.
        full_report: Whether to output a full report.

    Returns:
        Success/failure.
    """
    # set default parameter values
    ignore_vulns = ignore_vulns or {}

    # undo possible patching
    # see https://github.com/pyupio/safety/issues/348
    for module in sys.modules:
        if module.startswith("safety.") or module == "safety":
            del sys.modules[module]

    importlib.invalidate_caches()

    # reload original, unpatched safety
    from safety.formatter import SafetyFormatter
    from safety.safety import calculate_remediations, check
    from safety.util import read_requirements

    # check using safety as a library
    if isinstance(requirements, (list, tuple, set)):
        requirements = "\n".join(requirements)
    packages = list(read_requirements(StringIO(cast(str, requirements))))
    vulns, db_full = check(packages=packages, ignore_vulns=ignore_vulns)
    remediations = calculate_remediations(vulns, db_full)
    output_report = SafetyFormatter(formatter).render_vulnerabilities(
        announcements=[],
        vulnerabilities=vulns,
        remediations=remediations,
        full=full_report,
        packages=packages,
    )

    # print report, return status
    if vulns:
        print(output_report)  # noqa: T201
        return False
    return True
