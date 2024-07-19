from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema, OpenApiParameter,

)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import ResponseSerializer

from utils.response_patterns import (
    generate_response,
    status_messages,
)

from areas.services import (
    get_areas,
    get_area,
    search_by_name,
    filter_by_params,
)


class AreaListView(APIView):

    @extend_schema(
        responses={
            200: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': [
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
                                },
                            ]
                        },
                    ]
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {}
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def get(self, request):
        status_code, response_data = get_areas()
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class AreaView(APIView):
    @extend_schema(
        responses={
            200: ResponseSerializer,
            404: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
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
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='404',
                value={
                    'message': status_messages[404],
                    'data': {}
                },
                response_only=True,
                status_codes=[404],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {}
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def get(self, request, pk):
        status_code, response_data = get_area(
            pk=pk,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class AreaSearchView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='name',
                description='Название площадки',
                required=True,
                type=OpenApiTypes.STR
            ),
        ],
        responses={
            200: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': [
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
                                },
                            ]
                        },
                    ]
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {}
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def get(self, request):
        name = request.query_params.get('name', '')
        status_code, response_data = search_by_name(
            name=name,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class AreaFilterView(APIView):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='capacity',
                description='Вместимость площадки',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='min_price',
                description='Минимальная цена площадки за сутки',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='max_price',
                description='Максимальная цена площадки за сутки',
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
        ],
        responses={
            200: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': [
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
                                },
                            ]
                        },
                    ]
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {}
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def get(self, request):
        params = request.query_params
        status_code, response_data = filter_by_params(
            params=params,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )
