import json
import os

from django.test import TestCase

from areas.services import (
    get_areas,
    get_area,
)


CUR_DIR = os.path.dirname(__file__)


class ServicesTest(TestCase):
    fixtures = ['contacts.json', 'areas.json']

    @classmethod
    def setUpTestData(cls):
        cls.path = f'{CUR_DIR}/fixtures/services'

    def test_get_areas(self):
        status_code, response_data = get_areas()
        print(response_data)
        self.assertEqual(status_code, 200)

    def test_get_area(self):
        path = f'{self.path}/get_area'
        fixtures = (
            (200, 'valid'),
            (404, 'not_found'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, response_data = get_area(
                pk=data['pk'],
            )
            print(response_data)
            self.assertEqual(status_code, code, msg=fixture)

