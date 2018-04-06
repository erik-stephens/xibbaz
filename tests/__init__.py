
# from nose.tools import assert_raises
from pytest import raises
from mock import patch, Mock
from contextlib import contextmanager
from functools import partial
from datetime import datetime
import json
from xibbaz import Api, ApiException
from xibbaz.objects import Host, HostGroup


@contextmanager
def api_session(auth=True):
    """
    Yield an `Api` instance with a mocked requests.session instance
    and extra mock_reply() method to use like so:

        with api_session() as api:
            api.mock_reply(result='...')
            api.response('host.get', params)
    """
    with patch('xibbaz.api.requests.session') as session:
        api = Api('http://xibbaz', session)
        api.mock_reply = partial(mock_reply, session)
        if auth:
            api.mock_reply(result='36fc69043640c433c0010773499b44af')
            api.login('user', 'pass')
        yield api

def mock_reply(session, **fields):
    """
    Mock session.post() response to look like a zabbix response.
    """
    fields['jsonrpc'] = '2.0'
    fields['id'] = 0
    session.post.return_value = Mock(text=json.dumps(fields))


def test_auth1():
    'Return true when auth succeeds.'
    with api_session(auth=False) as api:
        api.mock_reply(result='36fc69043640c433c0010773499b44af')
        assert api.login('foo', 'bar')


def test_auth2():
    'Return false when auth fails.'
    with api_session(auth=False) as api:
        api.mock_reply(error={"code":-32602,"message":"Invalid params.","data":"Login name or password is incorrect."})
        assert not api.login('foo', 'bar')


def test_readonly1():
    'Setting a read-only property raises ApiException.'
    with api_session() as api:
        api.mock_reply(result=[{"groupid":"45","name":"MyGroup","internal":"0","flags":"0"}])
        grp = HostGroup.by_name(api, 'MyGroup')
        with raises(ApiException) as cm:
            grp.internal.val = 2
        assert cm.exception.code == -2


def test_type_int1():
    'Integer properties are coerced to ints.'
    with api_session() as api:
        api.mock_reply(result=[{"groupid":"45","name":"MyGroup","internal":"0","flags":"0"}])
        grp = HostGroup.by_name(api, 'MyGroup')
        assert isinstance(grp.internal.val, int)


def test_type_ts1():
    'Timestamp properties are coerced to datetimes.'
    with api_session() as api:
        api.mock_reply(result=[{"hostid":"45","name":"MyHost","errors_from":"1388867607"}])
        host = Host.by_name(api, 'MyHost')
        assert isinstance(host.errors_from.val, datetime)
        assert host.errors_from.val == datetime(2014, 1, 4, 20, 33, 27)


def test_id1():
    'The ID is saved as a non-property attribute.'
    with api_session() as api:
        api.mock_reply(result=[{"groupid":"45","name":"MyGroup","internal":"0","flags":"0"}])
        grp = HostGroup.by_name(api, 'MyGroup')
        assert grp.id == 45
