"""
Decorators and Middleware for proper HTTP Caching
"""

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from django.core.urlresolvers import get_callable
from django.utils.cache import patch_cache_control, add_never_cache_headers

def cache_control(view_func, **cache_control_args):
    """
    Like django.views.decorators.cache.cache_control except that it follows
    standard Python decorator syntax (using the first parameter as the
    function to wrap) and allows you to provide a string instead of a function
    for easy use in urls.py
    """
    view_func = get_callable(view_func)

    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        patch_cache_control(response, **cache_control_args)
        return response

    return wraps(view_func)(_wrapped_view_func)

def never_cache(view_func):
    """
    Like django.views.decorators.cache.never_cache except allows you to
    provide a string instead of a function for easy use in urls.py
    """
    view_func = get_callable(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response
    return wraps(view_func)(_wrapped_view_func)


