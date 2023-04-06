from rest_framework import serializers
from .models import *

class AccountDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Account
        fields = ["user_id", "username","avatar"]
    


class RecursiveCommentSerializer(serializers.Serializer):
    # Output recursive children comments
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
class FilterCommentListSerializer(serializers.ListSerializer):
    # Drop double comments
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
    

class CommentsSerializer(serializers.ModelSerializer):
    author = AccountDetailSerializer()
    children = RecursiveCommentSerializer(many=True)
    replies_count = serializers.IntegerField(source='get_childrens_comment_count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'author', 'status', 'created_at', 'report_reasons', 'comment_text', 'replies_count', 'children']
        list_serializer_class = FilterCommentListSerializer


class PostListSerializer(serializers.ModelSerializer):
    # Post list preview on feed
    tags = serializers.SlugRelatedField(slug_field='name', read_only = True, many=True)
    author = AccountDetailSerializer()
    comments_count = serializers.IntegerField(source='get_comments_count', read_only = True)

    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    # Detail info about one post
    tags = serializers.SlugRelatedField(slug_field='name', read_only = True, many=True)
    author = AccountDetailSerializer()
    comments = CommentsSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        include = ['tags', 'author']


class ReactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactionCategory
        fields = '__all__'


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = '__all__'

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']




