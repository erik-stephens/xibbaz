
from datetime import datetime
from .api import ApiObject


class Event(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/event/object
    """

    DEFAULT_SELECTS = ('Hosts', 'RelatedObject', 'Tags')

    RELATIONS = ('hosts',)


    def _process_refs(self, attrs):
        """
        Give references to other ApiObjects the xibbaz treatment.
        """
        super()
        obj = attrs.get('relatedObject')
        if obj and attrs.get('object') == 0:
            from .trigger import Trigger
            self._trigger = Trigger(self._api, **attrs)
        else:
            self._trigger = None


    @property
    def trigger(self):
        """
        `Trigger` if related object is a trigger, None otherwise.
        """
        if self.object.val != 0:
            return None
        if self._trigger is None:
            self._trigger = self._api.trigger(self.objectid.val)
        return self._trigger


    PROPS = dict(
        eventid = dict(
            doc = "ID of the event.",
            id = True,
            readonly = True,
        ),
        source = dict(
            doc = "Type of the event.",
            readonly = True,
            kind = int,
            vals = {
                0: 'event created by a trigger',
                1: 'event created by a discovery rule',
                2: 'event created by a active agent auto-registration',
                3: 'internal event',
            },
        ),
        object = dict(
            doc = "Type of object that is related to the event.",
            readonly = True,
            kind = int,
            vals = {
                0: 'trigger',
                1: 'discovered host',
                2: 'discovered service',
                3: 'auto-registered host',
                4: 'item',
                5: 'LLD rule',
            },
        ),
        objectid = dict(
            doc = "ID of the related object.",
            readonly = True,
        ),
        clock = dict(
            doc = "Time when the event was created.",
            kind = datetime,
            readonly = True,
        ),
        ns = dict(
            doc = "Nanoseconds when the event was created.",
            kind = int,
            readonly = True,
        ),
        value = dict(
            doc = "State of the related object.",
            readonly = True,
            kind = int,
            vals = {
                0: '{trigger:ok discovery:up internal:normal}',
                1: '{trigger:problem discovery:down internal:unknown}',
                2: '{discovery:discovered}',
                3: '{discvoery:lost}',
            },
        ),
        userid = dict(
            doc = "User ID if the event was manually closed.",
            readonly = True,
        ),
    )
