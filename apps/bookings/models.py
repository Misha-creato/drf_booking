import uuid

from django.db import models
from django.contrib.auth import get_user_model

from areas.models import Area


User = get_user_model()


class BookingArea(models.Model):
    id = models.CharField(
        verbose_name='Идентификатор',
        max_length=64,
        primary_key=True,
    )
    area = models.ForeignKey(
        verbose_name='Площадка',
        to=Area,
        related_name='bookings',
        on_delete=models.SET_DEFAULT,
        default='Площадка удалена',
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
    created_at = models.DateTimeField(
        verbose_name='Дата бронирования',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.area}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'bookings_area'
        verbose_name = 'Бронь площадок'
        verbose_name_plural = 'Брони площадок'
