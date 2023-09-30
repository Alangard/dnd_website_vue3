import base64
from django.shortcuts import get_object_or_404, get_list_or_404, render
from datetime import datetime
from django.utils.dateparse import parse_datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from django_filters import rest_framework as DjangoFilters
from rest_framework.permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
import re

from .filters import *
from .permisions import *
from .serializers import *
from .models import *
from django.db.models import Count



from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import json


from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.core.exceptions import ValidationError
from jwt import decode as jwt_decode
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

from rest_framework_simplejwt.authentication import JWTAuthentication


# //////////////////////////////////////////////////////////////////////

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, Tag
from .permisions import IsOwnerOrAdmin, IsOwnerOrReadOnly
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime

from PIL import Image




class PostListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostReactionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CommentsListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('tags', 'post_reactions', 'comments')

    def create(self, request, *args, **kwargs):
        self.serializer_class = PostCreateSerializer

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Проверяем, есть ли все необходимые поля
        required_fields = ['title', 'description', 'body']
        if request.data.get('is_draft') != 'true':
            if not all(field in request.data for field in required_fields):
                return Response({"error": "Необходимо указать заголовок, описание и содержимое поста"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'body': request.data.get('body'),
            'author': request.user.id,
        }

        for key, value in request.data.items():
            match key:
                case 'thumbnail':
                    data[key] = request.FILES.get('thumbnail')
                case 'tags':
                    data[key] = json.loads(request.data.get('tags', '[]'))
                case 'is_draft':
                    if request.data.get('is_draft') == 'true': data[key] = True 
                    else: data[key] = False
                case 'is_publish':
                    if request.data.get('is_publish') == 'true': data[key] = True 
                    else: data[key] = False
                case 'publish_datetime':
                    publish_datetime = parse_datetime(request.data.get('publish_datetime'))
                    data[key] = publish_datetime
                case _:
                    data[key] = request.data.get(key)

        
        post_serializer = self.get_serializer(data=data)
        if post_serializer.is_valid(raise_exception=True):

            if data.get('publish_datetime') != None and data.get('is_draft') == False: 
                print('make celery task')
            post = post_serializer.save()  

            # Создаем и добавляем новые тэги к посту
            if data.get('tags'):
                if data.get('tags') != []:
                    for tag in data['tags']:
                        tag, created = Tag.objects.get_or_create(name=tag, slug=slugify(tag))
                        post.tags.add(tag)
        
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Сериализация не пройдена"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        self.serializer_class = PostDeleteSerializer
        self.permission_classes = [IsOwnerOrAdmin]

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        post_id = kwargs.get('pk')
        post_exists = self.queryset.filter(pk=post_id).exists()
        instance = self.queryset.filter(pk=post_id).first()

        if not post_exists:
            return Response({"error": "Пост не существует"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user.id == instance.author.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Пользователь не является создателем поста или не имеет достаточно прав"}, status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = PostPartialUpdateSerializer
        self.permission_classes = [IsOwnerOrReadOnly] # Объявляем permission_classes только для метода destroy

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        post_id = kwargs.get('pk')
        instance = get_object_or_404(self.queryset, pk=post_id)

        # Получаем данные в необходимом формате
        data = {}

        for key, value in request.data.items():
            match key:
                case 'thumbnail':
                    data[key] = request.FILES.get('thumbnail')
                case 'tags':
                    data[key] = json.loads(request.data.get('tags', '[]'))
                case 'is_draft':
                    if request.data.get('is_draft') == 'true': data[key] = True 
                    else: data[key] = False
                case 'is_publish':
                    if request.data.get('is_publish') == 'true': data[key] = True 
                    else: data[key] = False
                case 'publish_datetime':
                    publish_datetime = parse_datetime(request.data.get('publish_datetime'))
                    data[key] = publish_datetime
                case _:
                    data[key] = request.data.get(key)

        if request.user.id == instance.author.id:
            post_serializer = self.get_serializer(instance, data=data, partial=True)
            if post_serializer.is_valid(raise_exception=True):

                if data.get('publish_datetime') != None and data.get('is_draft') == False: 
                    print('make celery task')
                post = post_serializer.save()  
                
            # Создаем и добавляем новые тэги к посту
            if data.get('tags'):
                if data.get('tags') != []:
                    for tag in data['tags']:
                        tag, created = Tag.objects.get_or_create(name=tag, slug=slugify(tag))
                        post.tags.add(tag)
                else:
                    post.tags.clear()

            return Response(post_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Пользователь не является создателем поста или не имеет достаточно прав"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailViewerSerializer
        params = request.query_params

        post_id = kwargs.get('pk')
        editable = bool(params['editable'])

        instance = get_object_or_404(self.queryset, pk=post_id)

        if editable and request.user.is_authenticated and request.user.id == instance.author.id:
            instance = self.queryset.get(pk=post_id)
            post_serializer = self.get_serializer(instance) 
            return Response(post_serializer.data)
        
            
        instance = self.queryset.get(pk=post_id, is_publish=True, is_draft=False)
        post_serializer = self.get_serializer(instance)
        return Response(post_serializer.data)
        
    def list(self, request, *args, **kwargs):
        self.serializer_class = PostListReadSerializer
        self.ordering = ['-created_datetime']
        self.pagination_class = PostListPagination

        def myfilters(queryset):
            instance = queryset
            params = request.query_params

            for param in params:

                if param == 'start_date' and params[param] != None:
                    start_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(created_datetime__gte=start_date_obj)

                if param == 'end_date' and params[param] != None:
                    end_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(created_datetime__lte = end_date_obj)

                if param == 'tags' and params[param] != None:
                    tags_list = params[param].split(',')
                    for tag in tags_list:
                        instance = instance.filter(tags__name=tag)

                if param == 'username' and params[param] != None:
                    username_list = params[param].split(',')
                    for username in username_list:
                        instance = instance.filter(author__username__exact=username)

                if param == 'ordering' and params[param] != None:
                    instance = instance.order_by(params[param])

                if param == 'search' and params[param] != None:
                    instance = instance.filter(Q(title__icontains=params[param]) | Q(description__icontains=params[param]))

            return instance

        instance = self.queryset.filter(is_publish=True, is_draft=False)
        instance = myfilters(instance)

        page = self.paginate_queryset(instance)
        if page is not None: 
            if request.user.is_authenticated: 
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                # return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        
class PostReactionViewSet(viewsets.ModelViewSet):
    queryset = PostReaction.objects.all()
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    serializer_class = PostReactionSerializer

    def create(self, request, *args, **kwargs):

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        post_id = request.data.get('post_id')
        try:
            Post.objects.all().get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Пост не существует"}, status=status.HTTP_404_NOT_FOUND)
        

        instance = self.queryset.filter(post=post_id, author__id=request.user.id).first()
        if instance is None:
    
            data = {
                'reaction_type': request.data.get('reaction_type'),
                'post': post_id,
                'author': request.user.id,
            }
            
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Сериализация не пройдена"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Реакция к посту уже имеется"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        reaction_id = kwargs.get('pk')
    
        try:
            instance = self.queryset.get(id=reaction_id)
        except PostReaction.DoesNotExist:
            return Response({"error": "Реакция к посту не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id == instance.author.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Пользователь не является создателем реакции"}, status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        reaction_id = kwargs.get('pk')
        
        try:
            instance = self.queryset.get(id=reaction_id)
        except PostReaction.DoesNotExist:
            return Response({"error": "Реакция к посту не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id == instance.author.id:
            serializer = self.serializer_class(instance, data={'reaction_type': request.data.get('reaction_type')}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Сериализация не пройдена"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Пользователь не является создателем реакции"}, status=status.HTTP_403_FORBIDDEN)
  
    # def list(self, request, *args, **kwargs):
        self.serializer_class = PostReactionsListSerializer
        self.ordering = ['-reacted_at']
        self.pagination_class = PostReactionPagination

        def myfilters(queryset):
            instance = queryset
            params = request.query_params

            for param in params:

                if param == 'post_id' and params[param] != None:
                    instance = instance.filter(post=params[param])

                if param == 'start_date' and params[param] != None:
                    start_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(reacted_at__gte=start_date_obj)

                if param == 'end_date' and params[param] != None:
                    end_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(reacted_at__lte = end_date_obj)

                if param == 'reaction_type' and params[param] != None:
                    instance = instance.filter(reaction_type__exact=params[param])

                if param == 'username' and params[param] != None:
                    instance = instance.filter(author__username__exact=params[param])

                if param == 'ordering' and params[param] != None:
                    ordering_list = params[param].split(',')
                    instance = instance.order_by(*ordering_list)

            return instance

        instance = myfilters(self.queryset)

        page = self.paginate_queryset(instance)
        if page is not None: 
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

class PostCommentsViewSet(viewsets.ModelViewSet):
    queryset =  Comment.objects.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializer

        post_id = request.data.get('post_id')

        try:
            post = Post.objects.all().get(id=post_id, is_draft = False, is_publish = True)
        except Post.DoesNotExist:
            return Response({"error": "Пост не существует или не опубликован"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if post.allow_comments == False:
            return Response({"error": "Создание комментариев к данном посту запрещено автором"}, status=status.HTTP_401_UNAUTHORIZED)
        
        comment_text = request.data.get('text')
        parent_id = request.data.get('parent')

        if parent_id is None:
            comment_obj = Comment.objects.create(
                status = 'n',
                post = post,
                author=request.user,
                text = comment_text
            )
        else:
            try:
                parent_comment = self.queryset.get(pk=parent_id)
                comment_obj = Comment.objects.create(
                    status = 'n',
                    post = post,
                    parent=parent_comment,
                    author=request.user,
                    text = comment_text
                )
            except Comment.DoesNotExist:
                return Response({"error": "Родительского комментария не существует"}, status=status.HTTP_400_BAD_REQUEST)
       
        serializer = self.get_serializer(comment_obj, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializer

        comment_id = kwargs.get('pk')

        # Проверяем, существует ли комментарий
        try:
            comment = self.queryset.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Комментарий не существует"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.is_staff or request.user.id == comment.author.id:
            if not comment.status=='n':
                return Response({"error": "Комментарий не может быть удалён, так как его статус 'normal'"}, status=status.HTTP_400_BAD_REQUEST)
            
            has_replies = comment.replies.exists()

            if request.user.id == comment.author.id:
                who_delete = 'author'
            elif request.user.is_staff:
                who_delete = 'staff'

            if(has_replies):
                comment.text = f'Comment was deleted by {who_delete}'
                comment.status = 'd'
                comment.save(update_fields=['text', 'status'])
                return Response(data={'changed_fields': {'text': comment.text, 'status': comment.status}}, status=status.HTTP_200_OK)
            else:
                comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
        else:
            return Response({"error": "Пользователь не является создателем поста или не имеет достаточно прав"}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializer
        
        comment_id = kwargs.get('pk')

        # Проверяем, существует ли комментарий
        try:
            comment = self.queryset.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Комментарий не существует"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not 'text' in request.data:
                return Response({"error": "Необходимо указать новый текст комментария"}, status=status.HTTP_400_BAD_REQUEST)
        
        text = request.data.get('text')

        if request.user.id == comment.author.id:
            serializer = self.get_serializer(comment, data={'text': text}, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save() 
                return Response(data={'text': serializer.data['text'], 'updated_datetime': serializer.data['updated_datetime']}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Пользователь не является создателем поста или не имеет достаточно прав"}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializer
        self.ordering = ['-created_datetime']
        self.pagination_class = CommentsListPagination

        post_id = self.request.query_params.get('post_id')
        

        try:
            post = Post.objects.all().get(id=post_id, is_draft = False, is_publish = True)
        except Post.DoesNotExist:
            return Response({"error": "Пост не существует или не опубликован"}, status=status.HTTP_400_BAD_REQUEST)
        
        def myfilters(queryset):
            instance = queryset
            params = request.query_params
            print(params)

            for param in params:

                if param == 'start_date' and params[param] != None:
                    start_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(created_datetime__gte=start_date_obj)

                if param == 'end_date' and params[param] != None:
                    end_date_obj = datetime.strptime(params[param], '%d/%m/%Y')
                    instance = instance.filter(created_datetime__lte = end_date_obj)

                if param == 'username' and params[param] != None:
                    username_list = params[param].split(',')
                    for username in username_list:
                        instance = instance.filter(author__username__exact=username)

                if param == 'ordering' and params[param] != None:
                    if params[param] == 'popularity':
                        instance = instance.annotate(reactions_count=Count('comment_reactions')).order_by('-reactions_count')
                    elif params[param] == 'date':
                        instance = instance.order_by('-created_datetime')

                if param == 'search' and params[param] != None:
                    instance = instance.filter(Q(text__icontains=params[param]) | Q(text__icontains=params[param]))

            return instance
        
        comments = self.queryset.filter(parent=None, post=post_id).select_related('author').prefetch_related('comment_reactions')
        instance = myfilters(comments)

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': self.request})
            data = {
                'allow_comments': post.allow_comments,
                'num_comments': Comment.objects.filter(post=post_id).count(),
                'comments': serializer.data, 
            }
            return self.get_paginated_response(data)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializer

        comment_id = kwargs.get('pk')

        # Проверяем, существует ли комментарий
        try:
            comment = self.queryset.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Комментарий не существует"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
  

class CommentReactionViewSet(viewsets.ModelViewSet):
    queryset = CommentReaction.objects.all()
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    serializer_class = CommentReactionSerializer

    def create(self, request, *args, **kwargs):

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        comment_id = request.data.get('comment_id')
        try:
            Comment.objects.all().get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Комментарий не существует"}, status=status.HTTP_404_NOT_FOUND)
        
        instance = self.queryset.filter(comment=comment_id, author__id=request.user.id).first()
        if instance is None:
            data = {
                'reaction_type': request.data.get('reaction_type'),
                'comment': comment_id,
                'author': request.user.id,
            }
            
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Сериализация не пройдена"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Реакция к комментарию уже имеется"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        reaction_id = kwargs.get('pk')
    
        try:
            instance = self.queryset.get(id=reaction_id)
        except CommentReaction.DoesNotExist:
            return Response({"error": "Реакция к комментарию не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id == instance.author.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Пользователь не является создателем реакции"}, status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):
         # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        reaction_id = kwargs.get('pk')
        
        try:
            instance = self.queryset.get(id=reaction_id)
        except CommentReaction.DoesNotExist:
            return Response({"error": "Реакция к комментарию не существует"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id == instance.author.id:
            serializer = self.serializer_class(instance, data={'reaction_type': request.data.get('reaction_type')}, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Сериализация не пройдена"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Пользователь не является создателем реакции"}, status=status.HTTP_403_FORBIDDEN)
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        self.serializer_class = TagListSerializer
        
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


def SendConfirmationCode(email):
    # user = get_object_or_404(Account, email = email)
    try:
        user = Account.objects.get(email = email)
    
        # Генерация и сохранение кода активации
        confirmation_code = default_token_generator.make_token(user)[::2][:6]
        user.confirmation_code = confirmation_code
        user.save()

        email_subject = 'Confirmation code'
        email_message = f'To execute the operation, insert this confirmation code {confirmation_code} in the "confirmation code" field'
        send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [email])
        
        return JsonResponse({'status': 'success'})
    
    except ObjectDoesNotExist:
        return HttpResponseNotFound(json.dumps({'status': 'error', 'message': 'User with this email address was not found'}), content_type="application/json")

class UserListView(APIView):
    def get(self, request):
        queryset = Account.objects.all()
        serializer = ShortAccountSerializer(queryset, many=True)
        return Response(serializer.data)

class SendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            resposne = SendConfirmationCode(email)
            return resposne
        else:
            return HttpResponseNotFound(json.dumps({'status': 'error', 'message': serializer.errors}), content_type="application/json")

class UserRegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Создание пользователя
            Account.objects.create_user(username=username, email=email, password=password)

            SendConfirmationCode(email)

            return JsonResponse({'status': 'success'})
        else:
            return HttpResponseBadRequest(json.dumps({'status': 'error', 'message': serializer.errors}), content_type="application/json")
        
        # JsonResponse()

class UserActivateView(APIView):
    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']

            try:
                user = Account.objects.get(confirmation_code=confirmation_code)
            except Account.DoesNotExist:
                return HttpResponseNotFound(json.dumps({'status': 'error', 'message': 'Invalid confirmation code'}), content_type="application/json")

            # Активация учетной записи пользователя
            user.confirmation_code = None
            user.is_active = True
            user.save()

            return JsonResponse({'status': 'success'})
        else:
            return HttpResponseBadRequest(json.dumps({'status': 'error', 'message': serializer.errors}), content_type="application/json")

class ResetPassword(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            response = SendConfirmationCode(email)

            return response
        else:
            return HttpResponseBadRequest(json.dumps({'status': 'error', 'message': serializer.errors}), content_type="application/json")

class ResetPasswordConfirm(APIView):
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = Account.objects.get(confirmation_code=confirmation_code)
            except Account.DoesNotExist:
                return HttpResponseNotFound(json.dumps({'status': 'error', 'message': 'Invalid confirmation code'}), content_type="application/json")

            # Активация учетной записи пользователя
            user.set_password = new_password
            user.confirmation_code = None
            user.save()

            return JsonResponse({'status': 'success'})
        else:
            return HttpResponseBadRequest(json.dumps({'status': 'error', 'message': serializer.errors}), content_type="application/json")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Post reactions views #############################################################

    




# Commetns views ########################################################

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

class CommentsListView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        comments = Comment.objects.filter(parent=None, post=post_id).\
            select_related('author').\
            prefetch_related('comment_reactions')
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        
        data = {
            'num_comments': Comment.objects.filter(post=post_id).count(),
            'comments': serializer.data,
        }
        
        return Response(data)   
    

class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)

        has_replies = comment.objects.filter(replies__id=comment_id).exists()


        if(has_replies):
            comment.text = 'Comment was deleted'
            comment.status = 'd'
            comment.save(update_fields=['text', 'status'])
        else:
            comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

        
class CommentDeleteBranchView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        comment_text = request.data.get('text')
       
        comment_obj = Comment.objects.create(
            status = 'n',
            post = post,
            author=request.user,
            text = comment_text
        )

        serializer = self.get_serializer(comment_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentCreateReplyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        parent_comment = get_object_or_404(Comment, id=comment_id)
        post = parent_comment.post
        comment_text = request.data.get('text')

        match_user_link = re.search(r'@(\w+),', comment_text)

        if match_user_link:
            comment_text_with_user_link = comment_text
        else:
            comment_text_with_user_link = f'@{parent_comment.author.username}, ' + comment_text
        
        comment_reply = Comment.objects.create(
            status = 'n',
            post = post,
            parent=parent_comment,
            author=request.user,
            text = comment_text_with_user_link
        )

        serializer = self.get_serializer(comment_reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def patch(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']
        comment_obj = get_object_or_404(Comment, id=comment_id)
        
        if 'text' in request.data and comment_obj.parent:
            comment_text = request.data['text']
            match_user_link = re.search(r'@(\w+),', comment_text)

            if match_user_link:
                comment_text_with_user_link = comment_text
            else:
                comment_text_with_user_link = f'@{comment_obj.parent.author.username}, ' + comment_text

            request.data['text'] = comment_text_with_user_link

        
        serializer = self.get_serializer(comment_obj, data=request.data, partial=True)
            
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


# Comment reactions views #############################################################

class CommentReactionsListView(generics.ListAPIView):
    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        queryset = CommentReaction.objects.filter(comment=comment_id)
        return queryset
    
    serializer_class = CommentReactionSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class  = CommentReactionsFilter
    ordering_fields  = ['author__username', 'reacted_at',]
    ordering = ['-reacted_at']

class CommentReactionCreateView(generics.CreateAPIView):
    serializer_class = CommentReactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        comment_id = kwargs['comment_id']

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(f"Comment with id {comment_id} does not exist", status=status.HTTP_404_NOT_FOUND)

        comment_reaction = CommentReaction.objects.create(
            reaction_type=request.data.get('reaction_type'),
            comment=comment_id,
            author=request.user
        )
        comment.save()

        serializer = self.get_serializer(comment_reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['comment_id'] = self.kwargs['comment_id']
        return context
    
class CommentReactionReadView(generics.RetrieveAPIView):
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = (AllowAny,)

class CommentReactionUpdateView(generics.UpdateAPIView):
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    
    def patch(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')

        if Comment.objects.filter(id=comment_id).exists():
            comment_reaction = get_object_or_404(CommentReaction, comment=comment_id, author=request.user)
            serializer = self.get_serializer(comment_reaction, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentReactionDeleteView(generics.DestroyAPIView):
    queryset = CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs["comment_id"]

        comment = get_object_or_404(Comment, id=comment_id)
        comment_reaction = get_object_or_404(PostReaction, comment=comment, author=request.user)

        comment_reaction.delete()
        comment.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Tags views ####################################################################
    
class TagsListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['name']
    search_fields = ['name']
    ordering_fields  = ['id', 'name']
    ordering = ['name']
    pagination_class = None



# class TagListView(APIView):

#     def get(self, request):
#         tags = get_list_or_404(Tag)
#         serializers = TagListSerializer(tags, many=True)
#         return Response(serializers.data)
    
# class TagDetailView(APIView):

#     def get(self, request, slug):
#         tag = get_object_or_404(Tag, slug__iexact = slug)
#         serializers = TagDetailSerializer(tag)
#         return Response(serializers.data)
    

    
###############################################################################



class CommentDetaliView(APIView):

    # def get(self, request, pk):
    #     comment = get_object_or_404(Comment, id=pk)
    #     serializer = CommentsSerializer(comment)
    #     return Response(serializer.data)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     # Передаем параметры маршрута в контекст сериализатора
    #     context.update(self.kwargs)
    #     return context

    # queryset = Comment.objects.all()    

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        parent_id = self.kwargs.get('parent_id')
        if parent_id:
            queryset = Comment.objects.filter(post=post_id, parent=parent_id)
        else:
            queryset = Comment.objects.filter(post=post_id, parent=None)
        return queryset


    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class ReportReasonsView(APIView):
    
    def get(self, request):
        report_reasons = get_list_or_404(ReportReason)
        serializer = ReportReasonSerializer(report_reasons, many=True)
        return Response(serializer.data)
    

class ReportReasonDetailView(APIView):

    def get(self, request, pk):
        report_reason = get_object_or_404(ReportReason, id=pk)
        serializer = ReportReasonSerializer(report_reason)
        return Response(serializer.data)