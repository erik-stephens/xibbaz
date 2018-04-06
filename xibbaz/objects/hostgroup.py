
from .api import ApiObject


class HostGroup(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/hostgroup/object
    """

    ID_FIELD = 'groupid'


    @classmethod
    def create(C, api, name):
        """
        Return id of new `HostGroup` with given `name`.
        """
        params = dict(
            name = name,
        )
        result = api.response('hostgroup.create', **params).get('result')
        return result.get('groupids')[0]


    @classmethod
    def get(Class, api, **params):
        """
        Return `[HostGroup]` that match criteria.
        """
        if 'selectHosts' not in params:
            params['selectHosts'] = True
        result = api.response('hostgroup.get', **params).get('result')
        return [Class(api, **i) for i in result]


    def json(self):
        """
        Return all properties as a dict suitable for JSON.
        """
        # TODO: Handle circular references
        d = super().json()
        d['hosts'] = [i.json() for i in self.hosts.values()]
        return d


    def _process_refs(self, attrs):
        """
        Process references to other xibbaz objects:
          - hosts: {name: Host}
          - templates: {name: Template}
        """
        # Import here to avoid circular imports.
        from .host import Host
        self.hosts = {}
        if 'hosts' in attrs:
            for host in attrs['hosts']:
                # print('host:', host)
                # TODO: What if selectHosts=False?  We only get {'hostid': '123'}.
                if 'name' in host:
                    self.hosts[host['name']] = Host(self._api, **host)
        # from .template import Template
        # self.templates = {}
        # if 'templates' in attrs:
        #     for template in attrs['templates']:
        #         self.templates[template['name']] = Template(self._api, **template)


    def add_hosts(self, *hosts):
        """
        Add `hosts:[Host]` to this group.
        """
        params = dict(
            groups = [dict(groupid = self.id)],
            hosts = [dict(hostid = i.id) for i in hosts],
        )
        result = self._api.response('hostgroup.massadd', **params).get('result')
        for host in hosts:
            if host.id in result.get('hostids'):
                self.hosts[host.name.val] = host


    def remove_hosts(self, *hosts):
        """
        Remove `hosts:[Host]` from this group.
        """
        params = dict(
            groupids = [self.id],
            hostids = [i.id for i in hosts],
        )
        return self._api.response('hostgroup.massremove', **params).get('result')


    PROPS = dict(
        groupid = dict(
            doc = "ID of the host group.",
            id = True,
            readonly = True,
        ),
        name = dict(
            doc = "Name of the host group.",
        ),
        flags = dict(
            doc = "Origin of the host group.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain host group',
                4: 'a discovered host group',
            },
        ),
        internal = dict(
            doc = "Whether the group is used internally by the system. An internal group cannot be deleted.",
            kind = int,
            readonly = True,
            vals = {
                0: 'not internal (default)',
                1: 'internal',
            },
        ),
    )
