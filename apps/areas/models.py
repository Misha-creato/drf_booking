from django.db import models

from django_ckeditor_5.fields import CKEditor5Field

from utils.constants import CONTACT_TYPES


class Area(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
    )
    description = CKEditor5Field(
        verbose_name='Описание',
        null=True,
        blank=True,
        config_name='extends',
    )
    address = models.TextField(
        verbose_name='Адрес',
    )
    available = models.BooleanField(
        verbose_name='Доступна',
        default=True,
    )
    price = models.DecimalField(
        verbose_name='Цена за сутки',
        max_digits=12,
        decimal_places=2,
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
        verbose_name='Площадка',
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


def area_photos_directory_path(instance, filename):
    return f'areas/{instance.area.name}/photos/{filename}'


class Photo(models.Model):
    area = models.ForeignKey(
        verbose_name='Площадка',
        to=Area,
        related_name='photos',
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='area_photos_path',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата размещения',
        auto_now_add=True,
    )

    @staticmethod
    def area_photos_path(instance, filename):
        return f'areas/{instance.area.name}/photos/{filename}'

    class Meta:
        db_table = 'area_photos'
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


Photo._meta.get_field('photo').upload_to = Photo.area_photos_path
