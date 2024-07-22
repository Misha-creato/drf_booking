from rest_framework import serializers


class DefaultResponse(serializers.Serializer):
    message = serializers.CharField(
        default='Сообщение',
    )
    data = serializers.JSONField(
        default={},
    )


class Register200Response(DefaultResponse):
    '''
    Регистрация пользователя

    Args: данные пользователя
        {
          "email": "test@cc.com",
          "password": "test123"
        }

    Returns:
        {
          "message": "Сообщение",
          "data": {
            "refresh": "refresh_token",
            "access": "access_token"
          }
        }
    '''

    data = serializers.JSONField(
        default={
            'refresh': 'refresh_token',
            'access': 'access_token',
        }
    )


class Auth200Response(DefaultResponse):
    '''
    Аутентификация пользователя

    Args: данные пользователя
        {
          "email": "test@cc.com",
          "password": "test123"
        }

    Returns:
        {
          "message": "Сообщение",
          "data": {
            "refresh": "refresh_token",
            "access": "access_token"
          }
        }
    '''

    data = serializers.JSONField(
        default={
            'refresh': 'refresh_token',
            'access': 'access_token',
        }
    )


class RefreshToken200Response(DefaultResponse):
    '''
    Обновление токена пользователя

    Args: токен
        {
          "refresh": "refresh_token"
        }

    Returns:
        {
          "message": "Сообщение",
          "data": {
            "refresh": "refresh_token",
            "access": "access_token"
          }
        }
    '''

    data = serializers.JSONField(
        default={
            'refresh': 'refresh_token',
            'access': 'access_token',
        }
    )


class Logout200Response(DefaultResponse):
    '''
    Выход из системы пользователя

    Args: токен
        {
          "refresh": "refresh_token"
        }

    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''


class ConfirmEmail200Response(DefaultResponse):
    '''
    Подтверждение email пользователя

    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''


class ConfirmEmailRequest200Response(DefaultResponse):
    '''
    Запрос на отправку письма для подтверждения email пользователя

    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''


class PasswordRestoreRequest200Response(DefaultResponse):
    '''
    Запрос на восстановление пароля пользователя

    Args:
        data: данные пользователя
            {
              "email": "test@cc.com"
            }
    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''


class PasswordRestore200Response(DefaultResponse):
    '''
    Восстановление пароля пользователя

    Args:
        data: данные пользователя
            {
              "new_password": "new_password123",
              "confirm_password": "new_password123"
            }
    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''


class Detail200Response(DefaultResponse):
    '''
    Данные пользователя

    Returns:
        {
          "message": "Сообщение",
          "data": {
                "email": "test@cc.com",
                "nickname": "user012345789",
                "email_confirmed": True,
            }
        }
    '''

    data = serializers.JSONField(
        default={
            "email": "test@cc.com",
            "nickname": "user012345789",
            "email_confirmed": True,
        }
    )


class Update200Response(DefaultResponse):
    '''
    Обновление данных пользователя
    Args:
        data: данные пользователя
            {
              "nickname": "new_nickname",
              "old_password": "old_password123",
              "new_password": "new_password123",
              "confirm_password": "new_password123",
            }

    Returns:
        {
          "message": "Сообщение",
          "data": {
                "email": "test@cc.com",
                "nickname": "new_nickname",
                "email_confirmed": True,
            }
        }
    '''

    data = serializers.JSONField(
        default={
            "email": "test@cc.com",
            "nickname": "user012345789",
            "email_confirmed": True,
        }
    )


class Remove200Response(DefaultResponse):
    '''
    Удаление пользователя

    Returns:
        {
          "message": "Сообщение",
          "data": {}
        }
    '''
