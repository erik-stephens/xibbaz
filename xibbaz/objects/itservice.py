
from .api import ApiObject


class ItService(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/service/object
    """

    PROPS = dict(
        serviceid = dict(
            doc = "ID of the IT service.",
            id = True,
            readonly = True,
        ),
        algorithm = dict(
            doc = "Algorithm used to calculate the state of the IT service.",
            kind = int,
            vals = {
                0: 'do not calculate',
                1: 'problem, if at least one child has a problem',
                2: 'problem, if all children have problems',
            },
        ),
        name = dict(
            doc = "Name of the host group.",
        ),
        showsla = dict(
            doc = "Whether SLA should be calculated.",
            kind = int,
            vals = {
                0: 'do not calculate',
                1: 'calculate',
            },
        ),
        sortorder = dict(
            doc = "Position of the IT service used for sorting.",
            kind = int,
        ),
        goodsla = dict(
            doc = "Minimum acceptable SLA value. If the SLA drops lower, the IT service is considered to be in problem state.",
            kind = float,
        ),
        status = dict(
            doc = "Whether the IT service is in OK or problem state.  0 if in an OK state.  Otherwise, either the priority of the linked trigger if set to 2 (Warning) or higher, or highest status of a child IT service in a problem state.",
            kind = int,
            readonly = True,
        ),
    )
