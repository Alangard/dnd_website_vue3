"""
ASGI config for dnd_website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""


"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_eventstream

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

application = ProtocolTypeRouter({
    'http': URLRouter([
        path('events/', AuthMiddlewareStack(
            URLRouter(django_eventstream.routing.urlpatterns)
        ), { 'channels': ['test'] }),
        re_path(r'', get_asgi_application()),
    ]),
})