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
import journal_api.routing

# from journal_api.middleware import TokenAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dnd_website.settings')



# application = ProtocolTypeRouter(
#     {
#         # (http->django views is added by default)
#         "http": get_asgi_application(),
#         "websocket": TokenAuthMiddleware(
#             URLRouter(journal_api.routing.websocket_urlpatterns)
#         )
#     }
# )

# application = ProtocolTypeRouter( 
#     { 
#         # (http->django views is added by default) 
#         "http": get_asgi_application(), 
#         "websocket": TokenAuthMiddleware( 
#             URLRouter(journal_api.routing.websocket_urlpatterns) 
#         ).__call__,  # добавьте вызов метода __call__
#     } 
# )


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            journal_api.routing.websocket_urlpatterns
        )
    )
})