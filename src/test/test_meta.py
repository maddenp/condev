"""
Unit tests for devconda.meta module
"""

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name # for pytest fixtures

from pathlib import Path

from pytest import fixture, raises

from devconda import meta


@fixture
def data():
    return Path(Path(__file__).parent, "data")


def test_die():
    with raises(SystemExit):
        meta.die("testing")


def test_get_channels(data, tmpdir):
    # Use mock recipe dir *with* a channels file:
    assert meta.get_channels(data) == ["foo", "bar", "local"]
    # Use mock recipe dir *without* a channels file:
    assert meta.get_channels(tmpdir) == ["local"]
