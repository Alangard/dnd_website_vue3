from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import *
from .permisions import *
from .serializers import *
from .models import *


# Account's views ###################################################

class AccountListView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAdminUser, )

class AccountUpdateView(generics.RetrieveUpdateAPIView):
    lookup_field = 'slug'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes=(IsOwnerOrReadOnly,)

class AccountDestroyView(generics.RetrieveDestroyAPIView):
    lookup_field = 'slug'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsOwnerOrAdmin, )
   
# Post's views ########################################################

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,)

class PostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class PostDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (IsOwnerOrAdmin,)

######################################################################

class ReactionCategoriesView(APIView):

    def get(self, request):
        categories = get_list_or_404(ReactionCategory)
        serializers = ReactionCategorySerializer(categories)
        return Response(serializers.data)

class ReactionListView(APIView):

    def get(self, request):
        reactions = get_list_or_404(Reaction)
        serializers = ReactionSerializer(reactions)
        return Response(serializers.data)

class PostReactionView(APIView):

    def get(self, request, pk):
        reactions = get_object_or_404(PostReaction, id=pk)
        serializers = PostReactionSerializer(reactions)
        return Response(serializers.data)
    

# Tags views ####################################################################
    
class TagListView(APIView):

    def get(self, request):
        tags = get_list_or_404(Tag)
        serializers = TagListSerializer(tags, many=True)
        return Response(serializers.data)
    
class TagDetailView(APIView):

    def get(self, request, slug):
        tag = get_object_or_404(Tag, slug__iexact = slug)
        serializers = TagDetailSerializer(tag)
        return Response(serializers.data)
    

    
###############################################################################

class CommentDetaliView(APIView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)
    

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