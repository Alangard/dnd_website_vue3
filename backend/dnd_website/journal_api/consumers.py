from .models import Post, Comment
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
    

class CommentConsumer(GenericAsyncAPIConsumer):
    queryset = Comment
    authentication_classes = (JWTAuthentication,)

    async def connect(self, **kwargs): 
        await self.model_change.subscribe() 
        await super().connect()  

    @model_observer(Comment) 
    async def model_change(self, message, observer=None, **kwargs): 
        serializer = self.get_serializer(message)  # Получаем соответствующий сериализатор
        await self.send_json(serializer.data) 

    def get_serializer(self, instance):
        method = self.scope['method']  # Получаем тип HTTP-запроса
        
        # Выбираем нужный сериализатор, устанавливаем нужные permissions и queryset в зависимости от типа запроса
        if method == 'GET':
            queryset = Comment.objects.all()  # Получаем все комментарии
            serializer_class = CommentListReadSerializer
            permissions = (permissions.AllowAny,)
            
        elif method == 'POST':
            queryset = Comment.objects.none()  # Нужно создать комментарий, поэтому queryset пустой
            serializer_class = CommentCreateSerializer
            permissions = (permissions.IsAuthenticated,)
            
        elif method == 'PUT':
            queryset = Comment.objects.filter(user=self.scope['user'])  # Получаем все комментарии пользователя
            serializer_class = CommentUpdateSerializer
            permissions = (permissions.IsAuthenticated,)
            
        elif method == 'DELETE':
            queryset = Comment.objects.filter(user=self.scope['user'])  # Получаем все комментарии пользователя
            serializer_class = CommentDeleteSerializer
            permissions = (permissions.IsAuthenticated,)
            
        self.permission_classes = permissions  # Устанавливаем нужные permissions
        self.queryset = queryset  # Устанавливаем нужный queryset
        serializer = serializer_class(instance=instance)
        return serializer

    @model_change.serializer 
    def model_serializer(self, instance, action, **kwargs): 
        serializer = self.get_serializer(instance)  # Получаем соответствующий сериализатор
        return dict(data=serializer.data, action=action.value)

