import re

from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_by_name
import pygments

from django import template

register = template.Library()

CODE_RE = re.compile(r'<code([^>]*)>(.*?)</code>', re.DOTALL)
CLASS_RE = re.compile(r'class="([^"]+)"')

def pygmentizer(match):
    code_block = match.group(2)

    lexer = None

    class_match = CLASS_RE.search(match.group(1))

    if class_match:
        for cls in class_match.group(1).split(" "):
            try:
                lexer = get_lexer_by_name(cls)
                break
            except ValueError:
                pass

    if not lexer:
        lexer = guess_lexer(code_block)

    return pygments.highlight(code_block, lexer, HtmlFormatter())


@register.filter(name='pygmentize')
def pygmentize(value):
    '''
    Finds all <code class="python"></code> blocks in a text block and replaces it with
    pygments-highlighted html semantics. It relies that you provide the format of the
    input as class attribute.

    Inspiration:  http://www.djangosnippets.org/snippets/25/
    Updated by: Samualy Clay

    Example
    -------

    {% post.body|pygmentize %}

    '''

    return CODE_RE.sub(pygmentizer, unicode(value))
