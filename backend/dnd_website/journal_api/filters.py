from django_filters import rest_framework as DjangoFilters
from .models import *

class AccountFilter(DjangoFilters.FilterSet):
    date_joined = DjangoFilters.DateFromToRangeFilter(field_name='date_joined')
    username = DjangoFilters.CharFilter(field_name='username')
    email = DjangoFilters.CharFilter(field_name='email')
    is_staff = DjangoFilters.BooleanFilter(field_name='is_staff')
    is_active = DjangoFilters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Account
        fields = {}

class PostListFilter(DjangoFilters.FilterSet):

    created_datetime = DjangoFilters.DateTimeFromToRangeFilter(field_name='created_datetime',)

    tag_name = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='name',
        field_name='tags__name',
        queryset = Tag.objects.all(),
        conjoined=False,
    )

    author_username = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='username',
        field_name='author__username',
        queryset = Account.objects.all(),
        conjoined=False,
    )

# class PostListFilter(DjangoFilters.FilterSet):
#     class Meta:
#         model = Post
#         fields = {
#             'tag__slug': ['exact'],
#             'author__username': ['exact'],
#             # Добавьте другие поля фильтров, если такие есть
#         }

class PostReactionsFilter(DjangoFilters.FilterSet):

    created_datetime = DjangoFilters.DateTimeFromToRangeFilter(field_name='reacted_at',)
    reaction_type = DjangoFilters.ChoiceFilter(choices=PostReaction.REACTION_CHOICES)
    username = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='username',
        field_name='author__username',
        queryset = Account.objects.all(),
        conjoined=False,
    )

class CommentReactionsFilter(DjangoFilters.FilterSet):

    created_datetime = DjangoFilters.DateTimeFromToRangeFilter(field_name='reacted_at',)
    reaction_type = DjangoFilters.ChoiceFilter(choices=PostReaction.REACTION_CHOICES)
    username = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='username',
        field_name='author__username',
        queryset = Account.objects.all(),
        conjoined=False,
    )