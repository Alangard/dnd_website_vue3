from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/post_socket-server/', consumers.PostConsumer.as_asgi()),
    re_path(r'ws/notification_socket-server/', consumers.NotificationConsumer.as_asgi()),
    # re_path(r'ws/comment_socket-server/', consumers.CommentConsumer.as_asgi()),
]