import json
import os

from django.test import TestCase

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from areas.api import AreaListView
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
        view = AreaListView

        path = f'{self.path}/get_areas'
        fixtures = (
            (200, 'valid_ordering'),
            (200, 'valid_search'),
            (200, 'valid_filters'),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'

            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            factory = APIRequestFactory()
            request = factory.get('/', data)
            request = Request(request)
            status_code, response_data = get_areas(
                request=request,
                filter_backends=view.filter_backends,
                view=view,
            )
            print(response_data)
            self.assertEqual(status_code, status_code, msg=fixture)

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

