from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *

# Create your views here.

class AccountDetailView(APIView):

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data)

class PostListView(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetailView(APIView):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
class ReactionCategoriesView(APIView):

    def get(self, request):
        categories = ReactionCategory.objects.all()
        serializers = ReactionCategorySerializer(categories)
        return Response(serializers.data)

class ReactionListView(APIView):

    def get(self, request):
        reactions = Reaction.objects.all()
        serializers = ReactionSerializer(reactions)
        return Response(serializers.data)

class PostReactionView(APIView):

    def get(self, request, pk):
        reactions = PostReaction.objects.get(id=pk)
        serializers = PostReactionSerializer(reactions)
        return Response(serializers.data)
    
class TagListView(APIView):

    def get(self, request):
        tags = Tag.objects.all()
        serializers = TagListSerializer(tags, many=True)
        return Response(serializers.data)
    
class TagDetailView(APIView):

    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact = slug)
        serializers = TagDetailSerializer(tag)
        return Response(serializers.data)
