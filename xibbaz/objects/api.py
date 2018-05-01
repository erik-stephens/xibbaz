"""
Implementation of Zabbix API objects.
"""

import json
from datetime import datetime


class MetaApiObject(type):
    """
    Metaclass for ApiObject provides:
      - dynamic doc string based on ApiObject.PROPS
    """

    @property
    def __doc__(self):
        l = ['API Properties:']
        for name, prop in self.PROPS.items():
            l.append("- {}: {}".format(name, prop['doc']))
        return '\n'.join(l)


class ApiObject(object, metaclass=MetaApiObject):
    """
    Base class for all Zabbix objects.
    """

    DEFAULT_SELECTS = ()

    @classmethod
    def _zabbix_name(Class):
        """
        Name most commonly used in fields, docs, etc.
        """
        return Class.__name__.lower()


    @classmethod
    def _api_name(Class):
        """
        Name used for api endpoints.
        """
        return Class.__name__.lower()


    @classmethod
    def _id_field(Class, plural=False):
        """
        Zabbix field name for unique identifier.
        """
        return Class._zabbix_name() + 'id' + (plural and 's' or '')


    @classmethod
    def _text_field(Class):
        """
        Zabbix field name for descriptive name.
        """
        return 'name'


    @property
    def id(self):
        """
        Zabbix object's unique identifier.
        """
        return self._props[self._id_field()].val


    @property
    def text(self):
        """
        Best textual description.
        """
        return self._props[self._text_field()].val


    @classmethod
    def get(Class, api, **params):
        """
        `[ApiObject]` that match criteria in `params`.
        """
        for name in ['select' + i for i in Class.DEFAULT_SELECTS]:
            if name not in params:
                params[name] = 'extend'
        result = api.response(Class._api_name() + '.get', **params).get('result')
        return [Class(api, **i) for i in result]


    def __init__(self, api, **attrs):
        # self._id = None
        self._api = api
        self._props = dict()
        for name in attrs:
            if name not in self.PROPS:
                pass # TODO: log warning?
            else:
                spec = self.PROPS[name]
                # if spec.get('id'):
                #     self._id = attrs[name]
                prop = Property(
                    name = name,
                    val = attrs[name],
                    doc = spec.get('doc'),
                    kind = spec.get('kind', str),
                    readonly = spec.get('readonly'),
                    vals = spec.get('vals'),
                )
                setattr(self, name, prop)
                self._props[name] = prop
        self._process_refs(attrs)


    def _process_refs(self, attrs):
        """
        Give references to other ApiObjects the xibbaz treatment.
        """
        # NOTES:
        # - Import here to avoid circular imports.
        # - When selectFoo=False, there may be Foo's in the response but only the ids or a count.
        # - There's a lot of common bits could factor out here but not deemed
        #   worth the extra layers of abstraction / indirection.

        if isinstance(attrs.get('hosts'), list):
            from .host import Host
            self._hosts = []
            for host in attrs['hosts']:
                if 'name' in host:
                    self._hosts.append(Host(self._api, **host))

        if isinstance(attrs.get('groups'), list):
            from .group import Group
            self._groups = []
            for group in attrs['groups']:
                if 'name' in group:
                    self._groups.append(Group(self._api, **group))

        if isinstance(attrs.get('templates'), list):
            from .template import Template
            self._templates = []
            for template in attrs['templates']:
                if 'name' in template:
                    self._templates.append(Template(self._api, **template))

        if isinstance(attrs.get('items'), list):
            from .item import Item
            self._items = []
            for item in attrs['items']:
                if 'name' in item:
                    self._items.append(Item(self._api, **item))

        if isinstance(attrs.get('triggers'), list):
            from .trigger import Trigger
            self._triggers = []
            for trigger in attrs['triggers']:
                if 'description' in trigger:
                    self._triggers.append(Trigger(self._api, **trigger))


    def __unicode__(self):
        return json.dumps(self.json(), indent=2, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self.json(), indent=2)

    def __repr__(self):
        s = self.id
        if self._text_field() in self._props:
            s += ":{}".format(self._props[self._text_field()].val)
        return s

    def __format__(self, s):
        return self._props[self._text_field()].val.__format__(s)


    def json(self):
        """
        Return all properties as a dict suitable for JSON.
        """
        d = dict()
        for name in self._props:
            prop = getattr(self, name)
            if prop.kind == datetime:
                d[name] = prop.val.isoformat()
            else:
                d[name] = prop.val
        # Include any loaded relations.
        for relation in self.RELATIONS:
            objs = getattr(self, '_' + relation, None)
            if objs is not None:
                d[relation] = [i.json() for i in objs]
        return d


    def refresh(self):
        """
        Refresh this instance via fresh api call.
        """
        pass


    def save(self):
        """
        Publish any changes to xibbaz.
        """
        params = dict()
        dirty = False
        for name, prop in self._props.items():
            if self.PROPS[name].get('id'):
                params[name] = self.id
            if prop.dirty:
                params[name] = prop.val
                dirty = True
        if dirty:
            self._api.response('update', params)


    def _repr_html_(self):
        """
        Return html, notebook-friendly format.
        """
        html = """
            <style>
              .rendered_html td, .rendered_html th {{ text-align: left }}
              .rendered_html th.dirty, .rendered_html th.readonly {{ text-align: center }}
              .rendered_html td.dirty, .rendered_html td.readonly {{ text-align: center; color: #f00; font-weight: bold }}
            </style>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Type</th>
                  <th>Dirty</th>
                  <th>Read-Only</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {rows}
              </tbody>
            </table>
        """
        return html.format(rows='\n'.join([i._repr_html_row() for i in self._props.values()]))


    @property
    def hosts(self):
        """
        Linked Hosts.
        """
        if 'hosts' not in self.RELATIONS:
            return None
        if not hasattr(self, '_hosts'):
            params = dict()
            params[self._id_field(plural=True)] = self.id
            self._hosts = self._api.hosts(**params)
        return self._hosts


    @property
    def groups(self):
        """
        Linked Groups.
        """
        if 'groups' not in self.RELATIONS:
            return None
        if not hasattr(self, '_groups'):
            params = dict()
            params[self._id_field(plural=True)] = self.id
            self._groups = self._api.groups(**params)
        return self._groups


    @property
    def templates(self):
        """
        Linked Templates.
        """
        if 'templates' not in self.RELATIONS:
            return None
        if not hasattr(self, '_templates'):
            params = dict()
            params[self._id_field(plural=True)] = self.id
            self._templates = self._api.templates(**params)
        return self._templates


    @property
    def items(self):
        """
        Linked Items.
        """
        if 'items' not in self.RELATIONS:
            return None
        if not hasattr(self, '_items'):
            params = dict()
            params[self._id_field(plural=True)] = self.id
            self._items = self._api.items(**params)
        return self._items


    @property
    def triggers(self):
        """
        Linked Triggers.
        """
        if 'triggers' not in self.RELATIONS:
            return None
        if not hasattr(self, '_triggers'):
            params = dict()
            params[self._id_field(plural=True)] = self.id
            self._triggers = self._api.triggers(**params)
        return self._triggers


class Property(object):
    """
    Each attribute of an `ApiObject` is wrapped by this class.
    """

    @property
    def val(self):
        """
        The property's actual value.
        """
        return self._val

    @val.setter
    def val(self, val):
        """
        Set val, ensuring coerced to correct type and dirty flag set when changed.
        """
        # Import here to avoid circular imports.
        from ..api import ApiException
        if val == self._val:
            return
        if self.readonly and self._val is not None:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'read-only property',
                "already defined as: {}".format(self._val),
            )
        try:
            for xform in self._xforms:
                val = xform(val)
        except Exception as e:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid value',
                "{}: {}: {}".format(self.name, val, e),
            )
        if not isinstance(val, self.kind):
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid type',
                "{}: {} is not a {}".format(self.name, val, self.kind.__name__),
            )
        if self.vals is not None and val not in self.vals:
            raise ApiException(
                ApiException.INVALID_VALUE,
                'invalid value',
                "{}: {} not in {}".format(self.name, val, self.vals.keys()),
            )
        self._val = val
        self._dirty = True


    @property
    def dirty(self):
        """
        True if this property's value has been modified.
        """
        return self._dirty


    def __init__(self, name='', doc='', val=None, kind=str, readonly=False, vals=None):
        self.name = name
        self.__doc__ = doc
        if vals:
            self.__doc__ += '  Acceptable Values:' + ''.join("\n  - {}: {}".format(*i) for i in vals.items())
        if kind == datetime:
            self._xforms = [int, datetime.utcfromtimestamp]
        else:
            self._xforms = [kind]
        self.kind = kind
        self.readonly = bool(readonly)
        self.vals = vals
        # Now set the value so that type checking happens
        self._val = None
        self.val = val
        self._dirty = False


    def __format__(self, s):
        return str(self).__format__(s)


    def __unicode__(self):
        return repr(self)


    def __str__(self):
        if self.vals is not None and self.val in self.vals:
            return self.vals[self.val]
        return str(self.val)


    def __repr__(self):
        notes = [self.kind.__name__]
        if self.readonly:
            notes.append('read-only')
        if self.dirty:
            notes.append('dirty')
        return u"{} [{}]".format(self.val, ', '.join(notes))


    def _repr_html_(self):
        return """
            <style>
              .rendered_html td {{ text-align: left }};
              .rendered_html th.dirty, .rendered_html th.readonly {{ text-align: center }};
              .rendered_html td.dirty, .rendered_html td.readonly {{ text-align: center; color: #f00; font-weight: bold }};
            </style>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Value</th>
                  <th>Type</th>
                  <th>Dirty</th>
                  <th>Read-Only</th>
                  <th>Documentation</th>
                </tr>
              </thead>
              <tbody>{}</tbody>
              </tbody>
            </table>
        """.format(self._repr_html_row())


    def _repr_html_row(self):
        return """
           <tr>
             <td class="name">{}</td>
             <td class="value">{}</td>
             <td class="type">{}</td>
             <td class="dirty">{}</td>
             <td class="readonly">{}</td>
             <td class="doc"><pre>{}</pre></td>
           </tr>
        """.format(self.name, self.val, self.kind.__name__, self.dirty and '*' or '', self.readonly and '*' or '', self.__doc__)
