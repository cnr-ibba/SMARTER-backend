# -*- coding: utf-8 -*-
import json
import pathlib

from .base import BaseCase

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class TestSmarterInfo(BaseCase):
    fixtures = [
        'user',
        'smarterInfo'
    ]

    test_endpoint = '/smarter-api/info'
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/smarterInfo.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_info(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)
        self.assertEqual(response.status_code, 200)
