import django_filters

from areas.models import Area


class AreaFilter(django_filters.FilterSet):

    class Meta:
        model = Area
        fields = {
            'price': ['lte', 'gte'],
            'capacity': ['lte', 'gte'],
            'width': ['lte', 'gte'],
            'length': ['lte', 'gte'],
        }
