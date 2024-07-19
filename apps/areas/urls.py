from django.urls import path

from areas.api import (
    AreaListView,
    AreaView,
    AreaSearchView,
    AreaFilterView,
)


urlpatterns = [
    path(
        'all/',
        AreaListView.as_view(),
        name='area_list',
    ),
    path(
        'search/',
        AreaSearchView.as_view(),
        name='area_search',
    ),
    path(
        'filter/',
        AreaFilterView.as_view(),
        name='area_filter',
    ),
    path(
        '<int:pk>/',
        AreaView.as_view(),
        name='area',
    ),
]
