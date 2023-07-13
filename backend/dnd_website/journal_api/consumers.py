from .models import Post
from .serializers import PostListReadSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import permissions
from asgiref.sync import sync_to_async

from rest_framework_simplejwt.authentication import JWTAuthentication

import jwt
from datetime import datetime
from django.contrib.auth.models import User
from .models import Account
from channels.db import database_sync_to_async

from urllib.parse import parse_qs
from django.conf import settings


class PostConsumer(GenericAsyncAPIConsumer):
    queryset = Post.objects.filter(is_publish=True).\
            select_related('author').\
            prefetch_related('tags','post_reactions','comments')
    
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)




    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect() 

        

    @model_observer(Post)
    async def model_change(self, message, observer=None, **kwargs):
        # e = self.scope['user']
        # print(e.email)
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=PostListReadSerializer(instance=instance).data, action=action.value)
    

    
