"""
WSGI config for abusor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abusor.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Main")

# This should be imported after setting DJANGO_CONFIGURATION.
from configurations.wsgi import get_wsgi_application  # noqa: E402 isort:skip

application = get_wsgi_application()
