import json
import os

from django.test import TestCase

from areas.services import (
    get_areas,
    get_area,
    search_by_name,
    filter_by_params,
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

    def test_search_by_name(self):
        path = f'{self.path}/search_by_name'
        fixtures = (
            (200, 'valid'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, response_data = search_by_name(
                name=data['name'],
            )
            print(response_data)
            self.assertEqual(status_code, code, msg=fixture)

    def test_filter_by_params(self):
        path = f'{self.path}/filter_by_params'
        fixtures = (
            (200, 'valid'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, response_data = filter_by_params(
                params=data,
            )
            print(response_data)
            self.assertEqual(status_code, code, msg=fixture)
