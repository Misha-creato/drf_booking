from django.db import models

from utils.constants import CONTACT_TYPES


class Area(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    address = models.TextField(
        verbose_name='Адрес',
    )
    available = models.BooleanField(
        verbose_name='Доступна',
        default=True,
    )
    price = models.CharField(
        verbose_name='Цена за сутки',
        max_length=256,
        default='Не указана',
    )
    capacity = models.PositiveIntegerField(
        verbose_name='Вместимость человек',
    )
    width = models.PositiveIntegerField(
        verbose_name='Ширина',
    )
    length = models.PositiveIntegerField(
        verbose_name='Длина',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата размещения',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        db_table = 'areas'
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'


class Contact(models.Model):
    area = models.ForeignKey(
        to=Area,
        related_name='contacts',
        on_delete=models.CASCADE,
    )
    contact = models.TextField(
        verbose_name='Контакт',
    )
    contact_type = models.CharField(
        verbose_name='Тип контакта',
        max_length=64,
        choices=CONTACT_TYPES,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата размещения',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'area_contacts'
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Photo(models.Model):
    area = models.ForeignKey(
        to=Area,
        related_name='photos',
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='photos/'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата размещения',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'area_photos'
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
