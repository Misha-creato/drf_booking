import uuid

from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone

from areas.models import Area

from utils import redis_cache
from utils.logger import get_logger

from bookings import check
from bookings.models import BookingArea
from bookings.serializers import (
    BookAreaSerializer,
    BookingAreaSerializer,
    GenerateQRSerializer,
    BookingAreaQRSerializer,
)


logger = get_logger(__name__)
User = get_user_model()


def booking_area(area_pk: int, data: QueryDict, user: User) -> (int, dict):
    temporary = data.get('temporary')
    logger.info(
        msg=f'Бронирование площадки {area_pk} пользователем {user}, '
            f'(временная бронь - {temporary})'
    )

    try:
        area = Area.objects.filter(
            pk=area_pk,
            available=True,
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                f'пользователем {user} (временная бронь - {temporary}): '
                f'{exc}'
        )
        return 500, {}

    if area is None:
        logger.error(
            msg=f'Площадка для бронирования {area_pk} '
                f'пользователем {user} (временная бронь - {temporary}) '
                f'не найдена',
        )
        return 404, {}

    serializer = BookAreaSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для бронирования площадки {area_pk} '
                f'пользователем {user} (временная бронь - {temporary}): '
                f'{serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        constant_bookings = BookingArea.objects.filter(
            area__pk=area_pk,
            booked_from__lt=validated_data['end_date'],
            booked_to__gt=validated_data['start_date'],
        )
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                f'пользователем {user} (временная бронь - {temporary}): '
                f'{exc}',
        )
        return 500, {}

    status, temporary_bookings = get_area_booking_temporary(
        area_pk=area_pk,
    )
    if status != 200:
        logger.error(
            msg=f'Не удалось забронировать площадку {area_pk} '
                f'пользователем {user} (временная бронь - {temporary})',
        )
        return status, {}

    valid_booking_dates = check.booking_dates(
        constant=constant_bookings,
        temporary=temporary_bookings,
        validated_data=validated_data,
        user_id=user.id,
    )
    if not valid_booking_dates:
        logger.error(
            msg=f'Не удалось забронировать площадку {area_pk} '
                f'пользователем {user} (временная бронь - {temporary}): '
                f'даты бронирования заняты'
        )
        return 400, {}

    start_date = validated_data['start_date']
    end_date = validated_data['end_date']
    if not temporary:
        try:
            BookingArea.objects.create(
                area_id=area_pk,
                user=user,
                booked_from=start_date,
                booked_to=end_date,
            )
        except Exception as exc:
            logger.error(
                msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                    f'пользователем {user} (временная бронь - {temporary}): '
                    f'{exc}',
            )
            return 500, {}
    else:
        key = f'area{area_pk}_user{user.id}_{str(uuid.uuid4())}'
        data = {
            'area': area_pk,
            'booked_from': start_date.strftime('%Y-%m-%d %H:%M:%S%z'),
            'booked_to': end_date.strftime('%Y-%m-%d %H:%M:%S%z'),
            'user_id': user.id,
            'created_at': timezone.now().strftime('%Y-%m-%d %H:%M:%S%z'),
        }
        status = redis_cache.set_key(
            key=key,
            data=data,
            time=60 * 60,
        )
        if status != 200:
            logger.error(
                msg=f'Не удалось временно забронировать площадку {area_pk} '
                    f'пользователем {user} (временная бронь - {temporary})',
            )
            return status, {}

    logger.info(
        msg=f'Бронирование площадки {area_pk} '
            f'пользователем {user} (временная бронь - {temporary}) '
            f'прошло успешно',
    )
    return 200, {}


def user_booking_history(user: User) -> (int, list):
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
        return 500, []

    response_data = BookingAreaSerializer(
        instance=bookings,
        many=True
    ).data
    logger.info(
        msg=f'Получена история постоянного бронирования '
            f'пользователя {user}',
    )
    return 200, response_data


def user_booking_temporary(user: User) -> (int, list):
    logger.info(
        msg=f'Получение списка временных броней пользователя {user}',
    )

    key_pattern = f'*_user{user.id}_*'
    status, matching_keys = redis_cache.get_matching_keys(
        key_pattern=key_pattern,
    )
    if status != 200:
        logger.error(
            msg=f'Не удалось получить список временных броней '
                f'пользователя {user}',
        )
        return status, []

    response_data = []
    for key in matching_keys:
        status, data = redis_cache.get(
            key=key,
        )
        if status != 200:
            return status, []

        response_data.append(data)

    logger.info(
        msg=f'Получен список временных броней пользователя {user}',
    )
    return 200, response_data


def get_area_booking_temporary(area_pk: int) -> (int, list):
    logger.info(
        msg=f'Получение списка временных броней площадки {area_pk}',
    )

    key_pattern = f'*area{area_pk}*'
    status, matching_keys = redis_cache.get_matching_keys(
        key_pattern=key_pattern,
    )
    if status != 200:
        logger.error(
            msg=f'Не удалось получить список временных броней '
                f'площадки {area_pk}',
        )
        return status, []

    response_data = []
    for key in matching_keys:
        status, data = redis_cache.get(
            key=key,
        )
        if status != 200:
            return status, []

        response_data.append(data)

    logger.info(
        msg=f'Получен список временных броней площадки {area_pk}',
    )
    return 200, response_data


def get_area_qr_data(data: QueryDict) -> (int, dict):
    logger.info(
        msg=f'Получение данных для генерации qr для '
            f'бронирования {data}',
    )

    serializer = GenerateQRSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для генерации QR для '
                f'бронирования {data}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        booking = BookingArea.objects.filter(
            id=validated_data['booking_id'],
            booked_to__gt=timezone.now()
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при получении данных '
                f'для генерации QR для бронирования {data}: {exc}',
        )
        return 500, {}

    if booking is None:
        logger.error(
            msg=f'Бронирование {data} при получении данных '
                f'для генерации QR не найдено',
        )
        return 400, {}

    response_data = BookingAreaQRSerializer(
        instance=booking,
    ).data
    logger.info(
        msg=f'Получены данные для генерации QR для бронирования {data}',
    )
    return 200, response_data


def area_qr_check(data: QueryDict) -> (int, dict):
    logger.info(
        msg=f'Подтверждение начала бронирования {data}',
    )

    serializer = BookingAreaQRSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для подтверждения '
                f'начала бронирования {data}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        booking = BookingArea.objects.filter(
            id=validated_data['id'],
            booked_to__gt=timezone.now(),
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при подтверждении начала '
                f'бронирования {data}: {exc}',
        )
        return 500, {}

    if booking is None:
        logger.error(
            msg=f'Бронирование {data} для подтверждения '
                f'начала не найдено',
        )
        return 400, {}

    booking.started = True
    try:
        booking.save()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при подтверждении начала '
                f'бронирования {data}: {exc}',
        )
        return 500, {}

    logger.info(
        msg=f'Успешно подтверждено начало бронирования {data}',
    )
    return 200, {}
