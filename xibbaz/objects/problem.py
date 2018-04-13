
from datetime import datetime
from .api import ApiObject


class Problem(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/problem/object
    """

    DEFAULT_SELECTS = ()

    RELATIONS = ()

    @classmethod
    def _id_field(Class, plural=False):
        """
        Name used for api endpoints.
        """
        return 'eventid' + (plural and 's' or '')


    def _process_refs(self, attrs):
        """
        Give references to other ApiObjects the xibbaz treatment.
        """
        # Load event & related object lazily.
        self._event = None
        self._trigger = None


    @property
    def event(self):
        """
        `Event` for this Problem.
        """
        if self._event is None:
            self._event = self._api.event(self.eventid.val)
        return self._event


    @property
    def trigger(self):
        """
        `Trigger` if related object is a trigger.
        """
        if self.object.val != 0:
            return None
        if self._trigger is None:
            self._trigger = self._api.trigger(self.objectid.val)
        return self._trigger


    PROPS = dict(
        eventid = dict(
            doc = "ID of the problem event.",
            id = True,
            readonly = True,
        ),
        source = dict(
            doc = "Type of the problem event.",
            kind = int,
            vals = {
                0: 'event created by a trigger',
                3: 'internal event',
            },
        ),
        object = dict(
            doc = "Type of object that is related to the problem event.",
            kind = int,
            vals = {
                0: 'trigger',
                4: 'item',
                5: 'LLD rule',
            },
        ),
        objectid = dict(
            doc = "ID of the related object.",
            id = True,
            readonly = True,
        ),
        clock = dict(
            doc = "Time when the problem event was created.",
            kind = datetime,
            readonly = True,
        ),
    )
