# """
# ASGI config for zaanQueril project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zaanQueril.settings')

# application = get_asgi_application()
# asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

from channels.auth import AuthMiddlewareStack
import zqUsers.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zaanQueril.settings')
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket':AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter( zqUsers.routing.websocket_urlpatterns)))
})
