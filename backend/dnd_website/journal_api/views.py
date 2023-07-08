from django.shortcuts import get_object_or_404, get_list_or_404
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
from django.db.models import Count, OuterRef, Subquery, Prefetch, Value, CharField, F, prefetch_related_objects
from django.db import connection



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Post's views ########################################################

class PostListPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000

class PostListView(generics.ListAPIView):

    def get_queryset(self):
        queryset = Post.objects.filter(is_publish=True).\
            select_related('author').\
            prefetch_related('tags','post_reactions','comments').\
            annotate(num_comments=Count('comments'))
        return queryset
    
    serializer_class = PostListReadSerializer
    permission_classess = [IsAuthenticated]
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class  = PostListFilter
    search_fields = ['title', 'description', 'body']
    ordering_fields  = ['id', 'created_datetime']
    ordering = ['-created_datetime']
    pagination_class = PostListPagination

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) 

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
    serializer_class = PostDetailSerializer
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

        
class CommentDeleteDeleteBranchView(generics.DestroyAPIView):
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