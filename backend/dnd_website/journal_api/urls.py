from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from .views import *

router = routers.DefaultRouter()

router.register(r'post', PostViewSet, basename='post')
router.register(r'post_reactions', PostReactionViewSet, basename='post_reactions')
router.register(r'post_comments', PostCommentsViewSet, basename='post_comments')
router.register(r'tag', TagViewSet, basename='tag')


urlpatterns = [
    path('', include(router.urls)),

    path('auth/users/', UserListView.as_view(), name='user_list'),
    path('auth/user/register/', UserRegisterView.as_view(), name='user_register'),
    path('auth/user/activation/', UserActivateView.as_view(), name='user_activate'),
    path('auth/user/reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('auth/user/reset_password_confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confrim'),
    path('auth/user/send_confirmation_code/', SendConfirmationCodeView.as_view(), name='send_confirmation_code'),

    path('auth/jwt/create/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('post/<int:post_id>/comments/', CommentsListView.as_view(), name='post_comments-list-url'),
    path('post/<int:post_id>/comment/create/', CommentCreateView.as_view(), name='post_comment-create-url'),
    path('comment/<int:comment_id>/create/', CommentCreateReplyView.as_view(), name='comment-create_reply-url'),
    path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete-url'),
    path('comment/<int:pk>/delete_branch/', CommentDeleteBranchView.as_view(), name='comment-delete_branch-url'),
    path('comment/<int:comment_id>/update/', CommentUpdateView.as_view(), name='comment-update-url'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-read-url'),

]


