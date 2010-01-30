# encoding: utf-8

from django.conf import settings
from django.contrib.sites.models import Site

def site_settings(request):
    """Expose common Django settings to templates"""

    context = {
        'CURRENT_SITE': Site.objects.get_current(),
    }

    for k in ('DEBUG', 'LOCAL_DEV', 'VERSION', 'MEDIA_URL', 'STATIC_URL', 'MEDIA_KEY'):
        if hasattr(settings, k):
            context[k] = getattr(settings, k)

    return context
