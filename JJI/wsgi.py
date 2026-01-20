"""
WSGI config for JJI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JJI.settings')

application = get_wsgi_application()

# Serve static + media directly via WhiteNoise (works on Railway without a separate CDN/storage)
application = WhiteNoise(application)
application.add_files("staticfiles", prefix="static/")
application.add_files("static", prefix="static/")
application.add_files("media", prefix="media/")
