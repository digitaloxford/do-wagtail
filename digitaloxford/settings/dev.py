from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ADMINS = []

INSTALLED_APPS += ["django_extensions", "coverage"]

INTERNAL_IPS = [
    "127.0.0.1",
]
