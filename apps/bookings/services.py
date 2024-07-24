from django.http import QueryDict
from django.contrib.auth import get_user_model

from areas.models import Area
from utils.logger import get_logger

from bookings import check
from bookings.models import BookingArea
from bookings.serializers import (
    BookAreaSerializer,
    BookingAreaSerializer,
)

from utils.project_redis import (
    get_temporary_bookings_by_key,
    set_temporary_booking,
)


logger = get_logger(__name__)
User = get_user_model()


def booking_area(area_pk: int, data: QueryDict, user: User) -> (int, dict):
    temporary = data.get('temporary')
    logger.info(
        msg=f'Бронирование площадки {area_pk} пользователем {user}, '
            f'временная бронь: {temporary}'
    )

    try:
        area = Area.objects.filter(
            pk=area_pk,
            available=True,
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                f'пользователем {user}: {exc}'
        )
        return 500, {}

    if area is None:
        logger.error(
            msg=f'Площадка для бронирования {area_pk} пользователем {user} '
                f'не найдена',
        )
        return 404, {}

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
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при бронировании площадки {area_pk} '
                f'пользователем {user}: {exc}',
        )
        return 500, {}

    key_pattern = f'*area{area_pk}*'
    status, temporary_bookings = get_temporary_bookings_by_key(
        key_pattern=key_pattern,
    )

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
        status, response = set_temporary_booking(
            area_pk=area_pk,
            validated_data=validated_data,
            user=user,
        )
        if status != 200:
            logger.error(
                msg=f'Не удалось временно забронировать площадку {area_pk} '
                    f'пользователем {user}',
            )
            return status, {}

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


def user_booking_temporary(user: User) -> (int, dict):
    logger.info(
        msg=f'Получение списка временных броней пользователя {user}',
    )

    key_pattern = f'*_user{user.id}_*'
    status, response_data = get_temporary_bookings_by_key(
        key_pattern=key_pattern,
    )
    if status != 200:
        logger.error(
            msg=f'Не удалось получить список временных броней '
                f'пользователя {user}',
        )
        return status

    logger.info(
        msg=f'Получен список временных броней пользователя {user}',
    )
    return 200, response_data
