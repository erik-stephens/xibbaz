
from . import api_session


def test_create_group1():
    'Can create a new hostgroup.'
    with api_session() as api:
        api.mock_reply(result={
            'groupids' : ['42'],
        })
        id = api.host_group_create('g1')
        assert id == '42'
        api.mock_reply(result=[{
            "hosts": [],
            "internal": "0",
            "flags": "0",
            "groupid": "42",
            "name": "g1",
        }])
        group = api.host_group('g1')
        assert group.id == '42'
        assert group.name.val == 'g1'


def test_add_host1():
    'Can add a host to a group.'
    with api_session() as api:
        api.mock_reply(result=[{
            "hostid" : "45",
            "name": "h1",
            "items": "42",
        }])
        host = api.host('h1')
        api.mock_reply(result=[{
            "hosts": [],
            "internal": "0",
            "flags": "0",
            "groupid": "14",
            "name": "g1",
        }])
        group = api.host_group('g1')
        api.mock_reply(result={
            "hostids": ["40"],
        })
        group.add_hosts(host)
        assert 'h1' not in group.hosts
        api.mock_reply(result={
            "hostids": ["45"],
        })
        group.add_hosts(host)
        assert 'h1' in group.hosts
