from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from .models import *
import json


## JWT serializers ################################################################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)


        data['user_data'] = {'id': self.user.id, 'username': self.user.username, 'profile_name': self.user.profile_name, 'avatar': self.user.avatar}
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
                    "about_info",
                    "avatar",
                    "background_image",
                    "email",
                    "is_staff",
                    "is_active",
                    'confirmation_code']

class AccountSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [  'id',
                    "about_info",
                    "avatar",
                    "background_image",
                    "is_staff",
                    "is_active",
                    'confirmation_code']
        
class ProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'slug', 'avatar', 'background_image', 'profile_name', 'tagname', 'about_info']

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = "__all__"

class AccountStatsSerializer(serializers.ModelSerializer):
    stat = StatsSerializer()

    class Meta:
        model = AccountStats
        fields = ['stat', 'order']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        stat_representation = representation.pop('stat')
        representation.update(stat_representation)  # Объединяем словари
        return json.loads(json.dumps(representation))  # Преобразуем в строку и затем обратно в словарь

        
        

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
        fields = ["id", "profile_name", "avatar", "about_info"]

class AccountSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["id", "profile_name", "tagname", "username", "email", "avatar", "background_image", "about_info"]

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"

class SubscriptionSerializer(serializers.ModelSerializer):
    subscription_reciever = ShortAccountSerializer(read_only=True)
    subscriber = ShortAccountSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        match instance.notification_type:
            case "post_reaction":
                post_id = instance.post.id
                post_title = instance.post.title

                post_reaction__obj = PostReaction.objects.get(pk=instance.post_reaction.id)
                post_reaction__serializer_data = PostReactionSerializer(post_reaction__obj).data
                post_reaction__serializer_data['post'] = {'id': post_id, 'title': post_title}
                post_reaction__serializer_data['created_datetime'] = post_reaction__serializer_data.pop('reacted_at')

                data = {
                    'notification_type': 'post_reaction',
                    'seen': instance.seen,
                    'data': post_reaction__serializer_data,
                    'notification_id': instance.id,
                }
                return data
            
            case "post_comment":
                comment = instance.comment
                post_id = instance.post.id
                post_title = instance.post.title

                comment__obj = Comment.objects.get(pk=comment.id)
                comment__serializer_data = NotificationCommentSerializer(comment__obj).data
                comment__serializer_data['post'] = {'id': post_id, 'title': post_title}

                del comment__serializer_data['parent']

                data = {
                    'notification_type': 'post_comment',
                    'seen': instance.seen,
                    'data': comment__serializer_data,
                    'notification_id': instance.id,
                }
                return data
            
            case "comment_reply":
                comment = instance.comment
                comment__obj = Comment.objects.get(pk=comment.id)
                comment__serializer_data = NotificationCommentSerializer(comment__obj).data

                data = {
                    'notification_type': 'comment_reply',
                    'seen': instance.seen,
                    'data': comment__serializer_data,
                    'notification_id': instance.id,
                }
                return data
            
            case "comment_reaction":
                comment_reaction = instance.comment_reaction
                comment_reaction__author = instance.comment_reaction.author
                comment_reaction__obj = CommentReaction.objects.get(pk=comment_reaction.id)
                comment_reaction__author_obj = Account.objects.get(pk=comment_reaction__author.id)

                comment_reaction__serializer_data = CommentReactionSerializer(comment_reaction__obj).data
                comment_reaction__serializer_data['comment'] = {'id': instance.comment.id, 'text': instance.comment.text, 'post': instance.post.id}
                comment_reaction__serializer_data['author'] = ShortAccountSerializer(comment_reaction__author_obj).data
                comment_reaction__serializer_data['created_datetime'] = comment_reaction__serializer_data.pop('reacted_at')
          
                data = {
                    'notification_type': 'comment_reaction',
                    'seen': instance.seen,
                    'data': comment_reaction__serializer_data,
                    'notification_id': instance.id,
                }
                return data
            
            case "subscribe":
                subscription = instance.subscription
                subscription_data = SubscriptionSerializer(subscription).data
                subscription_data['created_datetime'] = subscription_data.pop('subscription_datetime')
                subscription_data['author'] = subscription_data.pop('subscriber')
                del subscription_data["subscription_reciever"]

                data= {
                    "notification_type": 'subscribe',
                    "seen": instance.seen,
                    "data" : subscription_data,
                    'notification_id': instance.id,
                }

                return data
            



## Comment Serializer #########################################################################

class ParentCommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)

    class Meta:  
        model = Comment  
        fields = ['id', 'author', 'text', 'created_datetime']
      
class CommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    parent = ParentCommentSerializer(read_only=True)  
    user_reaction = serializers.SerializerMethodField() 
    replies = serializers.SerializerMethodField() 
    comment_reactions = serializers.SerializerMethodField()
    
  
    class Meta:  
        model = Comment  
        fields = ['id', 'status', 'post', 'parent', 'author', 'text', 'created_datetime', 'updated_datetime', 'user_reaction', 'replies',  'comment_reactions']


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

class NotificationCommentSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    parent = ParentCommentSerializer(read_only=True)  
  
    class Meta:  
        model = Comment  
        fields = ['id', 'parent', 'author', 'text', 'post', 'created_datetime']

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
        fields = ['id','reaction_type', 'author', 'reacted_at', 'post']

class PostReactionsListSerializer(serializers.ModelSerializer):
    author = ShortAccountSerializer(read_only=True)
    
    class Meta:
        model = PostReaction
        fields = '__all__'


# Comment reactions serializers ###################################################

class CommentReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentReaction
        fields = ['id','reaction_type', 'author', 'reacted_at', 'comment', ]
    
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
        fields = ['id', 'author', 'title', 'description', 'thumbnail', 'body', 'tags', 'is_publish', 'is_draft', 'publish_datetime', 'allow_comments']


class ReportReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportReason
        fields= '__all__'
    

