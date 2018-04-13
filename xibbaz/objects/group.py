
from .api import ApiObject


class Group(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/hostgroup/object
    """

    DEFAULT_SELECTS = ('Hosts', 'DiscoveryRule', 'GroupDiscovery', 'Templates')

    RELATIONS = ('hosts', 'templates')


    @classmethod
    def _api_name(Class):
        """
        Name used for api endpoints.
        """
        return 'hostgroup'


    @classmethod
    def create(C, api, name, **fields):
        """
        New `Group`.
        """
        fields['name'] = name
        r = api.response('hostgroup.create', **fields).get('result')
        return api.group(r.get('groupids')[0])


    def add_hosts(self, *hosts):
        """
        Add one or more Hosts to this Group.
        """
        params = dict(
            groups = [dict(groupid = self.id)],
            hosts = [dict(hostid = i.id) for i in hosts],
        )
        return self._api.response('hostgroup.massadd', **params).get('result')
        # for host in hosts:
        #     if host.id in result.get('hostids'):
        #         self._hosts.append(host)


    def remove_hosts(self, *hosts):
        """
        Remove one or more Hosts from this Group.
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
