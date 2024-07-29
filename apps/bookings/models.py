import uuid

from django.db import models
from django.contrib.auth import get_user_model

from solo.models import SingletonModel

from areas.models import Area


User = get_user_model()


class BookingArea(models.Model):
    uuid = models.UUIDField(
        verbose_name='Идентификатор',
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    area = models.ForeignKey(
        verbose_name='Площадка',
        to=Area,
        related_name='bookings',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        related_name='area_bookings',
        on_delete=models.CASCADE,
    )
    booked_from = models.DateTimeField(
        verbose_name='От',
    )
    booked_to = models.DateTimeField(
        verbose_name='До',
    )
    started = models.BooleanField(
        verbose_name='Начато',
        default=False,
    )
    started_at = models.DateTimeField(
        verbose_name='Дата начала',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата бронирования',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.area}'

    class Meta:
        db_table = 'bookings_area'
        verbose_name = 'Бронь площадок'
        verbose_name_plural = 'Брони площадок'


class BookingSettings(SingletonModel):
    temporary_timeout = models.IntegerField(
        verbose_name='Время жизни временной брони',
        default=60*60,
    )

    def __str__(self):
        return ''

    class Meta:
        db_table = 'bookings_settings'
        verbose_name = 'Настройки брони'
