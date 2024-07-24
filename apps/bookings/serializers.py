import pytz

from datetime import (
    datetime,
    time,
)

from config import settings

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bookings.models import BookingArea


class DateToDateTimeField(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            value = timezone.localtime(value)
            return super().to_representation(value.date())
        return super().to_representation(value)

    def to_internal_value(self, data):
        date = super().to_internal_value(data)
        default_time = time(12, 0)
        naive_datetime = datetime.combine(date, default_time)

        tz = pytz.timezone(settings.TIME_ZONE)
        aware_datetime = tz.localize(naive_datetime)

        return aware_datetime


class BookAreaSerializer(serializers.Serializer):
    temporary = serializers.IntegerField(
        min_value=0,
        max_value=1,
    )
    start_date = DateToDateTimeField(
        required=True,
    )
    end_date = DateToDateTimeField(
        required=True,
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        min_date = timezone.now().date()
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        if start_date.date() < min_date:
            raise ValidationError(
                'Дата начала бронирования не может быть в прошлом'
            )
        if start_date == end_date:
            raise ValidationError(
                'Дата начала бронирования и дата окончания не могут быть равны'
            )
        return attrs


class BookingAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingArea
        fields = [
            'area',
            'booked_from',
            'booked_to',
            'created_at'
        ]
