"""
WSGI config for digitaloxford project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.path.exists(os.getcwd() + '/env.py'):
    # env.py is excluded by .gitignore
    from .env import *
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "digitaloxford.settings.production")

application = get_wsgi_application()
