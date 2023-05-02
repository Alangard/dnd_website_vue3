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

    tags = DjangoFilters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset = Tag.objects.all(),
        conjoined='True',
    )

    created_datetime = DjangoFilters.DateTimeFromToRangeFilter(field_name='created_datetime',)

    class Meta:
        model = Post
        fields = {'author__username':['icontains']}
