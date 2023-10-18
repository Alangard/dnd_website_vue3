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
def like_post(user_id, username, post_reaction_id):
    post_reaction_obj = PostReaction.objects.get(pk = post_reaction_id)
    serializer = PostReactionSerializer(post_reaction_obj)
    async_to_sync(channel_layer.group_send)(f'{username}_{user_id}', {'type': 'send_notification', 'post_reaction_data': serializer.data})
    
