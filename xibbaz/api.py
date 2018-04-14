"""
A pythonic interface to the Zabbix APself.
"""

import os
import sys
import requests
import json
import re
from . import objects

__all__ = [
    'Api',
    'ApiException',
]


class ApiException(Exception):
    """
    Raised when bad reply from server or error msg in the reply.
    """
    INVALID_REPLY    = -1
    INVALID_VALUE    = -2
    FAILED_AUTH      = -32602

    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    def __str__(self):
        return "{}: {}: {}".format(self.code, self.msg, self.data)


class Api(object):
    """
    Zabbix API client / session
    """

    def __init__(self, server, session=None):
        if session is None:
            session = requests.session()
            session.headers['Content-Type'] = 'application/json-rpc'
        self._session = session
        self._endpoint = server + '/api_jsonrpc.php'
        self._id = 0
        self._auth = None


    def login(self, user, password):
        """
        Return true if able to authenticate, false otherwise.  Session
        key is saved in this object for future requests.
        """
        try:
            self._auth = self.response('user.login', user=user, password=password).get('result')
        except ApiException as e:
            if e.code != ApiException.FAILED_AUTH:
                raise
        return bool(self._auth)


    def response(self, method, **params):
        """
        Get "raw" response from zabbix server.
        """
        payload = dict(
            jsonrpc = '2.0',
            method = method,
            params = params,
            id = self._id,
            auth = self._auth,
        )
        response = self._session.post(self._endpoint, data=json.dumps(payload))
        self._id += 1

        if not response.text:
            raise ApiException(ApiException.INVALID_REPLY, 'empty reply', '')
        try:
            reply = json.loads(response.text)
            # print("API DEBUG {}:".format(method))
            # print("REQUEST:\n{}".format(json.dumps(payload, indent=2)))
            # print("RESPONSE:\n{}".format(json.dumps(reply, indent=2)))
        except ValueError:
            raise ApiException(ApiException.INVALID_REPLY, 'invalid json', response.text)

        if 'error' in reply:
            err = reply['error']
            raise ApiException(err['code'], err['message'], err['data'])

        return reply


    def host(self, name_or_id):
        """
        `Host` by id or name.
        """
        params = dict()
        if integerish(name_or_id):
            params['filter'] = dict(hostids=str(name_or_id))
        else:
            params['filter'] = dict(name=name_or_id)
        return one_only(self.hosts(**params))


    def hosts(self, **params):
        """
        Wrapper around `Host.get`.
        """
        return objects.Host.get(self, **params)


    def group_create(self, name):
        return objects.Group.create(self, name)


    def group(self, name_or_id):
        """
        `Group` by id or name.
        """
        params = dict()
        if integerish(name_or_id):
            params['filter'] = dict(groupids=str(name_or_id))
        else:
            params['filter'] = dict(name=name_or_id)
        return one_only(self.groups(**params))


    def groups(self, **params):
        """
        Wrapper around `Group.get`.
        """
        return objects.Group.get(self, **params)


    def template(self, name_or_id):
        """
        `Template` by id or name.
        """
        params = dict()
        if integerish(name_or_id):
            params['filter'] = dict(templateids=str(name_or_id))
        else:
            params['filter'] = dict(name=name_or_id)
        return one_only(self.templates(**params))


    def templates(self, **params):
        """
        Wrapper around `Template.get`.
        """
        return objects.Template.get(self, **params)


    def item(self, name_or_id):
        """
        `Item` by id or name.
        """
        params = dict()
        if integerish(name_or_id):
            params['filter'] = dict(itemids=str(name_or_id))
        else:
            params['filter'] = dict(name=name_or_id)
        return one_only(self.items(**params))


    def items(self, **params):
        """
        Wrapper around `Item.get`.
        """
        return objects.Item.get(self, **params)


    def trigger(self, id):
        """
        `Trigger` by id.
        """
        return one_only(self.triggers(triggerids=id))


    def triggers(self, **params):
        """
        Wrapper around `Trigger.get`.
        """
        return objects.Trigger.get(self, **params)


    def event(self, id):
        """
        `Event` by id.
        """
        return one_only(self.events(eventids=id))


    def events(self, **params):
        """
        Wrapper around `Event.get`.
        """
        return objects.Event.get(self, **params)


    def problems(self, **params):
        """
        Wrapper around `Problem.get`.
        """
        return objects.Problem.get(self, **params)


def integerish(val):
    """
    True if `val` looks like an integer.
    """
    return re.match('^\d+$', str(val))


def one_only(l):
    """
    Return None if `l` empty, raise exception if `len(l) > 1`, otherwise `l[0]`.
    """
    if len(l) == 1:
        return l[0]
    elif len(l) == 0:
        return None
    raise Exception('filter matched too many: {}'.format(len(l)))
