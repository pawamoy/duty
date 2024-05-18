"""Module containing callables for many tools."""

from __future__ import annotations

from failprint.lazy import lazy

from duty.tools._autoflake import autoflake
from duty.tools._base import LazyStderr, LazyStdout, Tool
from duty.tools._black import black
from duty.tools._blacken_docs import blacken_docs
from duty.tools._build import build
from duty.tools._coverage import coverage
from duty.tools._flake8 import flake8
from duty.tools._git_changelog import git_changelog
from duty.tools._griffe import griffe
from duty.tools._interrogate import interrogate
from duty.tools._isort import isort
from duty.tools._mkdocs import mkdocs
from duty.tools._mypy import mypy
from duty.tools._pytest import pytest
from duty.tools._ruff import ruff
from duty.tools._safety import safety
from duty.tools._ssort import ssort
from duty.tools._twine import twine

__all__ = [
    "Tool",
    "LazyStdout",
    "LazyStderr",
    "lazy",
    "autoflake",
    "black",
    "blacken_docs",
    "build",
    "coverage",
    "flake8",
    "git_changelog",
    "griffe",
    "interrogate",
    "isort",
    "mkdocs",
    "mypy",
    "pytest",
    "ruff",
    "safety",
    "ssort",
    "twine",
]
