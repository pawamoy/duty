# YORE: Bump 2: Remove file.

from __future__ import annotations

import importlib
import sys
from io import StringIO
from typing import TYPE_CHECKING, Literal, cast

from failprint import lazy

if TYPE_CHECKING:
    from collections.abc import Sequence


@lazy(name="safety.check")
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
    from safety.formatter import SafetyFormatter  # noqa: PLC0415
    from safety.safety import calculate_remediations, check  # noqa: PLC0415
    from safety.util import read_requirements  # noqa: PLC0415

    # check using safety as a library
    if isinstance(requirements, (list, tuple, set)):
        requirements = "\n".join(requirements)
    packages = list(read_requirements(StringIO(cast("str", requirements))))

    # TODO: Safety 3 support, merge once support for v2 is dropped.
    check_kwargs = {"packages": packages, "ignore_vulns": ignore_vulns}
    try:
        from safety.auth.cli_utils import build_client_session  # noqa: PLC0415

        client_session, _ = build_client_session()
        check_kwargs["session"] = client_session
    except ImportError:
        pass

    vulns, db_full = check(**check_kwargs)
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
