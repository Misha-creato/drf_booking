from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response_patterns import generate_response

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
