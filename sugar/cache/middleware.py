from django.conf import settings
from django.utils.cache import patch_cache_control

class HTTPCacheControlMiddleware(object):
    """
    Simple middleware which sets HTTP Cache-Control headers without all of the
    other overhead of django.middleware.cache.UpdateCacheMiddleware. This is
    intended for use with a front-end accelerator such as Varnish when you
    want Django to set cache policy but not actually cache responses.

    Basic rules:
        1. To avoid accidental leaks of private information only anonymous
           requests will be updated
        2. We only set headers for successful GET requests
        3. We don't touch requests which already have a Cache-Control header

    Usage:
        1. Add "sugar.utils.cache.HTTPCacheControlMiddleware" to your
           MIDDLEWARE_CLASSES
        2. Add a dictionary to settings.py which has the values you want::
            DEFAULT_HTTP_CACHE_CONTROL = dict(public=True, max_age=300)
    """
    def __init__(self):
        self.cache_control_args = getattr(settings, "DEFAULT_HTTP_CACHE_CONTROL", {})

    def process_response(self, request, response):
        if hasattr(request, "user") and not request.user.is_anonymous():
            return response

        if request.method != 'GET':
            return response

        if not response.status_code == 200:
            return response

        if response.has_header("Cache-Control"):
            return response

        patch_cache_control(response, **self.cache_control_args)

        return response
