import json
import redis

from django.contrib.auth import get_user_model

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
    print(temporary_bookings)
    return 200, temporary_bookings


def set_email_settings(email_settings: dict) -> None:
    email_settings_json = json.dumps(email_settings)
    redis_client.set('email_settings', email_settings_json)


def get_email_settings() -> dict:
    email_settings = redis_client.get('email_settings')
    return json.loads(email_settings)

