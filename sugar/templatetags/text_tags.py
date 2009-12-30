import re

from django import template

register = template.Library()


@register.filter
def truncchar(value, arg):
    '''
    Truncate after a certain number of characters.

    Source: http://www.djangosnippets.org/snippets/194/

    Notes
    -----
    Super stripped down filter to truncate after a certain number of letters.

    Example
    -------

    {{ long_blurb|truncchar:20 }}

    The above will display 20 characters of the long blurb followed by "..."

    '''

    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'


@register.filter
def re_sub(string, args):
    """
    Provide a full regular expression replace on strings in templates

    Usage:

    {{ my_variable|re_sub:"/(foo|bar)/baaz/" }}
    """
    old = args.split(args[0])[1]
    new = args.split(args[0])[2]

    return re.sub(old, new, string)


@register.filter
def replace(string, args):
    """
    Provide a standard Python string replace in templates

    Usage:

    {{ my_variable|replace:"/foo/bar/" }}
    """
    old = args.split(args[0])[1]
    new = args.split(args[0])[2]

    return string.replace(old, new)
