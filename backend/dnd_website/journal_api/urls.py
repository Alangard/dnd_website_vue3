from django.urls import path, include
from rest_framework import routers
from .views import *

# router = routers.DefaultRouter()
# router.register(r'posts', PostView)
# router.register(r'accounts', AccountView)


urlpatterns = [
    path('auth/', include('rest_framework.urls')),

    path('accounts/', AccountListView.as_view(), name='accounts-list-url'),
    path('account/<slug:slug>/', AccountUpdateView.as_view(), name='account-update-url'),
    path('account/<slug:slug>/delete', AccountDestroyView.as_view(), name='account-delete-url'),

    path('posts/', PostListView.as_view(), name='posts-list-url'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post-update-url'),
    path('post/<int:pk>/delete', PostDestroyView.as_view(), name='post-delete-url'),
]

