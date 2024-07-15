import uuid

from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import QueryDict
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from config.settings import SITE_PROTOCOL
from notifications.services import Email

from users.models import CustomUser
from users.serializers import (
    RegisterSerializer,
    AuthSerializer,
    RefreshAndLogoutSerializer,
    PasswordRestoreRequestSerializer, PasswordRestoreSerializer,
)

from utils.constants import (
    CONFIRM_EMAIL,
    PASSWORD_RESTORE,
)
from utils.logger import (
    get_logger,
    get_log_user_data,
)


logger = get_logger(__name__)


def register(data: QueryDict, host: str) -> (int, dict):
    '''
    Регистрация пользователя

    Args:
        data: данные пользователя
            {
              "email": "test_new@cc.com",
              "password": "test123",
              "confirm_password": "test123"
            }
        host: хост для создания полного url пути
            используется в отправке писем

    Returns:
        Код статуса и словарь данных
        200,
        {
            "refresh": "refresh_token",
            "access": "access_token"
        }
    '''

    user_data = get_log_user_data(
        user_data=dict(data),
    )
    logger.info(
        msg=f'Регистрация пользователя с данными {user_data}',
    )

    serializer = RegisterSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для регистрации пользователя '
                f'с данными {user_data}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
    except IntegrityError as exc:
        logger.error(
            msg=f'Пользователь с данными {user_data} уже существует: {exc}',
        )
        return 406, {}
    except Exception as exc:
        logger.error(
            msg=f'Не удалось создать пользователя с данными {user_data}: {exc}',
        )
        return 500, {}

    logger.info(
        msg=f'Успешно зарегистрирован пользователь с данными: {user_data}',
    )

    send_email_by_type(
        user=user,
        host=host,
        email_type=CONFIRM_EMAIL,
    )

    try:
        token = RefreshToken.for_user(
            user=user,
        )
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить токен для аутентификации пользователя '
                f'с данными {user_data} после регистрации: {exc}',
        )
        return 201, {}

    refresh = str(token)
    access = str(token.access_token)
    response_data = {
        'refresh': refresh,
        'access': access,
    }
    return 200, response_data


def auth(data: QueryDict) -> (int, dict):
    '''
    Аутентификация пользователя

    Args:
        data: данные пользователя
            {
              "email": "test@cc.com",
              "password": "test123"
            }

    Returns:
        Код статуса и словарь данных
        200,
        {
            "refresh": "refresh_token",
            "access": "access_token"
        }
    '''

    user_data = get_log_user_data(
        user_data=dict(data),
    )
    logger.info(
        msg=f'Аутентификация пользователя с данными: {user_data}',
    )

    serializer = AuthSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для аутентификации пользователя '
                f'с данными {user_data}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        user = authenticate(
            email=validated_data['email'],
            password=validated_data['password'],
        )
    except Exception as exc:
        logger.error(
            msg=f'Не удалось аутентифицировать пользователя с данными {user_data}: '
                f'{exc}',
        )
        return 500, {}

    if user is None:
        logger.error(
            msg=f'Не удалось аутентифицировать пользователя с данными {user_data}: '
                'неправильные email или пароль',
        )
        return 401, {}

    try:
        token = RefreshToken.for_user(
            user=user,
        )
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить токен для аутентификации пользователя '
                f'с данными {user_data}: {exc}',
        )
        return 500, {}

    refresh = str(token)
    access = str(token.access_token)
    response_data = {
        'refresh': refresh,
        'access': access,
    }
    logger.info(
        msg=f'Успешная аутентификация пользователя с данными: {user_data}',
    )
    return 200, response_data


def refresh_token(data: QueryDict) -> (int, dict):
    '''
    Обновление токена

    Args:
        data: данные для обновления
            {
              "refresh": "refresh_token"
            }

    Returns:
        Код статуса и словарь данных
        200,
        {
            "access": "access_token"
        }
    '''

    logger.info(
        msg='Обновление токена',
    )

    serializer = RefreshAndLogoutSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для обновления токена: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        refresh = RefreshToken(validated_data['refresh'])
    except Exception as exc:
        logger.error(
            msg=f'Не удалось обновить токен: {exc}',
        )
        return 403, {}

    response_data = {
        'access': str(refresh.access_token),
    }
    try:
        refresh.blacklist()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось занести токен в черный список: {exc}',
        )
        return 500, {}

    refresh.set_jti()
    refresh.set_iat()
    refresh.set_exp()
    response_data['refresh'] = str(refresh)
    logger.info(
        msg='Успешно обновлен токен'
    )
    return 200, response_data


def logout(data: QueryDict, user: CustomUser) -> (int, dict):
    '''
    Выход из системы

    Args:
        data: данные для выхода
            {
              "refresh": "refresh_token"
            }
        user: пользователь

    Returns:
        Код статуса и словарь данных
        200, {}
    '''

    logger.info(
        msg=f'Выход из системы пользователя {user}',
    )

    serializer = RefreshAndLogoutSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для выхода из системы пользователя {user}: '
                f'{serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        refresh = RefreshToken(validated_data['refresh'])
    except Exception as exc:
        logger.error(
            msg=f'Невалидный токен для выхода пользователя {user}: {exc}',
        )
        return 500, {}

    try:
        refresh.blacklist()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось занести токен пользователя {user} '
                f'в черный список: {exc}',
        )
        return 500, {}

    logger.info(
        msg=f'Успешный выход из системы пользователя {user}',
    )
    return 200, {}


def confirm_email(url_hash: str) -> (int, dict):
    '''
    Подтверждение email

    Args:
        url_hash: хэш

    Returns:
        Код статуса и словарь данных
        200, {}
    '''

    logger.info(
        msg=f'Подтверждение email пользователя с хэшем: {url_hash}',
    )

    try:
        user = CustomUser.objects.filter(
            url_hash=url_hash,
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибки при поиске пользователя с хэшем {url_hash} '
                f'для потвреждения email: {exc}',
        )
        return 500, {}

    if user is None:
        logger.error(
            msg=f'Не удалось найти пользователя с хэшем {url_hash} '
                'для подтвреждения email',
        )
        return 404, {}

    user.email_confirmed = True
    user.url_hash = None
    try:
        user.save()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось подтвердить email пользователя {user} '
                f'с хэшем {url_hash}: {exc}',
        )
        return 500, {}

    logger.info(
        msg=f'Успешно подтвержден email пользователя {user}',
    )
    return 200, {}


def password_restore_request(data: QueryDict, host: str) -> (int, dict):
    '''
    Запрос на восстановление пароля пользователя

    Args:
        data: данные пользователя
            {
              "email": "test@cc.com"
            }
        host: хост для создания полного url пути
                    используется в отправке писем

    Returns:
        Код статуса и словарь данных
        200, {}
    '''

    user_data = get_log_user_data(
        user_data=dict(data),
    )
    logger.info(
        msg=f'Запрос на восстановление пароля пользователя c данными {user_data}',
    )

    serializer = PasswordRestoreRequestSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg='Невалидные данные для запроса на восстановление пароля '
                f'пользователя c данными {user_data}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    try:
        user = CustomUser.objects.filter(
            email=validated_data['email'],
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при поиске пользователя с данными {user_data} '
                f'для запроса на восстановление пароля: {exc}',
        )
        return 500, {}

    if user is None:
        logger.error(
            msg='При запросе на восстановление пароля не найден '
                f'пользователь с данными {user_data} '
        )
        return 404, {}

    status_code = send_email_by_type(
        user=user,
        email_type=PASSWORD_RESTORE,
        host=host,
    )
    if status_code != 200:
        logger.error(
            msg='Запрос на восстановление пароля пользователя '
                f'с данными {user_data} не прошел',
        )
    else:
        logger.info(
            msg='Запрос на сброс пароля пользователя '
                f'с данными {user_data} прошел успешно',
        )
    return status_code, {}


def password_restore(data: QueryDict, url_hash: str) -> (int, dict):
    '''
    Восстановление пароля пользователя

    Args:
        url_hash: хэш
        data: данные пользователя
            {
              "new_password": "new_password123",
              "confirm_password": "new_password123"
            }

    Returns:
        Код статуса и словарь данных
        200, {}
    '''
    logger.info(
        msg=f'Восстановление пароля пользователя с хэшем: {url_hash}',
    )

    try:
        user = CustomUser.objects.filter(
            url_hash=url_hash,
        ).first()
    except Exception as exc:
        logger.error(
            msg=f'Возникла ошибка при поиске пользователя с хэшем {url_hash} '
                f'для восстановления пароля: {url_hash}'
        )
        return 500, {}

    if user is None:
        logger.error(
            msg=f'При восстановлении пароля не найден пользователь с хэшем: {url_hash}',
        )
        return 404, {}

    serializer = PasswordRestoreSerializer(
        data=data,
    )
    if not serializer.is_valid():
        logger.error(
            msg=f'Невалидные данные для восстановления пароля '
                f'пользователя {user} c хэшем {url_hash}: {serializer.errors}',
        )
        return 400, {}

    validated_data = serializer.validated_data
    user.set_password(validated_data['new_password'])
    user.url_hash = None
    try:
        user.save()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось восстановить пароль пользователя {user}: {exc}'
        )
        return 500, {}

    logger.info(
        msg=f'Успешно восстановлен пароль пользователя {user}',
    )
    return 200, {}


def send_email_by_type(user: CustomUser, email_type: str, host: str) -> int:
    '''
    Отправка письма по типу

    Args:
        user: пользователь
        email_type: тип письма
        host: хост для создания полного url пути
                    используется в отправке писем

    Returns:
        Код статуса
    '''

    logger.info(
        msg='Получение данных для формирования текста '
            f'письма {email_type} пользователю {user}',
    )

    url_hash = str(uuid.uuid4())
    user.url_hash = url_hash
    try:
        user.save()
    except Exception as exc:
        logger.error(
            msg=f'Не удалось получить данные для формирования текста письма {email_type} '
                f'пользователю {user}: {exc}',
        )
        return 500

    path = reverse(email_type, args=(user.url_hash,))
    url = f'{SITE_PROTOCOL}://{host}{path}'
    mail_data = {
        'url': url,
    }

    logger.info(
        msg=f'Данные для формирования текста письма {email_type} '
            f'пользователю {user} получены: {mail_data}',
    )

    email = Email(
        email_type=email_type,
        mail_data=mail_data,
        recipient=user,
    )
    status = email.send()
    return status