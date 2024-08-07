# Generated by Django 4.2 on 2024-07-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='email_type',
            field=models.CharField(choices=[('confirm_email', 'Подтверждение адреса электронной почты'), ('password_restore', 'Восстановление пароля')], max_length=64, unique=True, verbose_name='Тип письма'),
        ),
    ]
