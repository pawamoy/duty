from __future__ import annotations

import importlib
import sys
from io import StringIO
from typing import Sequence, cast, Literal


def check(
    requirements: str | Sequence[str],
    safety_ignore_vulns: dict[str, str] = None,
    safety_formatter: Literal["json", "bare", "text"] = "text",
    safety_full_report: bool = True,
):
    # set default parameter values
    safety_ignore_vulns = safety_ignore_vulns or {}

    # undo possible patching
    # see https://github.com/pyupio/safety/issues/348
    for module in sys.modules:  # noqa: WPS528
        if module.startswith("safety.") or module == "safety":
            del sys.modules[module]  # noqa: WPS420

    importlib.invalidate_caches()

    # reload original, unpatched safety
    from safety.formatter import SafetyFormatter
    from safety.safety import calculate_remediations
    from safety.safety import check
    from safety.util import read_requirements

    # check using safety as a library
    if isinstance(requirements, (list, tuple, set)):
        requirements = "\n".join(requirements)
    packages = list(read_requirements(StringIO(cast(str, requirements))))
    vulns, db_full = check(packages=packages, ignore_vulns=safety_ignore_vulns)
    remediations = calculate_remediations(vulns, db_full)
    output_report = SafetyFormatter(safety_formatter).render_vulnerabilities(
        announcements=[],
        vulnerabilities=vulns,
        remediations=remediations,
        full=safety_full_report,
        packages=packages,
    )

    # print report, return status
    if vulns:
        print(output_report)
        return False
    return True
