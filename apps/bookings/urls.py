from django.urls import path

from bookings.api import (
    BookingAreaView,
    UserBookingAreaHistoryView,
    UserBookingAreaTemporaryView,
    BookingAreaQRDataView,
    BookingAreaQRCheckView,
)


urlpatterns = [
    path(
        'areas/qr/get/',
        BookingAreaQRDataView.as_view(),
        name='areas_get_qr',
    ),
    path(
        'areas/qr/check/',
        BookingAreaQRCheckView.as_view(),
        name='areas_get_check',
    ),
    path(
        'areas/<int:area_pk>/',
        BookingAreaView.as_view(),
        name='booking_area',
    ),
    path(
        'users/history/',
        UserBookingAreaHistoryView.as_view(),
        name='user_bookings_history',
    ),
    path(
        'users/temporary/',
        UserBookingAreaTemporaryView.as_view(),
        name='user_bookings_temporary',
    ),
]
