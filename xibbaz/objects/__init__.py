"""
Implementation of Zabbix API objects.
"""

from .host import Host
from .hostgroup import HostGroup
from .maintenance import Maintenance
from .template import Template
from .trigger import Trigger
from .item import Item

# Export as all lowercase as well for compatibility with api.
host = Host
hostgroup = HostGroup
item = Item
maintenance = Maintenance
template = Template
trigger = Trigger

__all__ = [
    'ApiObject',
    'Host', 'host',
    'HostGroup', 'hostgroup',
    'Item', 'item',
    'Maintenance', 'maintenance',
    'Template', 'template',
    'Trigger', 'trigger',
]
