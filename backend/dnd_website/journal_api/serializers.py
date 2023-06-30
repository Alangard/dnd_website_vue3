from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import *
from django.db.models import Count

## JWT serializers ################################################################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['user_data'] = {'username': self.user.username}
        return data

## Accounts serializers ############################################################

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [  'id',
                    "username", 
                    "password",
                    "avatar",
                    "email",
                    "favorites_reaction",
                    "recent_reaction",
                    "is_staff",
                    "is_active"]
        

        
class ShortAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "avatar"]

## Utils #########################################################################
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'replies']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent=obj)
        if replies:
            serializer = CommentSerializer(replies, many=True)
            return serializer.data
        return None

## Tags serializers ################################################################

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TagDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']

# Post reactions serializers ###################################################

class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = '__all__'
## Posts serilizers #################################################################

class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    # reactions = PostReactionSerializer(many=True, read_only=True)
    # author = ShortAccountSerializer(read_only=True)
    post_author_username = serializers.CharField(source='author.username', default='', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

# Post list preview on feed



class PostListReadSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    author = ShortAccountSerializer(read_only=True)
    num_comments = serializers.IntegerField()
    reacted = serializers.SerializerMethodField()
    commented = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'thumbnail', 'is_publish', 'publish_datetime',
                  'created_datetime', 'updated_datetime', 'body', 'tags', 'num_comments', 'reacted',
                  'commented', 'reactions']

    def get_reactions(self, obj):
        post_reactions = obj.reactions.all()
        num_likes = post_reactions.filter(reaction_type='like').count()
        num_dislikes = post_reactions.filter(reaction_type='dislike').count()
        total_reactions = post_reactions.count()
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

    def get_reacted(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            return obj.reactions.filter(author=user).exists()
        return False

    def get_commented(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            return obj.comments.filter(author=user).exists()
        return False
  
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'body', 'tags', 'is_publish', 'publish_datetime']


class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

