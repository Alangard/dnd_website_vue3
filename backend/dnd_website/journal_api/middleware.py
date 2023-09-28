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

