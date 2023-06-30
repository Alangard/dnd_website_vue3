from django.urls import path, include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),

    path('auth/jwt/create/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('posts/', PostListView.as_view(), name='posts-list-url'),
    path('post/<int:pk>/', PostReadUpdateView.as_view(), name='post-read_update-url'),
    path('post/create', PostCreateView.as_view(), name='post-create-url'),
    path('post/<int:pk>/delete/', PostDestroyView.as_view(), name='post-delete-url'),

    path('post/<int:post_id>/post_reactions/', PostReactionsListView.as_view(), name='post_reactions-url'),
    path('post/<int:post_id>/post_reaction/create/', PostReactionCreateView.as_view(), name='post_reaction-create-url'),
    path('post_reaction/<int:pk>/', PostReactionReadView.as_view(), name='post_reaction-read-url'),
    path('post_reaction/<int:pk>/update/', PostReactionUpdateView.as_view(), name='post_reaction-update-url'),
    path('post_reaction/<int:pk>/delete/', PostReactionDeleteView.as_view(), name='post_reaction-delete-url'),

    path('post/<int:post_id>/comments/', CommentsListView.as_view(), name='post_comments-url'),
    # path('post/<int:post_id>/comment/create/', name='post_comment_create-url'),
    # path('comment/<int:pk>/', name='comment-read-url'),
    # path('comment/<int:pk>/update/', name='comment-update-url'),
    # path('comment/<int:pk>/delete/', name='comment-delete-url'),

    path('tags/', TagsListView.as_view(), name='tags_list-url')
]
