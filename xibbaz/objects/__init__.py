"""
Implementation of Zabbix API objects.
"""

from .api import ApiObject
from .event import Event
from .host import Host
from .group import Group
from .maintenance import Maintenance
from .problem import Problem
from .template import Template
from .trigger import Trigger
from .item import Item

# Export as all lowercase as well for compatibility with api.
event = Event
host = Host
group = Group
item = Item
maintenance = Maintenance
problem = Problem
template = Template
trigger = Trigger

__all__ = [
    'ApiObject',
    'Event', 'event',
    'Host', 'host',
    'Group', 'group',
    'Item', 'item',
    'Maintenance', 'maintenance',
    'Problem', 'problem',
    'Template', 'template',
    'Trigger', 'trigger',
]
