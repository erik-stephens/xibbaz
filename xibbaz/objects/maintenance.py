
from .api import ApiObject


class Maintenance(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/maintenance/object
    """

    DEFAULT_SELECTS = ('Hosts', 'Groups', 'Timeperiods')

    RELATIONS = ('hosts', 'groups')

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
            doc = "IDs of groups in this maintenance.",
            readonly = True,
        ),
        timeperiods = dict(
            doc = "The time definition of this maintenance.",
            readonly = True,
        ),
    )
