import json
import os
from datetime import datetime

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from bookings.models import BookingSettings
from bookings.services import (
    user_booking_history,
    user_booking_temporary,
    get_area_booking_temporary,
    get_area_qr_data,
    area_qr_check,
    booking_area,
)

from utils.redis_cache import redis_client


CUR_DIR = os.path.dirname(__file__)
User = get_user_model()


class ServicesTest(TestCase):
    fixtures = ['contacts.json', 'areas.json', 'users.json', 'booking_area.json']

    @classmethod
    def setUpTestData(cls):
        cls.path = f'{CUR_DIR}/fixtures/services'
        with open(f'{CUR_DIR}/fixtures/booking_temporary.json') as file:
            booking_temporary = json.load(file)
        for booking in booking_temporary:
            redis_client.setex(booking['key'], 5, json.dumps(booking['data']))
        cls.booking_settings = BookingSettings.temporary_timeout.default = 5

    @patch('django.utils.timezone.now')
    def test_booking_area(self, mock_timezone):
        dt = datetime(2024, 8, 1, tzinfo=timezone.utc)
        mock_timezone.return_value = dt
        user = User.objects.get(pk=2)

        path = f'{self.path}/booking_area'
        fixtures = (
            (200, 'valid_temporary'),
            (200, 'valid_constant'),
            (400, 'invalid'),
            (400, 'invalid_dates'),
            (404, 'not_found'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, response_data = booking_area(
                area_pk=data['area_pk'],
                data=data['data'],
                user=user,
            )
            self.assertEqual(status_code, code, msg=fixture)

    def test_user_booking_history(self):
        user = User.objects.get(pk=2)
        status_code, response_data = user_booking_history(
            user=user,
        )
        print(response_data)
        self.assertEqual(status_code, 200)

    def test_user_booking_temporary(self):
        user = User.objects.get(pk=1)
        status_code, response_data = user_booking_temporary(
            user=user,
        )
        print(response_data)
        self.assertEqual(status_code, 200)

    def test_get_area_booking_temporary(self):
        status_code, response_data = get_area_booking_temporary(
            area_pk=1,
        )
        print(response_data)
        self.assertEqual(status_code, 200)

    def test_get_area_qr_data(self):
        path = f'{self.path}/get_area_qr_data'
        fixtures = (
            (200, 'valid'),
            (400, 'invalid'),
            (410, 'does_not_exist'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

                status_code, response_data = get_area_qr_data(
                    data=data,
                )

            self.assertEqual(status_code, code, msg=fixture)

    def test_area_qr_check(self):
        path = f'{self.path}/area_qr_check'
        fixtures = (
            (200, 'valid'),
            (400, 'already_started'),
            (400, 'invalid'),
            (410, 'does_not_exist'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

                status_code, response_data = area_qr_check(
                    data=data,
                )

            self.assertEqual(status_code, code, msg=fixture)
