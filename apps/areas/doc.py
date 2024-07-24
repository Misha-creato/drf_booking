from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework import serializers


class DefaultAreaResponse(serializers.Serializer):
    message = serializers.CharField(
        default='Сообщение',
    )
    data = serializers.JSONField(
        default={},
    )


class AreaList200Response(DefaultAreaResponse):
    '''
    Получение списка всех площадок, поиск, фильтрация по параметрам

    '''

    data = serializers.JSONField(
        default=[
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
        ]
    )


class Area200Response(DefaultAreaResponse):
    '''
    Получение детальной информации о площадке

    '''

    data = serializers.JSONField(
        default=[
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
    )


area_list_parameters = [
    OpenApiParameter(
        name='search',
        description='Название площадки',
        required=False,
        type=OpenApiTypes.STR
    ),
    OpenApiParameter(
        name='price',
        description='Цена за сутки',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='capacity',
        description='Вместимость человек',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='width',
        description='Ширина площадки',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='length',
        description='Длина площадки',
        required=False,
        type=OpenApiTypes.INT
    ),
]
