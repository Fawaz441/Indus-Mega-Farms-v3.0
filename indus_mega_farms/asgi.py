"""
ASGI config for indus_mega_farms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from mode import dev

from django.core.asgi import get_asgi_application
if dev:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indus_mega_farms.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'indus_mega_farms.settings.prod')
    

application = get_asgi_application()
