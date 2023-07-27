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
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from journal_api.middleware import TokenAuthMiddleware
import journal_api.routing



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_website.settings')






# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     'websocket': 
    
#     AuthMiddlewareStack(
#         URLRouter(
#             journal_api.routing.websocket_urlpatterns
#         )
#     )
# })

application = ProtocolTypeRouter({ 
    "http": get_asgi_application(), 
    'websocket': TokenAuthMiddleware( 
        AuthMiddlewareStack( 
            URLRouter( 
                journal_api.routing.websocket_urlpatterns 
            ) 
        ) 
    ) 
})