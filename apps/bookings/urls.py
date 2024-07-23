from django.urls import path

from bookings.api import (
    BookingAreaView,
    UserBookingsConstantView,
    UserBookingsTemporaryView,
)


urlpatterns = [
    path(
        'areas/<int:area_pk>/',
        BookingAreaView.as_view(),
        name='booking_area',
    ),
    path(
        'history/constant/',
        UserBookingsConstantView.as_view(),
        name='user_bookings_constant',
    ),
    path(
        'history/temporary/',
        UserBookingsTemporaryView.as_view(),
        name='user_bookings_temporary',
    ),
]
