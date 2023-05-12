"""
Unit tests for condev.meta module
"""

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name # for pytest fixtures

from pathlib import Path
from unittest.mock import Mock, patch

from pytest import fixture, raises

from condev import meta


@fixture
def data():
    return Path(Path(__file__).parent, "data")


@fixture
def meta_json(packages):
    return {
        "build": "abcd_88",
        "buildnum": 88,
        "name": "pkgname",
        "packages": packages,
        "version": "1.0.1",
    }


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
        "build": {"number": 88},
        "package": {"name": "pkgname", "version": "1.0.1"},
    }[section]
    mm.info_index = lambda: {"build": "abcd_88"}
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


@fixture
def solves(mockmeta):
    return [[mockmeta, None], []]


def test_die():
    with raises(SystemExit):
        meta.die("testing")


def test_get_build(mockmeta):
    assert meta.get_build(mockmeta) == "abcd_88"


def test_get_buildnum(mockmeta):
    assert meta.get_buildnum(mockmeta) == 88


def test_get_channels(data, tmpdir):
    # Test case with a channels file:
    assert meta.get_channels(data) == ["foo", "bar", "local"]
    # Test case without a channels file:
    assert meta.get_channels(tmpdir) == ["local"]


def test_get_meta_json(data, meta_json, mockmeta, solves):
    with patch.object(meta, "api") as api:
        api.render.return_value = solves
        channels = ["c1", "c2"]
        x = meta.json.loads(meta.get_meta_json(recipedir=data, channels=channels))
        assert x == meta_json
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
    with patch.object(meta.os, "environ", new={"RECIPE_DIR": tmpdir}):
        assert meta.get_recipedir() == tmpdir


def test_get_version(mockmeta):
    assert meta.get_version(mockmeta) == "1.0.1"


def test_main(meta_json, solves, tmpdir):
    with patch.object(meta.os, "environ", new={"RECIPE_DIR": tmpdir}):
        with patch.object(meta, "api") as api:
            api.render.return_value = solves
            meta.main()
            api.render.assert_called_once()
    meta_json_path = Path(tmpdir, "meta.json")
    assert meta_json_path.is_file()
    with open(meta_json_path, "r", encoding="utf-8") as f:
        assert meta.json.load(f) == meta_json
