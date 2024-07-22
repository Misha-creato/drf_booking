from rest_framework import serializers

from bookings.models import BookingArea


class BookingAreaSerializer(serializers.Serializer):
    temporary = serializers.BooleanField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

