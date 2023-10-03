from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from .models import *

from django.db.models import Count, Q, Sum


## JWT serializers ################################################################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Получить полный URL-адрес изображения
        request = self.context.get('request')
        if self.user.avatar:
            image_url = f"{ request.scheme}://{get_current_site(request).domain}{self.user.avatar.url}"
        else:
            image_url = None

        data['user_data'] = {'id': self.user.id, 'username': self.user.username, 'avatar': image_url}
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

class SubscriptionListSerializer(serializers.ModelSerializer):
    user = ShortAccountSerializer(read_only=True)
    subscribed_to = ShortAccountSerializer(read_only=True, many=True)
    subscribers = serializers.SerializerMethodField() 

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'subscribed_to', 'subscribers']
        read_only_fields = ['user', 'subscribed_to', 'subscribers']

    def get_subscribers(self, obj):
        request_user = self.context['request'].user.id
        subscriptions = Subscription.objects.filter(subscribed_to=request_user)
        subscribers = [subscription.user for subscription in subscriptions]
        serializer = ShortAccountSerializer(subscribers, many=True)
        return serializer.data



## Comment Serializer #########################################################################

class ParentCommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)

    class Meta:  
        model = Comment  
        fields = ['id', 'author']
      

class CommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    parent = ParentCommentSerializer(read_only=True)  
    user_reaction = serializers.SerializerMethodField() 
    replies = serializers.SerializerMethodField() 
    comment_reactions = serializers.SerializerMethodField()
    
  
    class Meta:  
        model = Comment  
        fields = ['id', 'status', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'user_reaction', 'replies', 'comment_reactions']


    def get_user_reaction(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            user = request.user.id
            if obj.comment_reactions.filter(author=user).exists():
                for comment in obj.comment_reactions.filter(author=user):
                    return {'reacted': True, 'reaction_type': comment.reaction_type, 'id': comment.id}
        return {'reacted': False, 'reaction_type': '', 'id': ''}
    

    def get_replies(self, obj):
        if 'request' in self.context:
            replies = Comment.objects.filter(parent=obj)
            if replies.exists():
                data = []
                for reply in replies:
                    parent_comment = reply.parent
                    parent_data = {
                        'id': parent_comment.id,
                        'author': {
                            'id': parent_comment.author.id,
                            'username': parent_comment.author.username,
                            'avatar': parent_comment.author.avatar.url if parent_comment.author.avatar else None
                        }
                    }
                    reply_data = CommentSerializer(reply, context=self.context).data
                    reply_data['parent'] = parent_data
                    data.append(reply_data)
                return data
        return None
    
    def get_comment_reactions(self, obj):
        comment_reactions = obj.comment_reactions.all()
        num_likes = comment_reactions.filter(reaction_type='like').count()
        num_dislikes = comment_reactions.filter(reaction_type='dislike').count()
        total_reactions = num_likes + num_dislikes
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

    class Meta:
        model = PostReaction
        fields = ['id','reaction_type', 'author', 'reacted_at', 'post', ]

class PostReactionsListSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    
    class Meta:
        model = PostReaction
        fields = '__all__'
    
    # def create(self, validated_data):
    #     post_id = self.context.get('post_id')
    #     post = get_object_or_404(Post, id=post_id, reacted=False)
    #     validated_data['post'] = post
    #     return super().create(validated_data)

    
# class PostReactionDetailSerializer(serializers.ModelSerializer):
#     author = ShortAccountSerializer(read_only=True)
#     class Meta:
#         model = PostReaction
#         fields = ['id', 'reaction_type', 'author', 'reacted_at', 'post', ]

# Comment reactions serializers ###################################################

class CommentReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentReaction
        fields = ['id','reaction_type', 'author', 'reacted_at', 'comment', ]


# class CommentReactionSerializer(serializers.ModelSerializer):
#     author = ShortAccountSerializer(read_only=True)
#     comment_reactions = serializers.SerializerMethodField()
#     replies = serializers.SerializerMethodField() 

#     class Meta:
#         model = CommentReaction
#         fields = ['id', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'replies', 'comment_reactions']
#         read_only_fields = ['author', 'comment_reactions']
    
#     def create(self, validated_data):
#         comment_id = self.context.get('comment_id')
#         comment = get_object_or_404(Comment, id=comment_id, reacted=False)
#         validated_data['comment'] = comment
#         return super().create(validated_data)
    
#     def get_comment_reactions(self, obj):
#         comment_reactions = obj.comment_reactions.all()
#         num_likes = comment_reactions.filter(reaction_type='like').count()
#         num_dislikes = comment_reactions.filter(reaction_type='dislike').count()
#         total_reactions = comment_reactions.count()
#         return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

# class CommentReactionDetailSerializer(serializers.ModelSerializer):
#     author = ShortAccountSerializer(read_only=True)
#     class Meta:
#         model = CommentReaction
#         fields = ['id', 'reaction_type', 'author', 'reacted_at', 'comment', ]

    
## Posts serilizers #################################################################

class PostDetailOwnerSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    author = ShortAccountSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

class PostDetailViewerSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    author = ShortAccountSerializer(read_only=True)
    user_reaction = serializers.SerializerMethodField()
    post_reactions = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'thumbnail', 'is_publish', 'publish_datetime',
                  'created_datetime', 'updated_datetime', 'body', 'tags', 'user_reaction','post_reactions']
        read_only_fields = ['tags','author', 'user_reaction', 'post_reactions']

    def get_post_reactions(self, obj):
        post_reactions = obj.post_reactions.all()
        num_likes = post_reactions.filter(reaction_type='like').count()
        num_dislikes = post_reactions.filter(reaction_type='dislike').count()
        total_reactions = num_likes + num_dislikes
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}

    
    def get_user_reaction(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            if obj.post_reactions.filter(author=user).exists():
                for post in obj.post_reactions.filter(author=user):
                    return {'reacted': True, 'reaction_type': post.reaction_type, 'id': post.id}
        return {'reacted': False, 'reaction_type': '', 'id': ''}

class PostDeleteSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id']

class PostPartialUpdateSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    title = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    tags = TagListSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'thumbnail', 'body', 'tags', 'is_publish', 'is_draft', 'publish_datetime', 'allow_comments']

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

    def get_post_reactions(self, obj):
        post_reactions = obj.post_reactions.all().only('reaction_type')
        num_likes = post_reactions.filter(reaction_type='like').count()
        num_dislikes = post_reactions.filter(reaction_type='dislike').count()
        total_reactions = num_likes + num_dislikes
        return {'num_likes': num_likes, 'num_dislikes': num_dislikes, 'total_reactions': total_reactions}
    
    def get_user_reaction(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            if obj.post_reactions.filter(author=user).exists():
                for post in obj.post_reactions.filter(author=user):
                    return {'reacted': True, 'reaction_type': post.reaction_type, 'id': post.id}
        return {'reacted': False, 'reaction_type': '', 'id': ''}

    def get_commented(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user.id
            return obj.comments.filter(author=user).exists()
        return False
    
    def get_num_comments(self, obj):
        return obj.comments.count()

  
class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'thumbnail', 'body', 'tags', 'is_publish', 'is_draft', 'publish_datetime', 'allow_comments']


class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

