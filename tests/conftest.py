"""Configuration for the pytest test suite."""

import pytest

from duty import logic


@pytest.fixture(autouse=True)
def _clear_duties():
    """Clear duties before every test."""
    logic.duties.clear()
    logic.duties_aliases.clear()
