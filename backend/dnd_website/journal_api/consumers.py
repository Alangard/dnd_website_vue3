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

async def test(self, request_id, token, payload):
    try:
        user = await get_user_obj(token)
        user_id = user.id

        post_id  = payload['post']
        parent_id = payload['parent']
        comment_id = payload['id']
        comment_data = {**payload, 'author': user_id}

        serialized_data = CommentSerializer(data=comment_data)
        await sync_to_async(serialized_data.is_valid)()
        if not serialized_data.is_valid():
            raise serializers.ValidationError(serialized_data.errors)
        
        post = await sync_to_async(Post.objects.get)(id=post_id)
        parent_comment  = await sync_to_async(Comment.objects.get)(id=parent_id, post=post_id) 

        try:
            comment = await sync_to_async(Comment.objects.get)(id=comment_id, post=post_id)         
        except Comment.DoesNotExist:
            await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Comment object does not exist'})
            return


    except serializers.ValidationError as e:
        await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e.detail})
    
    except Post.DoesNotExist:
        await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Post object does not exist'})

    except Comment.DoesNotExist:
        await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Parent comment object does not exist'})

    except:
        await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'User object does not exist/token is invalid or expired'})

    return {'user': user, 'post': post, 'parent_comment': parent_comment, 'comment': comment}



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
    async def create_comment(self, payload, token, request_id, action, **kwarg):
        try:
            response = await test(self=self, request_id=request_id, token=token, payload=payload)
            comment = Comment(author=response['user'], text=payload['text'], post=response['post'])
            await sync_to_async(comment.save)()
        except Exception as e:
            return

    @action()
    async def create_reply_comment(self, payload, token, request_id, action, **kwarg):
        try:
            response = await test(self=self, request_id=request_id, token=token, payload=payload)
            comment = Comment(author=response['user'], parent=response['parent_comment'], text=payload['text'], post=response['post'])
            await sync_to_async(comment.save)()
        except Exception as e:
            return

    
    @action()
    async def delete_comment(self, payload, token, request_id, action, **kwarg):
        try:
            response = await test(self=self, request_id=request_id, token=token, payload=payload)
            comment = response['comment']

            if comment.author.id == response['user'].id:
                    if comment.replies.exists():
                        comment.status = 'd'
                        comment.text = '*this comment was deleted by author*'
                        await sync_to_async(comment.save)()
                    else:
                        await sync_to_async(comment.delete)()
            else:
                await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})    

        except Exception as e:
            return
        

    @action()
    async def partial_update_comment(self, payload, token, request_id, action, **kwarg):
        try:
            response = await test(self=self, request_id=request_id, token=token, payload=payload)
            comment = response['comment']

            if comment.author.id == response['user'].id:
                comment.text = payload['text']
                await sync_to_async(comment.save)()
            else:
                await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})

        except Exception as e:
            return


    @action()
    async def ban_comment(self, payload, token, request_id, action, **kwarg):
        try:
            response = await test(self=self, request_id=request_id, token=token, payload=payload)
            comment = response['comment']
            user = response['user']

            if comment.author.id != user.id:
                if user.is_staff:
                    comment.status = 'b'
                    comment.text = f'*this comment was banned by {user.username}*'
                    await sync_to_async(comment.save)()
                else:
                    await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are dont have permissions'})  
            else:
                await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})   

        except Exception as e:
            return


    # @action()
    # async def delete_comment_with_replies(self, payload, token, request_id, action, **kwarg):
    #     try:
    #         response = await test(self, request_id, token, payload)
    #         comment = response['comment']

    #         if comment.author.id == response['user'].id:
    #             await sync_to_async(comment.delete)()
    #         else:
    #             await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'}) 

    #     except Exception as e:
    #         return

    
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
        
            case 'update':
                return {
                    'status': '200',
                    'status_message': "Comment was updated",
                    'data': data,
                    'action': 'update_comment'
                }
            







   

