"""
Query String manipulation filters
"""

from django import template
from django.http import QueryDict
from django.utils.translation import ugettext as _
from django.utils.html import escape

register = template.Library()


class QueryStringAlterer(template.Node):
    """
    Query String alteration template tag

    Receives a query string (either text or a QueryDict such as request.GET)
    and a list of changes to apply. The result will be returned as text query
    string, allowing use like this::

        <a href="?{%% qs_alter request.GET type=object.type %%}">{{ label }}</a>

    There are two available alterations:

        Assignment:

            name=var

        Deletion - removes the named parameter:

            delete:name

        Delete a parameter matching a value:

            delete_value:"name",value

        Delete a parameter matching a value from another variable:

            delete_value:"field_name",value

    Examples:

    Query string provided as QueryDict::

        {%% qs_alter request.GET foo=bar %%}
        {%% qs_alter request.GET foo=bar baaz=quux %%}
        {%% qs_alter request.GET foo=bar baaz=quux delete:corge %%}

    Remove one facet from a list:

        {%% qs_alter request.GET foo=bar baaz=quux delete_value:"facets",value %%}

    Query string provided as string::

        {%% qs_alter "foo=baaz" foo=bar %%}">
    """

    def __init__(self, base_qs, *args):
        self.base_qs = template.Variable(base_qs)
        self.args = args

    def render(self, context):
        base_qs = self.base_qs.resolve(context)

        if isinstance(base_qs, QueryDict):
            qs = base_qs.copy()
        else:
            qs = QueryDict(base_qs, mutable=True)

        for arg in self.args:
            if arg.startswith("delete:"):
                v = arg[7:]
                if v in qs:
                    del qs[v]
            elif arg.startswith("delete_value:"):
                field, value = arg[13:].split(",", 2)
                value = template.Variable(value).resolve(context)

                if not (field[0] == '"' and field[-1] == '"'):
                    field = template.Variable(field).resolve(context)

                f_list = qs.getlist(field)
                if value in f_list:
                    f_list.remove(value)
                    qs.setlist(field, f_list)

            else:
                k, v = arg.split("=", 2)
                qs[k] = template.Variable(v).resolve(context)

        return escape(qs.urlencode())

    @classmethod
    def qs_alter_tag(cls, parser, token):
        try:
            bits = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError(
                _('qs_alter requires at least two arguments: the initial query string and at least one alteration')
            )

        return QueryStringAlterer(bits[1], *bits[2:])

register.tag('qs_alter', QueryStringAlterer.qs_alter_tag)
