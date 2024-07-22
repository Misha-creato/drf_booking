from rest_framework import filters
import django_filters

from areas.models import Area


class AreaFilter(django_filters.FilterSet):

    min_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='gte',
    )
    max_capacity = django_filters.NumberFilter(
        field_name='capacity',
        lookup_expr='lte',
    )
    min_width = django_filters.NumberFilter(
        field_name='width',
        lookup_expr='gte',
    )
    max_width = django_filters.NumberFilter(
        field_name='width',
        lookup_expr='lte',
    )
    min_length = django_filters.NumberFilter(
        field_name='length',
        lookup_expr='gte',
    )
    max_length = django_filters.NumberFilter(
        field_name='length',
        lookup_expr='lte',
    )
    min_price = django_filters.NumberFilter(
        field_name='price_int',
        lookup_expr='gte',
    )
    max_price = django_filters.NumberFilter(
        field_name='price_int',
        lookup_expr='lte',
    )

    class Meta:
        model = Area
        fields = [
            'price',
            'capacity',
            'width',
            'length',
        ]
