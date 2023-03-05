"""
Unit tests for devconda.meta module
"""

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name # for pytest fixtures

from pathlib import Path
from unittest.mock import Mock, patch

from pytest import fixture, raises

from devconda import meta


@fixture
def data():
    return Path(Path(__file__).parent, "data")


@fixture
def mockmeta():
    mm = Mock()
    mm.get_rendered_recipe_text.return_value = {
        "requirements": {
            "build": ["b >1.0,<2.0", "e =1.1"],
            "host": ["a >2.2", "f <3.3"],
            "run": ["h 4.4", "d 5.5.*"],
        },
        "test": {"requires": ["c >=6.6", "g"]},
    }
    mm.get_section = lambda section: {
        "package": {"name": "pkgname", "version": "1.0.1"},
        "source": {"path": "/source/path"},
    }[section]
    return mm


@fixture
def packages():
    return [
        "a >2.2",
        "b >1.0,<2.0",
        "c >=6.6",
        "d =5.5.*",
        "e =1.1",
        "f <3.3",
        "g",
        "h =4.4",
    ]


def test_die():
    with raises(SystemExit):
        meta.die("testing")


def test_get_channels(data, tmpdir):
    # Test case with a channels file:
    assert meta.get_channels(data) == ["foo", "bar", "local"]
    # Test case without a channels file:
    assert meta.get_channels(tmpdir) == ["local"]


def test_get_meta_json(data, mockmeta, packages):
    with patch.object(meta, "api") as api:
        solve0 = [mockmeta, None]
        solve1 = []
        api.render.return_value = [solve0, solve1]
        channels = ["c1", "c2"]
        x = meta.json.loads(meta.get_meta_json(recipedir=data, channels=channels))
        assert x == {
            "name": "pkgname",
            "packages": packages,
            "source": "/source/path",
            "version": "1.0.1",
        }
        api.render.assert_called_once_with(data, channels=channels, override_channels=True)
        mockmeta.clean.assert_called_once()


def test_get_name(mockmeta):
    assert meta.get_name(mockmeta) == "pkgname"


def test_get_packages(mockmeta, packages):
    assert meta.get_packages(mockmeta) == packages


def test_get_recipedir(tmpdir):
    # Test case where RECIPE_DIR is not set in environment:
    with patch.object(meta.os, "environ", new={}):
        with raises(SystemExit):
            meta.get_recipedir()
    # Test case where RECIPE_DIR is set but is not a directory:
    with patch.object(meta.os, "environ", new={"RECIPE_DIR": Path(tmpdir, "no-such-dir")}):
        with raises(SystemExit):
            meta.get_recipedir()
    # Test case where RECIPE_DIR is set and is a directory:
    with patch.object(meta.os, "environ", new={"RECIPE_DIR": Path(tmpdir)}):
        assert meta.get_recipedir() == tmpdir


def test_get_source(mockmeta):
    assert meta.get_source(mockmeta) == "/source/path"


def test_get_version(mockmeta):
    assert meta.get_version(mockmeta) == "1.0.1"
