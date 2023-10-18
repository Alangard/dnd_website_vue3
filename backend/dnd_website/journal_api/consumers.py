from .models import Post, Comment, Account, Tag
from .serializers import PostListReadSerializer, CommentSerializer, PostCreateSerializer, PostDeleteSerializer, PostPartialUpdateSerializer
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
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
from django.db.models import F
from channels.generic.websocket import AsyncWebsocketConsumer
import json


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

# async def consumer_rules_checker(self, request_id, token, payload):
    try:

        user = await get_user_obj(token)
        user_id = user.id
        post_id  = payload['post']
        parent_id = payload['parent'] if 'parent' in payload else None
        comment_id = payload['id']
        comment_data = {**payload, 'author': user_id}

        serialized_data = CommentSerializer(data=comment_data)
        await sync_to_async(serialized_data.is_valid)()
        if not serialized_data.is_valid():
            raise serializers.ValidationError(serialized_data.errors)
        
        post = await sync_to_async(Post.objects.get)(id=post_id)

        if parent_id is not None:
            parent_comment  = await sync_to_async(Comment.objects.get)(id=parent_id, post=post_id) 
        else:
            parent_comment = None


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

    else:
        return {'user': user, 'post': post, 'parent_comment': parent_comment, 'comment': comment}


# class UserNotFound(Exception):
#     pass

# class UserNotOwner(Exception):
#     pass


# class PostConsumer(GenericAsyncAPIConsumer):
#     async def connect(self, **kwargs): 
#         await self.model_change.subscribe() 
#         await super().connect() 


#     @action()
#     async def create_post(self, payload, token, request_id, action, **kwarg):
#         try:
#             user = await get_user_obj(token)
#             if user is None:
#                 raise UserNotFound
#             else:
#                 user_id = user.id
#                 post_data = {**payload, 'author': user_id}
#                 serialized_data =  PostCreateSerializer(data=post_data)

#                 await sync_to_async(serialized_data.is_valid)()
#                 if not serialized_data.is_valid():
#                     raise serializers.ValidationError(serialized_data.errors)     
                
#                 try:
#                     post = Post(author=user, title=payload['title'], description=payload['description'],  
#                                 body=payload['body'],  is_publish=payload['is_publish'],  publish_datetime=payload['publish_datetime'])
                
#                     await sync_to_async(post.save)()

#                     for tag_name in payload['tags']:
#                         try:
#                             tag = await sync_to_async(Tag.objects.get)(name=tag_name)
#                         except Tag.DoesNotExist:
#                             tag = await sync_to_async(Tag.objects.create)(name=tag_name)
#                         await sync_to_async(post.tags.add)(tag)

#                 except ValidationError as e:
#                     await self.send_json({'request_id': request_id, 'status': '500', 'error_message': 'Your model instance has not been saved'})
                    

#         except (InvalidToken, TokenError) as e:
#             await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'Token is invalid or expired'})
#         except UserNotFound as e:
#             await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'User object does not exist'})
#         except serializers.ValidationError as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': f'Something wrong with serialization.{e.detail}'})
#         except Exception as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e})


#     @action()
#     async def delete_post(self, payload, token, request_id, action, **kwarg):
#         try:
#             user = await get_user_obj(token)
#             if user is None:
#                 raise UserNotFound
#             elif user.id != payload['author'].id:
#                 raise UserNotOwner
#             else:
#                 user_id = user.id
#                 post_data = {**payload, 'author': user_id}
#                 serialized_data =  PostDeleteSerializer(data=post_data)

#                 await sync_to_async(serialized_data.is_valid)()
#                 if not serialized_data.is_valid():
#                     raise serializers.ValidationError(serialized_data.errors)     
                
#                 try:
#                     post = await sync_to_async(Post.objects.get)(id=payload['id'])
                    
#                     try:
#                         await sync_to_async(post.delete)()
#                     except ProtectedError as e:
#                         await self.send_json({'request_id': request_id, 'status': '404', 'error_message': f'Your model instance has not been deleted. {e}'})

#                 except Post.DoesNotExist:
#                     await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Post object does not exist'})

#         except (InvalidToken, TokenError) as e:
#             await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'Token is invalid or expired'})
#         except UserNotFound as e:
#             await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'User object does not exist'})
#         except UserNotOwner as e:
#             await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'User  not owner of this post and dont have permission'})
#         except serializers.ValidationError as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': f'Something wrong with serialization.{e.detail}'})
#         except Exception as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e})


#     @action()
#     async def partial_update_post(self, payload, token, request_id, action, **kwarg):

#         try:
#             user = await get_user_obj(token)
#             if user is None:
#                 raise UserNotFound
#             elif user.id != payload['author']['id']:
#                 raise UserNotOwner
#             else:
#                 user_id = user.id
#                 post_data = {**payload, 'author': user_id}
#                 serialized_data =  PostPartialUpdateSerializer(data=post_data)

#                 await sync_to_async(serialized_data.is_valid)()
#                 if not serialized_data.is_valid():
#                     raise serializers.ValidationError(serialized_data.errors)     
                
#                 try:
#                     post = await sync_to_async(Post.objects.get)(id=payload['id'])

#                     try:
#                         # new_payload = payload.copy()
#                         # data = {**new_payload, 'author': user, 'created_datetime': datetime.now()}
#                         # post = Post(**data)
#                         # await sync_to_async(post.save)()

#                         # post.description = payload['description']
#                         # post.title = payload['title']

#                         payload.pop('author')

#                         post = Post.objects.get(id=payload['id'])
#                         for key, value in payload.items():
#                             setattr(post, key, value)

#                         await sync_to_async(post.save)()



#                         # post = await sync_to_async(Post.objects.filter)(id=payload['id'])
#                         # await sync_to_async(post.update)(**data)
#                     except ValidationError as e:
#                         await self.send_json({'request_id': request_id, 'status': '500', 'error_message': 'Your model instance has not been saved'})
                    
#                 except Post.DoesNotExist:
#                     await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'Post object does not exist'})

#         except (InvalidToken, TokenError) as e:
#             await self.send_json({'request_id': request_id, 'status': '401', 'error_message': 'Token is invalid or expired'})
#         except UserNotFound as e:
#             await self.send_json({'request_id': request_id, 'status': '404', 'error_message': 'User object does not exist'})
#         except UserNotOwner as e:
#             await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'User  not owner of this post and dont have permission'})
#         except serializers.ValidationError as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': f'Something wrong with serialization.{e.detail}'})
#         except Exception as e:
#             await self.send_json({'request_id': request_id, 'status': '400', 'error_message': e})


#     @model_observer(Post)
#     async def model_change(self, message, observer=None, **kwargs):
#         await self.send_json(message)
    
#     @model_change.serializer
#     def model_serializer(self, instance, action, status_message=None, **kwargs):
#         data = PostListReadSerializer(instance=instance).data

#         match action.value:
#             case 'create':

#                 if data.get('is_publish') == True and (data.get('is_draft') == False or data.get('is_draft') is None):
#                     return {
#                         'status': '200',
#                         'status_message': "Post has been created",
#                         'action': 'create_post'
#                     }
            
#         return {
#                 'status': '200',
#                 'data': data,
#                 'action': action.value
#             }



# class CommentConsumer(GenericAsyncAPIConsumer):

#     async def connect(self, **kwargs): 
#         await self.model_change.subscribe() 
#         await super().connect()  

#     @action()
#     async def create_comment(self, payload, token, request_id, action, **kwarg):
#         try:
#             response = await consumer_rules_checker(self=self, request_id=request_id, token=token, payload=payload)
#             comment = Comment(author=response['user'], text=payload['text'], post=response['post'])
#             await sync_to_async(comment.save)()
#         except Exception as e:
#             return

#     @action()
#     async def create_reply_comment(self, payload, token, request_id, action, **kwarg):
#         try:
#             response = await consumer_rules_checker(self=self, request_id=request_id, token=token, payload=payload)
#             comment = Comment(author=response['user'], parent=response['parent_comment'], text=payload['text'], post=response['post'])
#             await sync_to_async(comment.save)()
#         except Exception as e:
#             return

    
#     @action()
#     async def delete_comment(self, payload, token, request_id, action, **kwarg):
#         try:
#             response = await consumer_rules_checker(self=self, request_id=request_id, token=token, payload=payload)
#             comment = response['comment']

#             if comment.author.id == response['user'].id:
#                     if comment.replies.exists():
#                         comment.status = 'd'
#                         comment.text = '*this comment was deleted by author*'
#                         await sync_to_async(comment.save)()
#                     else:
#                         await sync_to_async(comment.delete)()
#             else:
#                 await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})    

#         except Exception as e:
#             return
        

#     @action()
#     async def partial_update_comment(self, payload, token, request_id, action, **kwarg):
#         try:
#             response = await consumer_rules_checker(self=self, request_id=request_id, token=token, payload=payload)
#             comment = response['comment']

#             if comment.author.id == response['user'].id:
#                 comment.text = payload['text']
#                 await sync_to_async(comment.save)()
#             else:
#                 await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})

#         except Exception as e:
#             return


#     @action()
#     async def ban_comment(self, payload, token, request_id, action, **kwarg):
#         try:
#             response = await consumer_rules_checker(self=self, request_id=request_id, token=token, payload=payload)
#             comment = response['comment']
#             user = response['user']

#             if comment.author.id != user.id:
#                 if user.is_staff:
                    
#                     comment.status = 'b'
#                     comment.text = f'*this comment was banned by {user.username}*'
#                     await sync_to_async(comment.save)()
#                 else:
#                     await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are dont have permissions'})  
#             else:
#                 await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'})   

#         except Exception as e:
#             return


#     # @action()
#     # async def delete_comment_with_replies(self, payload, token, request_id, action, **kwarg):
#     #     try:
#     #         response = await consumer_rules_checker(self, request_id, token, payload)
#     #         comment = response['comment']

#     #         if comment.author.id == response['user'].id:
#     #             await sync_to_async(comment.delete)()
#     #         else:
#     #             await self.send_json({'request_id': request_id, 'status': '403', 'error_message': 'You are not owner of this comment'}) 

#     #     except Exception as e:
#     #         return

    
#     @model_observer(Comment)
#     async def model_change(self, message, observer=None, **kwargs):
#         await self.send_json(message)
    
#     @model_change.serializer
#     def model_serializer(self, instance, action, status_message=None, **kwargs):
#         data = CommentSerializer(instance=instance).data

#         match action.value:
#             case 'create':
#                 if data['parent'] is None:
#                     return {
#                         'status': '200',
#                         'status_message': "Comment was created",
#                         'data': data,
#                         'action': 'create_comment'
#                     }
#                 else:
#                     return {
#                         'status': '200',
#                         'status_message': "Reply comment was created",
#                         'data': data,
#                         'action': 'create_reply'
#                     }
                
#             case 'delete':
#                 return {
#                     'status': '200',
#                     'status_message': "Comment was deleted ",
#                     'data': data,
#                     'action': 'delete_comment'
#                 }
        
#             case 'update':
#                 return {
#                     'status': '200',
#                     'status_message': "Comment was updated",
#                     'data': data,
#                     'action': 'update_comment'
#                 }
            
#         return {
#                 'status': '200',
#                 'data': data,
#                 'action': action.value
#             }

            
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
            'data': event['post_reaction_data'],
            'action': 'like_comment'
        }

        await self.send(json.dumps(data))






   

