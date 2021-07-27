from unittest import mock
import fakeredis
import pytest

from colors_redis import colorsRedis


def mock_connect(self):
    self.db = fakeredis.FakeRedis()


class MockColor:
    def __init__(self, color_name, r, g, b):
        self.colorName = color_name
        self.r = r
        self.g = g
        self.b = b


@mock.patch.object(colorsRedis, 'connect', mock_connect)
def test_new_db_is_empty():
    cdb = colorsRedis()
    assert cdb.numColors() == 0


@mock.patch.object(colorsRedis, 'connect', mock_connect)
def test_item_is_remembered():
    cdb = colorsRedis()
    color = MockColor("Strong_blue", 0, 0, 255)
    cdb.register_color(color)
    assert cdb.numColors() == 1
    assert cdb.is_color(color)

@mock.patch.object(colorsRedis, 'connect', mock_connect)
def test_first_item_not_overwritten():
    cdb = colorsRedis()
    color1 = MockColor("Strong_blue", 0, 0, 255)
    cdb.register_color(color1)
    color2 = MockColor("Strong_red", 255, 0, 0)
    cdb.register_color(color2)
    assert cdb.numColors() == 2
    assert cdb.is_color(color1)
    assert cdb.is_color(color2)

@mock.patch.object(colorsRedis, 'connect', mock_connect)
def test_duplicate_color_not_set():
    cdb = colorsRedis()
    color = MockColor("Strong_blue", 0, 0, 255)
    cdb.register_color(color)
    color = MockColor("Strong_blue", 0, 0, 255)
    cdb.register_color(color)
    assert cdb.numColors() == 1
    assert cdb.is_color(color)


def test_object_throws_connection_error_if_no_db_available():
    with pytest.raises(ConnectionError):
        cdb = colorsRedis()

