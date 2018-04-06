
from datetime import datetime
from .api import ApiObject


class Template(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/template/object
    """

    @classmethod
    def get(Class, api, **params):
        """
        Return `[Host]` that match criteria:
        """
        # TODO: selectTemplates & selectParentTemplates?
        if 'selectHosts' not in params:
            params['selectHosts'] = True
        if 'selectGroups' not in params:
            params['selectGroups'] = True
        if 'selectItems' not in params:
            params['selectItems'] = True
        if 'selectTriggers' not in params:
            params['selectTriggers'] = True
        if 'selectMacros' not in params:
            params['selectMacros'] = True
        result = api.response('template.get', **params).get('result')
        return [Class(api, **i) for i in result]


    def _process_refs(self, attrs):
        # Import here to avoid circular imports.
        from .host import Host
        self._hosts = {}
        if 'hosts' in attrs:
            for host in attrs['hosts']:
                self._hosts[host['name']] = Host(self._api, **host)
        from .hostgroup import HostGroup
        self._groups = {}
        if 'groups' in attrs:
            for group in attrs['groups']:
                self._groups[group['name']] = HostGroup(self._api, **group)
        from .item import Item
        self._groups = {}
        if 'groups' in attrs:
            for group in attrs['groups']:
                self._groups[group['name']] = Item(self._api, **group)
        from .trigger import Trigger
        self._groups = {}
        if 'groups' in attrs:
            for group in attrs['groups']:
                self._groups[group['name']] = Trigger(self._api, **group)


    @property
    def hosts(self):
        """
        {name: Host} of linked `Hosts`.
        """
        return self._hosts


    @property
    def groups(self):
        """
        {name: HostGroup} of linked `HostGroups`.
        """
        return self._groups


    PROPS = dict(
        templateid = dict(
            doc = "ID of the template.",
            id = True,
            readonly = True,
        ),
        template = dict(
            doc = "Technical name of the template. NOTE: departing from xibbaz docs which call this `host`.",
        ),
        description = dict(
            doc = "Description of the template.",
        ),
        name = dict(
            doc = "Visible name of the template, defaults to `template` property value.",
        ),
    )
