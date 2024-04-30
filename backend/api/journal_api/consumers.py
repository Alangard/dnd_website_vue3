
from asgiref.sync import sync_to_async

from django.conf import settings
    
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


async def get_user_obj(token):
    try:
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        print(e)
        return None
    else:
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = await sync_to_async(get_user_model().objects.get)(id=decoded_data["user_id"])
    return user
          
# only django-channels (without DCRF)
class PostConsumer(AsyncWebsocketConsumer):

    async def connect(self): 
        await self.channel_layer.group_add('post', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('post', self.channel_name)

    async def send_new_post(self, event):

        data = {
            'status': '200',
            'status_message': "Post has been created",
            'action': 'create_post'
        }

        await self.send(json.dumps(data))


# only django-channels (without DCRF)
class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        token = self.scope["query_string"].decode().replace("token=", "")
        user = await get_user_obj(token)

        self.group_name = f'{user.username}_{user.id}'

        # Присоединить клиента к группе
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Отсоединить клиента от группы при закрытии соединения
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def send_notification(self, event):
        
        data = {
            'status': '200',
            'status_message': "Notification",
            'data': event['data'],
        }

        print('send')

        await self.send(json.dumps(data))






   

