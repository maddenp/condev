"""
Unit tests for hello.core module
"""

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name # for pytest fixtures

from pytest import fixture

from hello import core


@fixture
def hello():
    return "hello"


def test_hello(hello):
    assert core.hello() == hello


def test_main(capsys, hello):
    core.main()
    assert capsys.readouterr().out == f"{hello}, world\n"


def test_world():
    assert core.world() == "world"
