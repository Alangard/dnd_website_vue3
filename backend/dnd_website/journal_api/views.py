from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import datetime
from django.utils.dateparse import parse_datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from django_filters import rest_framework as DjangoFilters
from rest_framework.permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

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
            prefetch_related('tags','reactions','comments').\
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
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class PostDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsOwnerOrAdmin,)

    
 # Post reactions views #############################################################

class PostReactionsListView(generics.ListAPIView):
    serializer_class = PostReactionSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reaction_name', 'reaction_category']
    ordering_fields  = ['id', 'reaction_name', 'reaction_category']
    ordering = ['reaction_name']
  
    def get_queryset(self):
        return PostReaction.objects.filter(post_id = self.kwargs["post_id"])

class PostReactionCreateView(generics.CreateAPIView):
    serializer_class = PostReactionSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return PostReaction.objects.filter(post_id = self.kwargs["post_id"])
    
class PostReactionReadView(generics.RetrieveAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (AllowAny,)

class PostReactionUpdateView(generics.UpdateAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class PostReactionDeleteView(generics.DestroyAPIView):
    queryset = PostReaction.objects.all()
    serializer_class = PostReactionSerializer
    permission_classes = (IsOwnerOrReadOnly, )


# Commetns views ########################################################

# class CommentsListView(generics.ListAPIView):
#     # serializer_class = CommentsSerializer
#     permission_classes = (AllowAny,)
#     filter_backends = [DjangoFilters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     # search_fields = ['comment_text']
#     # ordering_fields  = ['id', 'reaction_name', 'reaction_category']
#     # ordering = ['reaction_name']
  
#     def get_queryset(self):
#         return Comment.objects.filter(post_id = self.kwargs["post_id"])

class CommentsListView(generics.ListAPIView):
    queryset = Comment.objects.filter(parent=None)    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    



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

    queryset = Comment.objects.all()    
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