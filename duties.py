"""Development tasks."""

import os
from pathlib import Path
from shutil import which

from duty import duty

PY_SRC_PATHS = (Path(_) for _ in ("src", "scripts", "tests", "duties.py"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)
TESTING = os.environ.get("TESTING", "0") in {"1", "true"}
CI = os.environ.get("CI", "0") in {"1", "true"}
WINDOWS = os.name == "nt"
PTY = not WINDOWS


@duty
def changelog(ctx):
    """
    Update the changelog in-place with latest commits.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(
        [
            "python",
            "scripts/update_changelog.py",
            "CHANGELOG.md",
            "<!-- insertion marker -->",
            r"^## \[v?(?P<version>[^\]]+)",
        ],
        title="Updating changelog",
        pty=PTY,
    )


@duty(pre=["check_code_quality", "check_types", "check_docs", "check_dependencies"])
def check(ctx):  # noqa: W0613 (no use for the context argument)
    """
    Check it all!

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """  # noqa: D400 (exclamation mark is funnier)


@duty
def check_code_quality(ctx):
    """
    Check the code quality.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(["flakehell", "lint", *PY_SRC_LIST], title="Checking code quality", pty=PTY)


@duty
def check_dependencies(ctx):
    """
    Check for vulnerabilities in dependencies.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    safety = "safety" if which("safety") else "pipx run safety"
    ctx.run(
        "poetry export -f requirements.txt --without-hashes | " f"{safety} check --stdin --full-report",
        title="Checking dependencies",
        pty=PTY,
    )


@duty
def check_docs(ctx):
    """
    Check if the documentation builds correctly.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(["mkdocs", "build", "-s"], title="Building documentation", pty=PTY)


@duty
def check_types(ctx):
    """
    Check that the code is correctly typed.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(["mypy", "--config-file", "config/mypy.ini", *PY_SRC_LIST], title="Type-checking", pty=PTY)


@duty(silent=True)
def clean(ctx):
    """
    Delete temporary files.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run("rm -rf .coverage*")
    ctx.run("rm -rf .mypy_cache")
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf pip-wheel-metadata")
    ctx.run("rm -rf site")
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf")
    ctx.run("find . -name '*.rej' -delete")


@duty
def docs_regen(ctx):
    """
    Regenerate some documentation pages.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(["python", "scripts/regen_docs.py"], title="Regenerating docfiles", pty=PTY)


# @duty(docs_regen)
@duty
def docs(ctx):
    """
    Build the documentation locally.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(["mkdocs", "build"])


# @duty(docs_regen)
@duty
def docs_serve(ctx, host="127.0.0.1", port=8000):
    """
    Serve the documentation (localhost:8000).

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
        host: The host to serve the docs from.
        port: The port to serve the docs on.
    """
    ctx.run(["mkdocs", "serve", "-a", f"{host}:{port}"])


# @duty(docs_regen)
@duty
def docs_deploy(ctx):
    """
    Deploy the documentation on GitHub pages.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run("mkdocs gh-deploy")


@duty
def format(ctx):  # noqa: W0622 (we don't mind shadowing the format builtin)
    """
    Run formatting tools on the code.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run(
        ["autoflake", "-ir", "--exclude", "tests/fixtures", "--remove-all-unused-imports", *PY_SRC_LIST],
        title="Removing unused imports",
        pty=PTY,
    )
    ctx.run(["isort", "-y", "-rc", *PY_SRC_LIST], title="Ordering imports", pty=PTY)
    ctx.run(["black", *PY_SRC_LIST], title="Formatting code", pty=PTY)


@duty
def release(ctx, version):
    """
    Release a new Python package.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
        version: The new version number to use.
    """
    ctx.run(f"poetry version {version}", title="Bumping version in pyproject.toml", pty=PTY)
    ctx.run("git add pyproject.toml CHANGELOG.md", title="Staging files", pty=PTY)
    ctx.run(f"git commit -m 'chore: Prepare release {version}'", title="Committing changes", pty=PTY)
    ctx.run(f"git tag {version}", title="Tagging commit", pty=PTY)
    if not TESTING:
        ctx.run("git push", title="Pushing commits", pty=False)
        ctx.run("git push --tags", title="Pushing tags", pty=False)
        ctx.run("poetry build", title="Building dist/wheel", pty=PTY)
        ctx.run("poetry publish", title="Publishing version", pty=PTY)
        ctx.run("poetry run mkdocs gh-deploy", title="Deploying docs", pty=PTY)


@duty
def combine(ctx):
    """
    Combine coverage data from multiple runs.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run("coverage combine --rcfile=config/coverage.ini")


@duty
def coverage(ctx):
    """
    Report coverage as text and HTML.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
    """
    ctx.run("coverage report --rcfile=config/coverage.ini")
    ctx.run("coverage html --rcfile=config/coverage.ini")


@duty(pre=[duty(lambda ctx: ctx.run("rm -f .coverage", silent=True))])
def test(ctx, match=""):
    """
    Run the test suite.

    Arguments:
        ctx: The [context][duties.logic.Context] instance (passed automatically).
        match: A pytest expression to filter selected tests.
    """
    ctx.run(
        ["pytest", "-c", "config/pytest.ini", "-n", "auto", "-k", match, *PY_SRC_LIST],
        title="Running tests",
        pty=PTY,
    )
