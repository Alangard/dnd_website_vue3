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



# //////////////////////////////////////////////////////////////////////

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Post, Tag
from .permisions import IsOwnerOrAdmin, IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes
from django.utils.text import slugify

from django.utils.timezone import make_aware
from rest_framework.filters import BaseFilterBackend


class PostListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def filter_queryset(self, queryset):
        filter_backends = [DjangoFilters.DjangoFilterBackend]

        # Other condition for different filter backend goes here

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, view=self)
        return queryset


    def create(self, request, *args, **kwargs):
        self.serializer_class = PostCreateSerializer

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        # Парсим данные из запроса
        data = request.data
        data['author'] = request.user.id

        # Проверяем, есть ли все необходимые поля
        if 'title' not in data or 'description' not in data or 'body' not in data:
            return Response({"error": "Необходимо указать заголовок, описание и содержимое поста"},status=status.HTTP_400_BAD_REQUEST)

        # Создаем пост
        post_serializer = self.get_serializer(data=data)
        post_serializer.is_valid(raise_exception=True)
        post = post_serializer.save()

        # Проверяем, есть ли тэги в запросе
        if 'tags' in data:
            tags = data['tags']

            # Создаем и добавляем новые тэги к посту
            for tag_slug in tags:
                if Tag.objects.filter(slug = tag_slug).exists():
                    pass
                else:
                    tag_serializer = TagDetailSerializer(data={'name': tag_slug})
                    tag_serializer.is_valid(raise_exception=True)
                    tag = tag_serializer.save(slug=slugify(tag_slug))

            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
     
    def destroy(self, request, *args, **kwargs):
        self.serializer_class = PostDeleteSerializer
        self.permission_classes = [IsOwnerOrAdmin] # Объявляем permission_classes только для метода destroy

        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return Response({"error": "Необходима авторизация"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
             # Получаем id поста из kwargs
            post_id = kwargs.get('pk')
            if not self.queryset.filter(pk=post_id).exists():
                return Response({"error": "Пост не существует"}, status=status.HTTP_404_NOT_FOUND)

            instance = self.queryset.get(pk=post_id)

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
        else:
             # Получаем id поста из kwargs
            post_id = kwargs.get('pk')

            if not self.queryset.filter(pk=post_id).exists():
                return Response({"error": "Пост не существует"}, status=status.HTTP_404_NOT_FOUND)
            instance = self.queryset.get(pk=post_id)

            if request.user.is_staff or request.user.id == instance.author.id:

                # Парсим данные из запроса
                data = request.data

                # Используем частичное обновление модели с помощью аргумента partial=True
                post_serializer = self.get_serializer(instance, data=data, partial=True)
                post_serializer.is_valid(raise_exception=True)
                post_serializer.save()

                return Response(post_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Пользователь не является создателем поста или не имеет достаточно прав"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        
        # Получаем id поста из kwargs
        post_id = kwargs.get('pk')

        if not self.queryset.filter(pk=post_id).exists():
                return Response({"error": "Пост не существует"}, status=status.HTTP_404_NOT_FOUND)

        instance = self.queryset.get(pk=post_id)

        if request.user.is_authenticated and request.user.id == instance.author.id:
            self.serializer_class = PostDetailOwnerSerializer
            post_serializer = self.get_serializer(instance)
            return Response(post_serializer.data)
            
        else:
            if not self.queryset.filter(pk=post_id, is_publish=True).exists():
                return Response({"error": "Пост не существует или не опубликован"}, status=status.HTTP_404_NOT_FOUND)
            else:
                instance = self.queryset.filter(pk=post_id, is_publish=True).\
                    select_related('author').prefetch_related('tags','post_reactions','comments')
                # Передаем экземпляр поста сериализатору
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
                    instance = instance.filter(author__username__exact=params[param])

                if param == 'ordering' and params[param] != None:
                    ordering_list = params[param].split(',')
                    instance = instance.order_by(*ordering_list)

            return instance


        # Проверяем, авторизован ли пользователь
        if request.user.is_authenticated:
            # выдать post_instance с фидом пользователя 
            
            instance = self.queryset.filter(is_publish=True).\
                select_related('author').\
                prefetch_related('tags','post_reactions','comments')
            
            instance = myfilters(instance)
        

            # Пагинация
            page = self.paginate_queryset(instance)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                # serializer = self.get_serializer(self.filter_queryset(instance), page, many=True, context={"request": request})
                return self.get_paginated_response(serializer.data)

            # Сериализация
            # serializer = self.get_serializer(self.filter_queryset(instance), many=True, context={"request": request})
            serializer = self.get_serializer(instance, many=True)
            return Response(serializer.data)
            
        else:
            # выдать post_instance с фидом для всех
            return Response(status=status.HTTP_401_UNAUTHORIZED)


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


# Post's views ########################################################



class PostListView(generics.ListAPIView):

    def get_queryset(self):
        queryset = Post.objects.filter(is_publish=True).\
            select_related('author').\
            prefetch_related('tags','post_reactions','comments')
            # annotate(num_comments=Count('comments'))
        return queryset
    
    serializer_class = PostListReadSerializer
    permission_classess = [AllowAny,]
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class  = PostListFilter
    search_fields = ['title', 'description', 'body']
    ordering_fields  = ['id', 'created_datetime']
    ordering = ['-created_datetime']
    pagination_class = PostListPagination



# class PostCreateView(generics.CreateAPIView):
    # serializer_class = PostCreateSerializer
    # permission_classes = (IsAuthenticated,) 

    # async def post(self, request, *args, **kwargs):
    #     payload = kwargs['payload']

    #     if 'Authorization' in request.headers:
    #         auth_header = request.headers['Authorization']
    #         token = auth_header.split('Bearer ')[1]

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


class PostReadUpdateView(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        queryset = Post.objects.all().filter(is_publish=True).\
            select_related('author').\
            prefetch_related('tags','post_reactions','comments').\
            annotate(num_comments=Count('comments'))
        return queryset
    
    serializer_class = PostListReadSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class PostDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailOwnerSerializer
    permission_classes = (IsOwnerOrAdmin,)

    
# Post reactions views #############################################################

class PostReactionsListView(generics.ListAPIView):
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = PostReaction.objects.filter(post=post_id)
        return queryset
    
    serializer_class = PostReactionSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class  = PostReactionsFilter
    ordering_fields  = ['author__username', 'reacted_at',]
    ordering = ['-reacted_at']

class PostReactionCreateView(generics.CreateAPIView):
    serializer_class = PostReactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        post_id = kwargs["post_id"]

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(f"Post with id {post_id} does not exist", status=status.HTTP_404_NOT_FOUND)

        post_reaction = PostReaction.objects.create(
            reaction_type=request.data.get('reaction_type'),
            post=post,
            author=request.user
        )
        post.save()

        serializer = self.get_serializer(post_reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post_id'] = self.kwargs['post_id']
        return context
    
class PostReactionReadView(generics.RetrieveAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (AllowAny,)

class PostReactionUpdateView(generics.UpdateAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    
    def patch(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')

        if Post.objects.filter(id=post_id).exists():
            post_reaction = get_object_or_404(PostReaction, post_id=post_id, author=request.user)
            serializer = self.get_serializer(post_reaction, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostReactionDeleteView(generics.DestroyAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def destroy(self, request, *args, **kwargs):
        post_id = kwargs["post_id"]

        post = get_object_or_404(Post, id=post_id)
        post_reaction = get_object_or_404(PostReaction, post=post, author=request.user)

        post_reaction.delete()
        post.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

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