from django.urls import path

from areas.api import (
    AreaListView,
    AreaView,
)


urlpatterns = [
    path(
        'all/',
        AreaListView.as_view(),
        name='areas',
    ),
    path(
        '<int:pk>/',
        AreaView.as_view(),
        name='area',
    ),
]
