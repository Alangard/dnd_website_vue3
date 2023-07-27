from .models import Post, Comment
from .serializers import PostListReadSerializer, CommentSerializer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework import permissions
from asgiref.sync import sync_to_async

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

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
    

class CommentConsumer(GenericAsyncAPIConsumer):
    queryset = Comment
    authentication_classes = (JWTAuthentication,)

    async def connect(self, **kwargs): 
        await self.model_change.subscribe() 
        await super().connect()  

    @action()
    async def create_comment(self, payload, **kwargs):

        user = self.scope['user']
        post_id  = payload['post']
        comment_data = {**payload, 'author': user.id}

        #Check auth user
        #Change frontend request (get 1-st post and comments through websocket and verify token before it)

        try:
            serialized_data = CommentSerializer(data=comment_data)
            await sync_to_async(serialized_data.is_valid)()
            if not serialized_data.is_valid():
                raise serializers.ValidationError(serialized_data.errors)

            try:
                post = await sync_to_async(Post.objects.get)(id=post_id)                  
                comment = Comment(author=user, text=payload['text'], post=post)
                await sync_to_async(comment.save)()

                await self.send_json({'status': 'OK 200', 'status_message': 'Comment was created'})

            except Post.DoesNotExist:
                await self.send_json({'error': 'Error 404', 'error_message': 'Post objects does not exist'})

        except serializers.ValidationError as e:
            await self.send_json({'error': 'Error 400', 'error_message': e.detail})

    @action()
    async def create_reply_comment(self, payload, **kwargs):
        print(f'This is your payload {payload}')
    
    @action()
    async def delete_comment(self, payload, **kwargs):
        print(f'This is your payload {payload}')
    
    @action()
    async def partial_update_comment(self, payload, **kwargs):
        print(f'This is your payload {payload}')
    

    @model_observer(Comment)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serializer(self, instance, action, **kwargs):
        return dict(data=CommentSerializer(instance=instance).data, action=action.value)
    
    

   

