# Generated by Django 4.2 on 2024-07-23 12:31

import areas.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0005_alter_area_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to=areas.models.area_photos_directory_path, verbose_name='Фото'),
        ),
    ]
