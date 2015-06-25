"""
WSGI config for reportstar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os, sys
sys.path.insert(0, '/var/www/html/usersurvey/environ/lib/python2.7/site-packages')
sys.path.insert(0, '/var/www/html/usersurvey/reportstar')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reportstar.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
