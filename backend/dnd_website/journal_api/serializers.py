from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count

from .models import *


## JWT serializers ################################################################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['user_data'] = {'id': self.user.id, 'username': self.user.username, 'avatar': self.user.avatar}
        return data

## Accounts serializers ############################################################

class AccountSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        validate_password(value)
        return value

    class Meta:
        model = Account
        fields = [  'id',
                    "username", 
                    "password",
                    "avatar",
                    "email",
                    "is_staff",
                    "is_active",
                    'confirmation_code']
        

        
class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['confirmation_code']

class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = Account
        fields = ['email']

class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value)
        return value

    class Meta:
        model = Account
        fields = ['confirmation_code', 'new_password']
        
class ShortAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "avatar"]

## Comment Serializer #########################################################################

class CommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    user_reaction = serializers.SerializerMethodField()  
    replies = serializers.SerializerMethodField() 
    comment_reactions = serializers.SerializerMethodField()
    
  
    class Meta:  
        model = Comment  
        fields = ['id', 'status', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'user_reaction', 'replies', 'comment_reactions']
        read_only_fields = ['author', 'user_reaction', 'comment_reactions']


    def get_user_reaction(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
  
            if obj.comment_reactions.filter(author=user).exists():
                for comment in obj.comment_reactions.filter(author=user):
                    return {'reacted': True, 'reaction_type': comment.reaction_type}
            else:
                return {'reacted': False, 'reaction_type': ''}

    def get_replies(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            replies = Comment.objects.filter(parent=obj)
            if replies.exists():
                serializer = CommentSerializer(replies, many=True, context={'request': request})
                return serializer.data
        return None
    
    def get_comment_reactions(self, obj):
        comment_reactions = obj.comment_reactions.all()
        num_likes = comment_reactions.filter(reaction_type='like').count()
        num_dislikes = comment_reactions.filter(reaction_type='dislike').count()
        total_reactions = comment_reactions.count()
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

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
    author = ShortAccountSerializer(read_only=True)

    class Meta:
        model = PostReaction
        fields = ['id', 'reaction_type', 'author', 'reacted_at', 'post', ]
        read_only_fields = ['post']
    
    def create(self, validated_data):
        post_id = self.context.get('post_id')
        post = get_object_or_404(Post, id=post_id, reacted=False)
        validated_data['post'] = post
        return super().create(validated_data)

    
# class PostReactionDetailSerializer(serializers.ModelSerializer):
#     author = ShortAccountSerializer(read_only=True)
#     class Meta:
#         model = PostReaction
#         fields = ['id', 'reaction_type', 'author', 'reacted_at', 'post', ]

# Comment reactions serializers ###################################################

class CommentReactionSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    comment_reactions = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField() 

    class Meta:
        model = CommentReaction
        fields = ['id', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'replies', 'comment_reactions']
        read_only_fields = ['author', 'comment_reactions']
    
    def create(self, validated_data):
        comment_id = self.context.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, reacted=False)
        validated_data['comment'] = comment
        return super().create(validated_data)
    
    def get_comment_reactions(self, obj):
        comment_reactions = obj.comment_reactions.all()
        num_likes = comment_reactions.filter(reaction_type='like').count()
        num_dislikes = comment_reactions.filter(reaction_type='dislike').count()
        total_reactions = comment_reactions.count()
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

class CommentReactionDetailSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    class Meta:
        model = CommentReaction
        fields = ['id', 'reaction_type', 'author', 'reacted_at', 'comment', ]

    
## Posts serilizers #################################################################

class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class PostListReadSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    author = ShortAccountSerializer(read_only=True)
    user_reaction = serializers.SerializerMethodField()
    commented = serializers.SerializerMethodField()
    post_reactions = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'thumbnail', 'is_publish', 'publish_datetime',
                  'created_datetime', 'updated_datetime', 'body', 'tags', 'num_comments', 'user_reaction',
                  'commented', 'post_reactions']
        read_only_fields = ['tags','author', 'user_reaction', 'post_reactions']

    def get_post_reactions(self, obj):
        post_reactions = obj.post_reactions.all()
        num_likes = post_reactions.filter(reaction_type='like').count()
        num_dislikes = post_reactions.filter(reaction_type='dislike').count()
        total_reactions = num_likes + num_dislikes
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

    
    def get_user_reaction(self, obj):
        print(self.context)
        if 'request' in self.context:
            user = self.context['request'].user.id
            if obj.post_reactions.filter(author=user).exists():
                for post in obj.post_reactions.filter(author=user):
                    return {'reacted': True, 'reaction_type': post.reaction_type}
        return {'reacted': False, 'reaction_type': ''}

    def get_commented(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            return obj.comments.filter(author=user).exists()
        return False
    
    def get_num_comments(self, obj):
        return obj.comments.count()
  
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'body', 'tags', 'is_publish', 'publish_datetime']


class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

