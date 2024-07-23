from rest_framework import serializers

from bookings.models import BookingArea


class BookAreaSerializer(serializers.Serializer):
    temporary = serializers.BooleanField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()


class BookingAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingArea
        fields = [
            'area',
            'booked_from',
            'booked_to',
            'created_at'
        ]
