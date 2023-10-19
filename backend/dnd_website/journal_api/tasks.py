# tasks.py

import time
from celery import Celery
from django.conf import settings
from .serializers import *
from .models import *
from django.utils.text import slugify

from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()



@shared_task
def postponed_publish(id):
    queryset = Post.objects.all().select_related('author').prefetch_related('tags', 'post_reactions', 'comments').get(pk=id)
    data = {'publish_datetime': None, 'is_publish': True}

    post_serializer = PostPartialUpdateSerializer(queryset, data=data, partial=True)
    if post_serializer.is_valid(raise_exception=True):
        post = post_serializer.save()  

    async_to_sync(channel_layer.group_send)('post', {'type': 'send_new_post'})


@shared_task
def like_post(post_author_id, post_author_username, post_reaction_id):
    post_reaction_obj = PostReaction.objects.get(pk=post_reaction_id)
    serializer = PostReactionSerializer(post_reaction_obj)
    data = serializer.data
    data['action'] = 'like_post'
    async_to_sync(channel_layer.group_send)(f'{post_author_username}_{post_author_id}', {'type': 'send_notification', 'data': data})
    


@shared_task
def leave_comment(post_author_id, post_author_username, comment_id):
    comment_obj = Comment.objects.get(pk=comment_id)
    serializer = NotificationCommentSerializer(comment_obj)
    data = serializer.data
    data['action'] = 'leave_comment'
    async_to_sync(channel_layer.group_send)(f'{post_author_username}_{post_author_id}', {'type': 'send_notification', 'data': data})


@shared_task
def leave_reply_comment(parent_user_id, parent_username, reply_comment_id):
    reply_comment_obj = Comment.objects.get(pk=reply_comment_id)
    serializer = NotificationCommentSerializer(reply_comment_obj)
    data = serializer.data
    data['action'] = 'leave_reply_comment'
    async_to_sync(channel_layer.group_send)(f'{parent_username}_{parent_user_id}', {'type': 'send_notification', 'data': data})


@shared_task
def like_comment(comment_author_id, comment_author_username, comment_reaction_id):
    comment_reaction_obj = CommentReaction.objects.get(pk=comment_reaction_id)
    serializer = CommentReactionSerializer(comment_reaction_obj)
    data = serializer.data
    data['action'] = 'like_comment'
    async_to_sync(channel_layer.group_send)(f'{comment_author_username}_{comment_author_id}', {'type': 'send_notification', 'data': data})