from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    RegisterSerializer,
    AuthSerializer,
    RefreshAndLogoutSerializer,
    PasswordRestoreRequestSerializer,
    PasswordRestoreSerializer,
    UpdateSerializer,
    ResponseSerializer,
)
from utils.response_patterns import (
    generate_response,
    status_messages,
)

from users.services import (
    register,
    auth,
    refresh_token,
    logout,
    confirm_email,
    password_restore_request,
    password_restore,
    detail,
    update,
    remove,
    confirm_email_request,
)


class RegisterView(APIView):

    @extend_schema(
        request=RegisterSerializer,
        responses={
            200: ResponseSerializer,
            201: ResponseSerializer,
            400: ResponseSerializer,
            406: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
                        'refresh': 'refresh_token',
                        'access': 'access_token',
                    }
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='201',
                value={
                    'message': status_messages[201],
                    'data': {}
                },
                response_only=True,
                status_codes=[201],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
            ),
            OpenApiExample(
                name='406',
                value={
                    'message': status_messages[406],
                    'data': {}
                },
                response_only=True,
                status_codes=[406],
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
    def post(self, request):
        data = request.data
        host = request.get_host()
        status_code, response_data = register(
            data=data,
            host=host,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class AuthView(APIView):

    @extend_schema(
        request=AuthSerializer,
        responses={
            200: RegisterSerializer,
            400: RegisterSerializer,
            401: RegisterSerializer,
            500: RegisterSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
                        'refresh': 'refresh_token',
                        'access': 'access_token',
                    }
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
            ),
            OpenApiExample(
                name='401',
                value={
                    'message': status_messages[401],
                    'data': {}
                },
                response_only=True,
                status_codes=[401],
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
    def post(self, request):
        data = request.data
        status_code, response_data = auth(
            data=data,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class RefreshTokenView(APIView):

    @extend_schema(
        request=RefreshAndLogoutSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            403: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
                        'access': 'access_token',
                        'refresh': 'new_refresh_token',
                    }
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
            ),
            OpenApiExample(
                name='403',
                value={
                    'message': status_messages[403],
                    'data': {}
                },
                response_only=True,
                status_codes=[403],
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
    def post(self, request):
        data = request.data
        status_code, response_data = refresh_token(
            data=data,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RefreshAndLogoutSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {}
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
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
    def post(self, request):
        data = request.data
        user = request.user
        status_code, response_data = logout(
            data=data,
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class ConfirmEmailView(APIView):

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
                    'data': {}
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
    def get(self, request, url_hash):
        status_code, response_data = confirm_email(
            url_hash=url_hash,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class ConfirmEmailRequestView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: ResponseSerializer,
            403: ResponseSerializer,
            500: ResponseSerializer,
            501: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {}
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='403',
                value={
                    'message': status_messages[403],
                    'data': {}
                },
                response_only=True,
                status_codes=[403],
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
            OpenApiExample(
                name='501',
                value={
                    'message': status_messages[501],
                    'data': {}
                },
                response_only=True,
                status_codes=[501],
            ),
        ],
    )
    def post(self, request):
        user = request.user
        host = request.get_host()
        status_code, response_data = confirm_email_request(
            user=user,
            host=host,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class PasswordRestoreRequestView(APIView):

    @extend_schema(
        request=PasswordRestoreRequestSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            403: ResponseSerializer,
            404: ResponseSerializer,
            500: ResponseSerializer,
            501: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {}
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
            ),
            OpenApiExample(
                name='403',
                value={
                    'message': status_messages[403],
                    'data': {}
                },
                response_only=True,
                status_codes=[403],
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
            OpenApiExample(
                name='501',
                value={
                    'message': status_messages[501],
                    'data': {}
                },
                response_only=True,
                status_codes=[501],
            ),
        ],
    )
    def post(self, request):
        data = request.data
        host = request.get_host()
        status_code, response_data = password_restore_request(
            data=data,
            host=host,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class PasswordRestoreView(APIView):

    @extend_schema(
        request=PasswordRestoreSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            404: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {}
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {}
                },
                response_only=True,
                status_codes=[400],
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
    def post(self, request, url_hash):
        data = request.data
        status_code, response_data = password_restore(
            data=data,
            url_hash=url_hash,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class CustomUserView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
                            "email": "test@cc.com",
                            "nickname": "user012345789",
                            "email_confirmed": True,
                    },
                },
                response_only=True,
                status_codes=[200],
            ),
        ],
    )
    def get(self, request):
        user = request.user
        status_code, response_data = detail(
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )

    @extend_schema(
        request=UpdateSerializer,
        responses={
            200: ResponseSerializer,
            400: ResponseSerializer,
            500: ResponseSerializer,
        },
        examples=[
            OpenApiExample(
                name='200',
                value={
                    'message': status_messages[200],
                    'data': {
                            "email": "test@cc.com",
                            "nickname": "user012345789",
                            "email_confirmed": True,
                    },
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='400',
                value={
                    'message': status_messages[400],
                    'data': {},
                },
                response_only=True,
                status_codes=[400],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {},
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def patch(self, request):
        data = request.data
        user = request.user
        status_code, response_data = update(
            data=data,
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )

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
                    'data': {},
                },
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                name='500',
                value={
                    'message': status_messages[500],
                    'data': {},
                },
                response_only=True,
                status_codes=[500],
            ),
        ],
    )
    def delete(self, request):
        user = request.user
        status_code, response_data = remove(
            user=user,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )
