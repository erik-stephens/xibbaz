
from datetime import datetime
from .api import ApiObject


class Template(ApiObject):
    """
    https://www.xibbaz.com/documentation/3.4/manual/api/reference/template/object
    """

    DEFAULT_SELECTS = ('Groups', 'Items', 'Triggers', 'Macros')

    RELATIONS = ('hosts', 'groups', 'items', 'triggers')


    def add_hosts(self, *hosts):
        """
        Add one or more Hosts to this Template.
        """
        params = dict(
            templates = [dict(templateid = self.id)],
            hosts = [dict(hostid = i.id) for i in hosts],
        )
        return self._api.response('template.massadd', **params).get('result')


    def remove_hosts(self, *hosts):
        """
        Remove one or more Hosts from this Template.
        """
        params = dict(
            templateids = [self.id],
            hostids = [i.id for i in hosts],
        )
        return self._api.response('template.massremove', **params).get('result')


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
