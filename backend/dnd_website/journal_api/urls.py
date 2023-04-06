from django.urls import path
from .views import *

urlpatterns = [
    path("account/<int:pk>/", AccountDetailView.as_view(), name='account_detail_url'),
    path("reactions_categories/", ReactionCategoriesView.as_view(), name='reactions_categories_url'),
    path("reactions/", ReactionListView.as_view(), name='reactions_url'),
    path("post_reactions/<int:pk>/", PostReactionView.as_view(), name='post_reactions_url'),
    path("posts/", PostListView.as_view(), name='posts_url'),
    path("post/<int:pk>/", PostDetailView.as_view(), name='post_detail_url'),
    path("tags/", TagListView.as_view(), name='tags_url'),
    path("tag/<str:slug>", TagDetailView.as_view(), name='tag_detail_url'),
    
    # path('comments', CommentsView.as_view()),
    # path('tags', TagsView.as_view()),
    # path('report_reasons', ReportReason.as_view()),
    # path('users', UserView.as_view()),
]