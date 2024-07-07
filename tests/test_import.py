"""Test sungen."""

import sungen


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(sungen.__name__, str)
