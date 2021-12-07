# -*- coding: utf-8 -*-
import json
import pathlib

from dateutil.parser import parse as parse_date

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class TestSmarterInfo(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'smarterInfo'
    ]

    test_endpoint = '/api/info'
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/smarterInfo.json") as handle:
            cls.data = json.load(handle)[0]

        cls.data['last_updated']['$date'] = parse_date(
            cls.data['last_updated']['$date']
        ).timestamp() * 1000

    def test_get_info(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)
        self.assertEqual(response.status_code, 200)
