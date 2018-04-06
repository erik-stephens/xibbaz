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

    @property
    def id(self):
        """
        Zabbix object's unique identifier.
        """
        return self._id


    def __init__(self, api, **attrs):
        self._id = None
        self._api = api
        self._props = dict()
        for name in attrs:
            if name not in self.PROPS:
                pass # TODO: log warning?
            else:
                spec = self.PROPS[name]
                if spec.get('id'):
                    self._id = attrs[name]
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
        A hook to process object-specific references.
        """
        pass


    def __unicode__(self):
        return json.dumps(self.json(), indent=2, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self.json(), indent=2)

    def __repr__(self):
        s = self.id
        if 'name' in self._props:
            s = self.name.val
        return "{}={}".format(self.__class__.__name__, s)

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
        params[self.ID_FIELD] = self.id
        for name, prop in self._props.items():
            if prop.dirty:
                params[name] = prop.val
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
        # rows = [
        #     '<style>.rendered_html td { text-align: left };</style>',
        #     '<style>.rendered_html th.dirty, .rendered_html th.readonly { text-align: center };</style>',
        #     '<style>.rendered_html td.dirty, .rendered_html td.readonly { text-align: center; color: #f00; font-weight: bold };</style>',
        #     '<table><thead><tr><th>Name</th><th>Value</th><th>Type</th><th>Dirty</th><th>Read-Only</th><th>Documentation</th></tr></thead><tbody>',
        # ]
        # for name in sorted(self._props):
        #     prop = self._props[name]
        #     val = prop.val
        #     if prop.vals and val in prop.vals:
        #         val = "{}: {}".format(val, prop.vals[val])
        #     rows.append('<tr><td class="name">{}</td><td class="value">{}</td><td class="type">{}</td><td class="readonly">{}</td><td class="dirty">{}</td><td class="doc"><pre>{}</pre></td></tr>'.format(
        #         name, val, prop.kind.__name__, prop.dirty and '*' or '', prop.readonly and '*' or '', prop.__doc__))
        # rows.append('</tbody></table>')

        return html.format(rows='\n'.join([i._repr_html_row() for i in self._props.values()]))


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


    def __unicode__(self):
        return u"{} [dirty={}, readonly={}]".format(self.val, self.dirty, self.readonly)


    def __str__(self):
        return str(self)


    def __repr__(self):
        return str(self.val)


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
