from rest_framework import serializers
from .models import *
    
## Accounts serializers ############################################################

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}
        fields = ["username", 
                  "email", 
                  "password",
                  "avatar",
                  "recent_reaction"]

## Utils #########################################################################

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
    author = AccountSerializer()
    children = RecursiveCommentSerializer(many=True)
    replies_count = serializers.IntegerField(source='get_childrens_comment_count', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'author', 'status', 'created_at', 'report_reasons', 'comment_text', 'replies_count', 'children']
        list_serializer_class = FilterCommentListSerializer
    

## Tags serializers ################################################################

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

## Posts serilizers #################################################################

class PostDetailSerializer(serializers.ModelSerializer):
    # Post list preview on feed
    tags = TagListSerializer(many=True, read_only=True)
    author = serializers.HiddenField(default = serializers.CurrentUserDefault())
    comments_count = serializers.IntegerField(source='get_comments_count', read_only = True)

    class Meta:
        model = Post
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'tags', 'title', 'description', 'body']


######################################################################################


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



class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

