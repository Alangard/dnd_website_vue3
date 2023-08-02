from .models import Post, Comment, Account
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
    

from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async

import re
import os
import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# django.setup()


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

    async def connect(self, **kwargs): 
        await self.model_change.subscribe() 
        await super().connect()  

    @action()
    async def create_comment(self, payload, token, request_id, action, **kwargs):

        try:
            user = await get_user_obj(token)
            user_id = user.id
        
        except:
            await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'User object does not exist/token is invalid or expired'})

        post_id  = payload['post']
        comment_data = {**payload, 'author': user_id}

        try:
            serialized_data = CommentSerializer(data=comment_data)
            await sync_to_async(serialized_data.is_valid)()
            if not serialized_data.is_valid():
                raise serializers.ValidationError(serialized_data.errors)
            
        except serializers.ValidationError as e:
            await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e.detail})

        try:
            post = await sync_to_async(Post.objects.get)(id=post_id)                  
        except Post.DoesNotExist:
            await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Post object does not exist'})
    

        comment = Comment(author=user, text=payload['text'], post=post)
        await sync_to_async(comment.save)()


    @action()
    async def create_reply_comment(self, payload, token, request_id, action, **kwarg):
        try:
            user = await get_user_obj(token)
            user_id = user.id
        
        except:
            await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'User object does not exist/token is invalid or expired'})

        post_id  = payload['post']
        parent_id = payload['parent']
        comment_data = {**payload, 'author': user_id}

        try:
            serialized_data = CommentSerializer(data=comment_data)
            await sync_to_async(serialized_data.is_valid)()
            if not serialized_data.is_valid():
                raise serializers.ValidationError(serialized_data.errors)
            
        except serializers.ValidationError as e:
            await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e.detail})

        try:
            post = await sync_to_async(Post.objects.get)(id=post_id)
            parent_comment  = await sync_to_async(Comment.objects.get)(id=parent_id, post=post_id)                

        except Post.DoesNotExist:
            await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Post object does not exist'})
        except Comment.DoesNotExist:
            await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Parent comment object does not exist'})

        comment = Comment(author=user, parent=parent_comment, text=payload['text'], post=post)
        await sync_to_async(comment.save)()

    
    @action()
    async def delete_comment_with_replies(self, payload, token, request_id, action, **kwarg):
        try:
            user = await get_user_obj(token)
            user_id = user.id
        
        except:
            await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'User object does not exist/token is invalid or expired'})

        try:
            comment_id = payload['id']
            comment = await sync_to_async(Comment.objects.get)(id=comment_id)

            try:
            # if comment.author.id == user_id: work in unsafe mode

                comment = await sync_to_async(Comment.objects.get)(id=comment_id, author__id=user_id)
                await sync_to_async(comment.delete)()

            except Comment.DoesNotExist:
                await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this commen'})

        except Comment.DoesNotExist:
            await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Comment object does not exist'})



        

        print(f'This is your payload {payload}')
    
    @action()
    async def partial_update_comment(self, payload, **kwargs):
        print(f'This is your payload {payload}')
    

    @model_observer(Comment)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)
    
    @model_change.serializer
    def model_serializer(self, instance, action, status_message=None, **kwargs):
        data = CommentSerializer(instance=instance).data

        match action.value:
            case 'create':
                if data['parent'] is None:
                    return {
                        'status': '200',
                        'status_message': "Comment was created",
                        'data': data,
                        'action': 'create_comment'
                    }
                else:
                    return {
                        'status': '200',
                        'status_message': "Reply comment was created",
                        'data': data,
                        'action': 'create_reply'
                    }
                
            case 'delete':
                return {
                    'status': '200',
                    'status_message': "Comment was deleted ",
                    'data': data,
                    'action': 'delete_comment'
                }






   

