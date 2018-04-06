
from xibbaz.objects import Item
from . import api_session


def test_history_text1():
    'Can retrieve textual history.'
    with api_session() as api:
        item = Item(api, itemid='1', key_='version', value_type=Item.TYPE_TEXT)
        api.mock_reply(result=[
            {"itemid": "1", "ns": "0", "value": "Darwin 13.0.1", "clock": "1391709315"},
            {"itemid": "1", "ns": "0", "value": "Darwin 13.0.2", "clock": "1391709316"},
        ])
        l = item.get_history()
        assert ['Darwin 13.0.1', 'Darwin 13.0.2'] == [i[1] for i in l]


def test_history_int1():
    'Can retrieve integer history.'
    with api_session() as api:
        item = Item(api, itemid='1', key_='item1', value_type=Item.TYPE_INT)
        api.mock_reply(result=[
            {"itemid": "1", "ns": "0", "value": "1", "clock": "1391709315"},
            {"itemid": "1", "ns": "0", "value": "2", "clock": "1391709315"},
        ])
        l = item.get_history()
        assert [1, 2] == [i[1] for i in l]


def test_history_float1():
    'Can retrieve floating point history.'
    with api_session() as api:
        item = Item(api, itemid='1', key_='item1', value_type=Item.TYPE_FLOAT)
        api.mock_reply(result=[
            {"itemid": "1", "ns": "0", "value": "-1.1", "clock": "1391709315"},
            {"itemid": "1", "ns": "0", "value": "2.59", "clock": "1391709315"},
        ])
        l = item.get_history()
        assert [-1.1, 2.59] == [i[1] for i in l]
