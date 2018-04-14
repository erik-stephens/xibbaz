"""
A pythonic interface to the Zabbix API.
"""

import os
from .api import Api, ApiException


def login(url=None, username=None, password=None):
    """
    Helper around common way to get credentials and log in.
    """
    api = Api(url or os.environ['ZABBIX_API'])
    if username is None:
        if 'ZABBIX_USER' in os.environ:
            username = os.environ['ZABBIX_USER']
        else:
            username = os.environ['USER']
    if password is None:
        if 'ZABBIX_PASS' in os.environ:
            password = os.environ['ZABBIX_PASS']
        else:
            import keyring
            password = keyring.get_password('zabbix-api', username)
    api.login(username, password)
    return api
