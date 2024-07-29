# Generated by Django 4.2 on 2024-07-22 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('areas', '0003_alter_area_options_alter_area_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_from', models.DateTimeField(verbose_name='От')),
                ('booked_to', models.DateTimeField(verbose_name='До')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата бронирования')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='areas.area', verbose_name='Площадка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_bookings', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бронь площадок',
                'verbose_name_plural': 'Брони площадок',
                'db_table': 'bookings_area',
            },
        ),
    ]
