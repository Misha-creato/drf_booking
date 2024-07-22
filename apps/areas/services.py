from typing import Any

from django.db.models.expressions import RawSQL

from areas.models import Area
from areas.serializers import AreaSerializer

from utils.logger import get_logger

logger = get_logger(__name__)


def get_areas(request: Any, filter_backends: list, view: Any) -> (int, list):
    '''
    Получение списка всех площадок

    Returns:
        Код статуса и список данных
        200,
        [
            {
                "pk": 1,
                "name": "Test",
                "description": "<p>description</p>",
                "address": "address",
                "price": "1000",
                "capacity": 1000,
                "width": 200,
                "length": 100,
                "contacts": [
                    {
                        "contact": "88005553535",
                        "contact_type": "Phone"
                    },
                    {
                        "contact": "test3@cc.com",
                        "contact_type": "Email"
                    },
                ],
                "photos": [
                {
                    "photo": "/media/photos/test.jpeg"
                }
            ]
            },
        ]
    '''

    logger.info(
        msg='Получение списка всех площадок',
    )

    try:
        areas = Area.objects.annotate(
            price_int=RawSQL(
                "CAST(REPLACE(price, ' ', '') AS INTEGER)",
                []
            )
        ).filter(
            available=True,
        ).prefetch_related('contacts', 'photos')
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить список всех площадок: {exc}',
        )
        return 500, {}

    if request.query_params:
        for backend in filter_backends:
            try:
                areas = backend().filter_queryset(
                    request=request,
                    queryset=areas,
                    view=view,
                )
            except Exception as exc:
                logger.info(
                    msg=f'Не удалось получить список всех площадок по фильтрам: {exc}',
                )

    response_data = AreaSerializer(
        instance=areas,
        many=True,
    ).data
    logger.info(
        msg=f'Список всех площадок получен',
    )
    return 200, response_data


def get_area(pk: int) -> (int, dict):
    '''
    Получение площадки по pk

    Args:
        pk: pk площадки

    Returns:
        Код статуса и словарь данных
        200,
        {
            "pk": 1,
            "name": "Test",
            "description": "<p>description</p>",
            "address": "address",
            "price": "1000",
            "capacity": 1000,
            "width": 200,
            "length": 100,
            "contacts": [
                {
                    "contact": "88005553535",
                    "contact_type": "Phone"
                },
                {
                    "contact": "test3@cc.com",
                    "contact_type": "Email"
                },
            ],
            "photos": [
                {
                    "photo": "/media/photos/test.jpeg"
                }
            ]
        }
    '''

    logger.info(
        msg=f'Получение площадки по pk {pk}',
    )

    try:
        area = Area.objects.filter(
            pk=pk,
            available=True,
        ).prefetch_related('contacts', 'photos').first()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить площадку по pk {pk}: {exc}',
        )
        return 500, {}

    if area is None:
        logger.error(
            msg=f'Площадка по pk {pk} не найдена',
        )
        return 404, {}

    response_data = AreaSerializer(
        instance=area,
    ).data
    logger.info(
        msg=f'Площадка по pk {pk} получена',
    )
    return 200, response_data

