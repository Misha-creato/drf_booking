from django.db.models.expressions import RawSQL

from areas.models import Area
from areas.serializers import AreaSerializer

from utils.logger import get_logger

logger = get_logger(__name__)


def get_areas() -> (int, list):
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
                    {
                        "contact": "wa.me/88005553535",
                        "contact_type": "Whatsapp"
                    },
                    {
                        "contact": "@test2",
                        "contact_type": "Instagram"
                    },
                    {
                        "contact": "t.me/test2",
                        "contact_type": "Telegram"
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
        areas = Area.objects.filter(
            available=True,
        ).prefetch_related('contacts', 'photos')
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить список всех площадок: {exc}',
        )
        return 500, {}

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
                {
                    "contact": "wa.me/88005553535",
                    "contact_type": "Whatsapp"
                },
                {
                    "contact": "@test2",
                    "contact_type": "Instagram"
                },
                {
                    "contact": "t.me/test2",
                    "contact_type": "Telegram"
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


def search_by_name(name: str) -> (int, list):
    '''
    Получение списка площадок по названию

    Args:
        name: название площадки

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
                    {
                        "contact": "wa.me/88005553535",
                        "contact_type": "Whatsapp"
                    },
                    {
                        "contact": "@test2",
                        "contact_type": "Instagram"
                    },
                    {
                        "contact": "t.me/test2",
                        "contact_type": "Telegram"
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
        msg=f'Получение списка площадок по названию {name}',
    )

    try:
        areas = Area.objects.filter(
            name__icontains=name,
            available=True,
        ).prefetch_related('contacts', 'photos')
    except Exception as exc:
        logger.error(
            msg=f'Не удалось найти площадки по названию {name}: {exc}',
        )
        return 500, {}

    response_data = AreaSerializer(
        instance=areas,
        many=True,
    ).data
    logger.info(
        msg=f'Получен список площадок по названию {name}',
    )
    return 200, response_data


def filter_by_params(params: dict) -> (int, dict):
    '''
    Получение списка площадок по полям

    Args:
        params: поля для фильтрации
            {
              "capacity": 200,
              "min_price": 1000,
              "max_price": 100000,
              "width": 100,
              "length": 100,
            }

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
                    {
                        "contact": "wa.me/88005553535",
                        "contact_type": "Whatsapp"
                    },
                    {
                        "contact": "@test2",
                        "contact_type": "Instagram"
                    },
                    {
                        "contact": "t.me/test2",
                        "contact_type": "Telegram"
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
        msg=f'Получение списка площадок по полям {params}',
    )
    capacity = params.get('capacity', '0')
    min_price = params.get('min_price', '0')
    max_price = params.get('max_price', '1000000')
    width = params.get('width', '0')
    length = params.get('length', '0')

    try:
        areas = Area.objects.annotate(
            price_int=RawSQL(
                "CAST(REPLACE(price, ' ', '') AS INTEGER)",
                []
            )
        ).exclude(
            price='Не указана',
        ).filter(
            available=True,
            capacity__gte=capacity,
            width__gte=width,
            length__gte=length,
            price_int__gte=min_price,
            price_int__lte=max_price,
        )
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить список площадок по полям {params}: {exc}',
        )
        return 500, {}

    response_data = AreaSerializer(
        instance=areas,
        many=True,
    ).data
    logger.info(
        msg=f'Список площадок по полям {params} получен',
    )
    return 200, response_data


# def sort_by_params(params: dict) -> (int, dict)
#     logger.info(
#         msg=f'Сортировка списка площадок по полям {params}',
#     )
