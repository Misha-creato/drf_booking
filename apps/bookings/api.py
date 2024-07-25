from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response_patterns import generate_response

from bookings.services import (
    booking_area,
    user_booking_history,
    user_booking_temporary,
    get_area_qr_data,
    area_qr_check,
)


class BookingAreaView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, area_pk):
        data = request.data
        user = request.user
        status_code, response_data = booking_area(
            area_pk=area_pk,
            data=data,
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class UserBookingAreaHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_code, response_data = user_booking_history(
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class UserBookingAreaTemporaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_code, response_data = user_booking_temporary(
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class BookingAreaQRDataView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        status_code, response_data = get_area_qr_data(
            data=data,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class BookingAreaQRCheckView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        status_code, response_data = area_qr_check(
            data=data,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )