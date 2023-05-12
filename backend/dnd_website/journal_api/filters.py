from django_filters import rest_framework as DjangoFilters
from .models import *

class AccountFilter(DjangoFilters.FilterSet):
    date_joined = DjangoFilters.DateFromToRangeFilter(field_name='date_joined')
    username = DjangoFilters.CharFilter(field_name='username')
    is_staff = DjangoFilters.BooleanFilter(field_name='is_staff')
    is_active = DjangoFilters.BooleanFilter(field_name='is_active')

    class Meta:
        model = Account
        fields = {}

class PostListFilter(DjangoFilters.FilterSet):

    created_datetime = DjangoFilters.DateTimeFromToRangeFilter(field_name='created_datetime',)

    tags = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='slug',
        field_name='tags__slug',
        queryset = Tag.objects.all(),
        conjoined=False,
    )

    username = DjangoFilters.ModelMultipleChoiceFilter(
        to_field_name='username',
        field_name='author__username',
        queryset = Account.objects.all(),
        conjoined=False,
    )
