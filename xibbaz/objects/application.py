
from datetime import datetime
from .api import ApiObject


class Application(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/application/object
    """

    DEFAULT_SELECTS = ()

    RELATIONS = ('hosts', 'items', 'templates')


    def delete(self):
        """
        Delete this Application.
        """
        params = [self.id]
        return self._api.response('application.delete', params).get('result')


    PROPS = dict(
        applicationid = dict(
            doc = "ID of the application.",
            id = True,
            readonly = True,
        ),
        hostid = dict(
            doc = "ID of the host that the application belongs to.",
        ),
        name = dict(
            doc = "Name of the application.",
        ),
        flags = dict(
            doc = "Origin of the application.",
            kind = int,
            vals = {
                0: 'a plain application',
                4: 'a discovered application',
            },
        ),
        templateids = dict(
            doc = "IDs of the parent template applications.",
            kind = tuple,
        ),
    )
