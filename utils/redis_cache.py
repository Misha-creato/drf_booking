import json
import uuid

import redis

from django.contrib.auth import get_user_model
from django.utils import timezone

from config.settings import (
    REDIS_HOST,
    REDIS_PORT,
)

from utils.logger import get_logger


User = get_user_model()
logger = get_logger(__name__)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)


def get_temporary_bookings_by_key(key_pattern: str) -> (int, list):
    logger.info(
        msg=f'Получение списка временных броней по шаблону ключа {key_pattern}',
    )
    try:
        matching_keys = redis_client.keys(key_pattern)
        temporary_bookings = [json.loads(redis_client.get(key)) for key in matching_keys]
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при получении временных броней '
                f'по шаблону ключа {key_pattern}: {exc}',
        )
        return 500, []

    logger.info(
        msg=f'Получен список временных броней по шаблону ключа {key_pattern}',
    )
    return 200, temporary_bookings


def set_temporary_booking(area_pk: int, validated_data: dict, user: User) -> (int, {}):
    start_date = validated_data['start_date']
    end_date = validated_data['end_date']
    data = {
        'area': area_pk,
        'booked_from': start_date.strftime('%Y-%m-%d %H:%M:%S%z'),
        'booked_to': end_date.strftime('%Y-%m-%d %H:%M:%S%z'),
        'user_id': user.id,
        'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S%z'),
    }
    key = f'area{area_pk}_user{user.id}_{str(uuid.uuid4())}'
    try:
        key_data = json.dumps(data)
        redis_client.setex(name=key, time=60, value=key_data)
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при временном бронировании площадки {area_pk} '
                f'пользователем {user}: {exc}',
        )
        return 500, {}

    return 200, {}


def set_email_settings(email_settings: dict) -> None:
    email_settings_json = json.dumps(email_settings)
    redis_client.set('email_settings', email_settings_json)


def get_email_settings() -> dict:
    email_settings = redis_client.get('email_settings')
    return json.loads(email_settings)

