"""
WSGI config for TotT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TotT.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# paths for AWS
sys.path.append('/opt/python/current/app/TotT/TotT/src/')
sys.path.append('/opt/python/current/app/lib/python2.7/site-packages/')

# Wrap werkzeug debugger if DEBUG is on
from django.conf import settings
if settings.DEBUG:
    try:
        import django.views.debug
        import six
        from werkzeug.debug import DebuggedApplication

        def null_technical_500_response(request, exc_type, exc_value, tb):
            six.reraise(exc_type, exc_value, tb)

        django.views.debug.technical_500_response = null_technical_500_response
        application = DebuggedApplication(application, evalex=True)
    except ImportError:
        pass
