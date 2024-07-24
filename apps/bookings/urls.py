from django.urls import path

from bookings.api import (
    BookingAreaView,
    UserBookingsHistoryView,
    UserBookingsTemporaryView,
)


urlpatterns = [
    path(
        'areas/<int:area_pk>/',
        BookingAreaView.as_view(),
        name='booking_area',
    ),
    path(
        'users/history/',
        UserBookingsHistoryView.as_view(),
        name='user_bookings_history',
    ),
    path(
        'users/temporary/',
        UserBookingsTemporaryView.as_view(),
        name='user_bookings_temporary',
    ),
]
