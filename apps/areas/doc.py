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
    Получение списка всех площадок

    Returns:
        {
          "message": "Сообщение",
          "data": [
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
        }
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


class Area200Response(DefaultAreaResponse):
    '''
    Получение площадки по pk

    Returns:
        {
          "message": "Сообщение",
          "data": {
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
                ],
                "photos": [
                    {
                        "photo": "/media/photos/test.jpeg"
                    }
                ]
            }
        }
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
