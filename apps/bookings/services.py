import json
import uuid
import redis

from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone

from utils.logger import get_logger

from bookings import check
from bookings.models import BookingArea
from bookings.serializers import (
    BookAreaSerializer,
    BookingAreaSerializer,
)


logger = get_logger(__name__)
User = get_user_model()
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)


def booking_area(area_pk: int, data: QueryDict, user: User) -> (int, dict):
    temporary = data.get('temporary')
    logger.info(
        msg=f'Бронирование площадки {area_pk} пользователем {user}, '
            f'временная бронь: {temporary}'
    )
    serializer = BookAreaSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для бронирования площадки {area_pk} '
                f'пользователем {user}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        constant_bookings = BookingArea.objects.filter(
            area__pk=area_pk,
            booked_from__lt=validated_data['end_date'],
            booked_to__gt=validated_data['start_date'],
        )
        matching_keys = redis_client.keys(f'*area{area_pk}*')
        temporary_bookings = [json.loads(redis_client.get(key)) for key in matching_keys]
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                f'пользователем {user}: {exc}',
        )
        return 500, {}

    valid_booking_dates = check.booking_dates(
        constant=constant_bookings,
        temporary=temporary_bookings,
        validated_data=validated_data,
        user_id=user.id,
    )
    if not valid_booking_dates:
        logger.error(
            msg=f'Не удалось забронировать площадку {area_pk} '
                f'пользователем {user}. Даты бронирования заняты'
        )
        return 400, {}

    return book_area_by_status(
        area_pk=area_pk,
        validated_data=validated_data,
        user=user,
    )


def book_area_by_status(area_pk: int, validated_data: dict, user: User) -> (int, dict):
    start_date = validated_data['start_date']
    end_date = validated_data['end_date']
    if validated_data['temporary']:
        logger.info(
            msg=f'Временное бронирование площадки {area_pk} '
                f'пользователем {user}',
        )
        data = {
            'area': area_pk,
            'booked_from': start_date.strftime('%Y-%m-%d'),
            'booked_to': end_date.strftime('%Y-%m-%d'),
            'user_id': user.id,
            'created_at': timezone.now().strftime('%Y-%m-%d'),
        }
        key = f'area{area_pk}_user{user.id}_{str(uuid.uuid4())}'
        print(key)
        try:
            key_data = json.dumps(data)
            redis_client.setex(name=key, time=60, value=key_data)
        except Exception as exc:
            logger.error(
                msg=f'Возникла ошибка при временном бронировании площадки {area_pk} '
                    f'пользователем {user}: {exc}',
            )
            return 500, {}

        logger.info(
            msg=f'Временное бронирование площадки {area_pk} '
                f'пользователем {user} прошло успешно',
        )
        return 200, {}

    logger.info(
        msg=f'Постоянное бронирование площадки {area_pk} '
            f'пользователем {user}',
    )
    try:
        booking = BookingArea.objects.create(
            area_id=area_pk,
            user=user,
            booked_from=start_date,
            booked_to=end_date,
        )
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при постоянном бронировании площадки {area_pk} '
                f'пользователем {user}: {exc}',
        )
        return 500, {}

    logger.info(
        msg=f'Постоянное бронирование площадки {area_pk} '
            f'пользователем {user} прошло успешно',
    )
    return 200, {}


def user_booking_constant(user: User) -> (int, dict):
    logger.info(
        msg=f'Получение истории постоянного бронирования '
            f'пользователя {user}',
    )

    try:
        bookings = BookingArea.objects.filter(
            user=user,
        )
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при получении истории постоянного '
                f'бронирования пользователя {user}: {exc}',
        )
        return 500, {}

    response_data = BookingAreaSerializer(
        instance=bookings,
        many=True
    ).data
    logger.info(
        msg=f'Получена история постоянного бронирования '
            f'пользователя {user}',
    )
    return 200, response_data


def user_booking_temporary(user: User) -> (int, dict):
    logger.info(
        msg=f'Получение истории временного бронирования '
            f'пользователя {user}',
    )

    try:
        matching_keys = redis_client.keys(f'*_user{user.id}_*')
        temporary_bookings = [json.loads(redis_client.get(key)) for key in matching_keys]
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при получении истории временного '
                f'бронирования пользователя {user}: {exc}',
        )
        return 500, {}

    response_data = temporary_bookings
    logger.info(
        msg=f'Получена история временного бронирования '
            f'пользователя {user}',
    )
    return 200, response_data
