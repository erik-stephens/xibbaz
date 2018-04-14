
from datetime import datetime
from .api import ApiObject


class Trigger(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/trigger/object
    """

    DEFAULT_SELECTS = ('Items', 'Functions', 'Dependencies', 'DiscoveryRule', 'LastEvent', 'Tags')

    RELATIONS = ('hosts', 'groups')


    @classmethod
    def _text_field(self):
        return 'description'


    PROPS = dict(
        triggerid = dict(
            doc = "ID of the trigger.",
            id = True,
            readonly = True,
        ),
        description = dict(
            doc = "Name of the trigger.",
        ),
        expression = dict(
            doc = "Reduced trigger expression.",
        ),
        comments = dict(
            doc = "Additional comments to the trigger.",
        ),
        error = dict(
            doc = "Error text if there have been any problems when updating the state of the trigger.",
            readonly = True,
        ),
        flags = dict(
            doc = "Origin of the trigger.",
            kind = int,
            readonly = True,
            vals = {
                0: 'a plain trigger (default)',
                4: 'a discovered trigger',
            },
        ),
        lastchange = dict(
            doc = "Time when the trigger last changed its state.",
            kind = datetime,
            readonly = True,
        ),
        priority = dict(
            doc = "Severity of the trigger.",
            kind = int,
            vals = {
                0: 'not classified (default)',
                1: 'information',
                2: 'warning',
                3: 'average',
                4: 'high',
                5: 'disaster',
            },
        ),
        state = dict(
            doc = "State of the trigger.",
            kind = int,
            readonly = True,
            vals = {
                0: 'trigger state is up to date (default)',
                1: 'current trigger state is unknown',
            },
        ),
        status = dict(
            doc = "Whether the trigger is enabled or disabled.",
            kind = int,
            vals = {
                0: 'enabled (default)',
                1: 'disabled',
            },
        ),
        templateid = dict(
            doc = "ID of the parent template trigger.",
            readonly = True,
        ),
        type = dict(
            doc = "Whether the trigger can generate multiple problem events.",
            kind = int,
            vals = {
                0: 'do not generate multiple events (default)',
                1: 'generate multiple events',
            },
        ),
        url = dict(
            doc = "URL associated with the trigger.",
        ),
        value = dict(
            doc = "Whether the trigger is in OK or problem state.",
            kind = int,
            readonly = True,
            vals = {
                0: 'ok',
                1: 'problem',
            },
        ),
        recovery_mode = dict(
            doc = "OK event generation mode.",
            kind = int,
            vals = {
                0: 'expression (default)',
                1: 'recovery expression',
                2: 'none',
            },
        ),
        recovery_expression = dict(
            doc = "Reduced trigger recovery expression.",
        ),
        correlation_mode = dict(
            doc = "OK event closes.",
            kind = int,
            vals = {
                0: 'all problems (default)',
                1: 'all problems if tag values match',
            },
        ),
        correlation_tag = dict(
            doc = "Tag for matching.",
        ),
        manual_close = dict(
            doc = "Allow manual close.",
            kind = int,
            vals = {
                0: 'no (default)',
                1: 'yes',
            },
        ),
    )
