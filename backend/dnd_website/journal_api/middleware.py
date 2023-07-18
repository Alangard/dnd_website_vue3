# import os
# from datetime import datetime

# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()

# import jwt
# from channels.auth import AuthMiddlewareStack
# from django.conf import settings
# from django.contrib.auth.models import AnonymousUser
# from channels.db import database_sync_to_async
# from channels.middleware import BaseMiddleware

# from django.contrib.auth.models import User
# from .models import Account
# from django.db import close_old_connections

# import logging
# logger = logging.getLogger(__name__)


# ALGORITHM = "HS256"


# def get_user(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
#         print('payload', payload)
#         logger.debug('payload: %s', payload)
#     except:
#         print('no payload')
#         logger.debug('no payload')
#         return AnonymousUser()


#     token_exp = datetime.fromtimestamp(payload['exp'])
#     if token_exp < datetime.utcnow():
#         logger.debug('no date-time')
#         print("no date-time")
#         return AnonymousUser()

#     try:
#         user = Account.objects.get(id=payload['user_id'])
#         print('user', user)
#         logger.debug('user: %s', user)
#     except Account.DoesNotExist:
#         logger.debug('no date-time')
#         print('no user')
#         return AnonymousUser()

#     return user


# class TokenAuthMiddleware(BaseMiddleware):

#     async def __call__(self, scope, receive, send):

#         close_old_connections()
#         try:
#             token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
#             print(token_key)
#             logger.debug('token_key: %s', token_key)
#         except ValueError:
#             token_key = None

#         scope['user'] = await get_user(token_key)
#         logger.debug('d2: %s', scope['user'])
#         print('d2', scope['user'])
#         return await super().__call__(scope, receive, send)


# def JwtAuthMiddlewareStack(inner):
#     return TokenAuthMiddleware(inner)
#     # return TokenAuthMiddleware(AuthMiddlewareStack(inner))


from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async



class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):

        await sync_to_async(close_old_connections)()

        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        try:
           
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
     
            print(e)
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            user = await sync_to_async(get_user_model().objects.get)(id=decoded_data["user_id"])
            scope['user'] = user

        return await self.inner(scope, receive, send)

