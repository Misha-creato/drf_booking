from django.db import models
from django.forms import model_to_dict

from solo.models import SingletonModel

from utils.constants import EMAIL_TYPES
from utils.project_redis import set_email_settings


class EmailTemplate(models.Model):
    email_type = models.CharField(
        verbose_name='Тип письма',
        max_length=64,
        unique=True,
        choices=EMAIL_TYPES,
    )
    subject = models.CharField(
        verbose_name='Тема',
        max_length=256,
    )
    message = models.TextField(
        verbose_name='Сообщение',
    )

    def __str__(self):
        return self.email_type

    class Meta:
        db_table = 'email_templates'
        verbose_name = 'Шаблон письма'
        verbose_name_plural = 'Шаблоны писем'


class EmailSettings(SingletonModel):
    send_emails = models.BooleanField(
        verbose_name='Отправка писем включена',
        default=True,
    )

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        set_email_settings(email_settings=model_to_dict(self))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'email_settings'
        verbose_name = 'Настройки email'
