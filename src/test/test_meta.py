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


def test_die():
    with raises(SystemExit):
        meta.die("testing")


def test_get_channels(data, tmpdir):
    # Use mock recipe dir *with* a channels file:
    assert meta.get_channels(data) == ["foo", "bar", "local"]
    # Use mock recipe dir *without* a channels file:
    assert meta.get_channels(tmpdir) == ["local"]


def test_get_meta_json():
    with patch.object(meta, "api") as api:
        m = Mock()
        m.get_rendered_recipe_text.return_value = {
            "requirements": {
                "build": ["b >1.0,<2.0", "e =1.1"],
                "host": ["a >2.2", "f <3.3"],
                "run": ["h 4.4", "d 5.5.*"],
            },
            "test": {"requires": ["c >=6.6", "g"]},
        }
        m.get_section = lambda section: {
            "package": {"name": "pkgname", "version": "1.0.1"},
            "source": {"path": "/source/path"},
        }[section]
        solve0 = [m, None]
        solve1 = []
        api.render.return_value = [solve0, solve1]
        x = meta.json.loads(meta.get_meta_json(recipedir=data, channels=["c1", "c2"]))
        assert x == {
            "name": "pkgname",
            "packages": [
                "a >2.2",
                "b >1.0,<2.0",
                "c >=6.6",
                "d =5.5.*",
                "e =1.1",
                "f <3.3",
                "g",
                "h =4.4",
            ],
            "source": "/source/path",
            "version": "1.0.1",
        }
        m.clean.assert_called_once()
