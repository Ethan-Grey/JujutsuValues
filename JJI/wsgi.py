"""
WSGI config for JJI project.
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JJI.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '..'))
application.add_files('staticfiles', prefix='/static/')
application.add_files('static', prefix='/static/')
application.add_files('media', prefix='/media/')
