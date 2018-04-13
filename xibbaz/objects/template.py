
from datetime import datetime
from .api import ApiObject


class Template(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/template/object
    """

    DEFAULT_SELECTS = ('Groups', 'Items', 'Triggers', 'Macros')

    RELATIONS = ('hosts', 'groups', 'items', 'triggers')

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
