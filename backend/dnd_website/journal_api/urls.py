from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'post', PostViewSet, basename='post')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = [
    # path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    

    
    path('auth/user/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/user/activation/', UserActivateView.as_view(), name='user_activate'),
    path('auth/user/reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('auth/user/reset_password_confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confrim'),
    path('auth/user/send_confirmation_code/', SendConfirmationCodeView.as_view(), name='send_confirmation_code'),

    path('auth/jwt/create/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('posts/', PostListView.as_view(), name='posts-list-url'),
    path('post/<int:pk>/', PostReadUpdateView.as_view(), name='post-read_update-url'),
    # path('post/create/', PostCreateView.as_view(), name='post-create-url'),
    path('post/<int:pk>/delete/', PostDestroyView.as_view(), name='post-delete-url'),

    path('post/<int:post_id>/comments/', CommentsListView.as_view(), name='post_comments-list-url'),
    path('post/<int:post_id>/comment/create/', CommentCreateView.as_view(), name='post_comment-create-url'),
    path('comment/<int:comment_id>/create/', CommentCreateReplyView.as_view(), name='comment-create_reply-url'),
    path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete-url'),
    path('comment/<int:pk>/delete_branch/', CommentDeleteBranchView.as_view(), name='comment-delete_branch-url'),
    path('comment/<int:comment_id>/update/', CommentUpdateView.as_view(), name='comment-update-url'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-read-url'),
    
    # path('post/<int:post_id>/create_comment/', name='post_comment_create-url'),
    # path('post/<int:post_id>/update_comment/' name=''post_comment-update-url'),
    # path('post/<int:post_id>/delete_comment/', name='post_comment_delete-url'),
    # path('comment/<int:pk>/', name='comment-read-url'),

    path('post/<int:post_id>/reactions/', PostReactionsListView.as_view(), name='post_reaction-list-url'),
    path('post/<int:post_id>/add_reaction/', PostReactionCreateView.as_view(), name='post_reaction-create-url'),
    path('post/<int:post_id>/update_reaction/', PostReactionUpdateView.as_view(), name='post_reaction-update-url'),
    path('post/<int:post_id>/remove_reaction/', PostReactionDeleteView.as_view(), name='post_reaction-delete-url'),
    path('post_reaction/<int:pk>/', PostReactionReadView.as_view(), name='post_reaction-read-url'),
 

    path('tags/', TagsListView.as_view(), name='tags_list-url')
]
