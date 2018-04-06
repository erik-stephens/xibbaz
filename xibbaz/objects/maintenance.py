
from datetime import datetime
from .api import ApiObject


class Maintenance(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/maintenance/object
    """

    @classmethod
    def get(Class, api, **params):
        """
        Return `[Maintenance]` that match criteria:
        """
        if 'selectHosts' not in params:
            params['selectHosts'] = True
        if 'selectGroups' not in params:
            params['selectGroups'] = True
        result = api.response('maintenance.get', **params).get('result')
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


    @property
    def hosts(self):
        """
        {name: Host} of associated `Hosts`.
        """
        return self._hosts


    @property
    def groups(self):
        """
        {name: HostGroup} of associated `HostGroups`.
        """
        return self._groups


    PROPS = dict(
        name = dict(
            doc = "Maintenance period name.",
        ),
        description = dict(
            doc = "Description of the maintenance.",
        ),
        maintenance_type = dict(
            doc = "Type of maintenance.",
            kind = int,
            vals = {
                0: 'with data collection (default)',
                1: 'without data collection',
            },
        ),
        active_since = dict(
            doc = "Time when the maintenance becomes active.",
        ),
        active_till = dict(
            doc = "Time when the maintenance stops being active.",
        ),
        hostids = dict(
            doc = "IDs of hosts in this maintenance.",
            readonly = True,
        ),
        groupids = dict(
            doc = "IDs of hostgroups in this maintenance.",
            readonly = True,
        ),
        timeperiods = dict(
            doc = "The time definition of this maintenance.",
            readonly = True,
        ),
    )
