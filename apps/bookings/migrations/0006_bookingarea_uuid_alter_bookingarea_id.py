# Generated by Django 4.2 on 2024-07-29 13:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_bookingarea_started_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingarea',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, verbose_name='Идентификатор'),
        ),
        migrations.RemoveField(
            model_name='bookingarea',
            name='id',
        ),
        migrations.AlterField(
            model_name='bookingarea',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False,
                                   verbose_name='Идентификатор'),
        ),
    ]
