"""Development tasks."""

from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from importlib.metadata import version as pkgversion
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

from duty import callables, duty

if TYPE_CHECKING:
    from duty.context import Context


PY_SRC_PATHS = (Path(_) for _ in ("src", "tests", "duties.py", "scripts"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)
CI = os.environ.get("CI", "0") in {"1", "true", "yes", ""}
WINDOWS = os.name == "nt"
PTY = not WINDOWS and not CI
MULTIRUN = os.environ.get("MULTIRUN", "0") == "1"


def pyprefix(title: str) -> str:  # noqa: D103
    if MULTIRUN:
        prefix = f"(python{sys.version_info.major}.{sys.version_info.minor})"
        return f"{prefix:14}{title}"
    return title


@contextmanager
def material_insiders() -> Iterator[bool]:  # noqa: D103
    if "+insiders" in pkgversion("mkdocs-material"):
        os.environ["MATERIAL_INSIDERS"] = "true"
        try:
            yield True
        finally:
            os.environ.pop("MATERIAL_INSIDERS")
    else:
        yield False


@duty
def changelog(ctx: Context, bump: str = "") -> None:
    """Update the changelog in-place with latest commits.

    Parameters:
        bump: Bump option passed to git-changelog.
    """
    ctx.run(callables.git_changelog.run(bump=bump or None), title="Updating changelog", command="git-changelog")


@duty(pre=["check_quality", "check_types", "check_docs", "check_dependencies", "check-api"])
def check(ctx: Context) -> None:  # noqa: ARG001
    """Check it all!"""


@duty
def check_quality(ctx: Context) -> None:
    """Check the code quality."""
    ctx.run(
        callables.ruff.check(*PY_SRC_LIST, config="config/ruff.toml"),
        title=pyprefix("Checking code quality"),
        command=f"ruff check --config config/ruff.toml {PY_SRC}",
    )


@duty
def check_dependencies(ctx: Context) -> None:
    """Check for vulnerabilities in dependencies."""
    # retrieve the list of dependencies
    requirements = ctx.run(
        ["uv", "pip", "freeze"],
        silent=True,
        allow_overrides=False,
    )

    ctx.run(
        callables.safety.check(requirements),
        title="Checking dependencies",
        command="uv pip freeze | safety check --stdin",
    )


@duty
def check_docs(ctx: Context) -> None:
    """Check if the documentation builds correctly."""
    Path("htmlcov").mkdir(parents=True, exist_ok=True)
    Path("htmlcov/index.html").touch(exist_ok=True)
    with material_insiders():
        ctx.run(
            callables.mkdocs.build(strict=True, verbose=True),
            title=pyprefix("Building documentation"),
            command="mkdocs build -vs",
        )


@duty
def check_types(ctx: Context) -> None:
    """Check that the code is correctly typed."""
    ctx.run(
        callables.mypy.run(*PY_SRC_LIST, config_file="config/mypy.ini"),
        title=pyprefix("Type-checking"),
        command=f"mypy --config-file config/mypy.ini {PY_SRC}",
    )


@duty
def check_api(ctx: Context) -> None:
    """Check for API breaking changes."""
    ctx.run(
        callables.griffe.check("duty", search=["src"], color=True),
        title="Checking for API breaking changes",
        command="griffe check -ssrc duty",
        nofail=True,
    )


@duty
def docs(ctx: Context, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Serve the documentation (localhost:8000).

    Parameters:
        host: The host to serve the docs from.
        port: The port to serve the docs on.
    """
    with material_insiders():
        ctx.run(
            callables.mkdocs.serve(dev_addr=f"{host}:{port}"),
            title="Serving documentation",
            capture=False,
        )


@duty
def docs_deploy(ctx: Context) -> None:
    """Deploy the documentation on GitHub pages."""
    os.environ["DEPLOY"] = "true"
    with material_insiders() as insiders:
        if not insiders:
            ctx.run(lambda: False, title="Not deploying docs without Material for MkDocs Insiders!")
        ctx.run(callables.mkdocs.gh_deploy(), title="Deploying documentation")


@duty
def format(ctx: Context) -> None:
    """Run formatting tools on the code."""
    ctx.run(
        callables.ruff.check(*PY_SRC_LIST, config="config/ruff.toml", fix_only=True, exit_zero=True),
        title="Auto-fixing code",
    )
    ctx.run(callables.ruff.format(*PY_SRC_LIST, config="config/ruff.toml"), title="Formatting code")


@duty
def build(ctx: Context) -> None:
    """Build source and wheel distributions."""
    ctx.run(
        callables.build.run(),
        title="Building source and wheel distributions",
        command="pyproject-build",
        pty=PTY,
    )


@duty
def publish(ctx: Context) -> None:
    """Publish source and wheel distributions to PyPI."""
    if not Path("dist").exists():
        ctx.run("false", title="No distribution files found")
    dists = [str(dist) for dist in Path("dist").iterdir()]
    ctx.run(
        callables.twine.upload(*dists, skip_existing=True),
        title="Publish source and wheel distributions to PyPI",
        command="twine upload -r pypi --skip-existing dist/*",
        pty=PTY,
    )


@duty(post=["build", "publish", "docs-deploy"])
def release(ctx: Context, version: str = "") -> None:
    """Release a new Python package.

    Parameters:
        version: The new version number to use.
    """
    if not (version := (version or input("> Version to release: ")).strip()):
        ctx.run("false", title="A version must be provided")
    ctx.run("git add pyproject.toml CHANGELOG.md", title="Staging files", pty=PTY)
    ctx.run(["git", "commit", "-m", f"chore: Prepare release {version}"], title="Committing changes", pty=PTY)
    ctx.run(f"git tag {version}", title="Tagging commit", pty=PTY)
    ctx.run("git push", title="Pushing commits", pty=False)
    ctx.run("git push --tags", title="Pushing tags", pty=False)


@duty(silent=True, aliases=["coverage"])
def cov(ctx: Context) -> None:
    """Report coverage as text and HTML."""
    ctx.run(callables.coverage.combine, nofail=True)
    ctx.run(callables.coverage.report(rcfile="config/coverage.ini"), capture=False)
    ctx.run(callables.coverage.html(rcfile="config/coverage.ini"))


@duty
def test(ctx: Context, match: str = "") -> None:
    """Run the test suite.

    Parameters:
        match: A pytest expression to filter selected tests.
    """
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    os.environ["COVERAGE_FILE"] = f".coverage.{py_version}"
    ctx.run(
        callables.pytest.run("-n", "auto", "tests", config_file="config/pytest.ini", select=match, color="yes"),
        title=pyprefix("Running tests"),
        command=f"pytest -c config/pytest.ini -n auto -k{match!r} --color=yes tests",
    )
