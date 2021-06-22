#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:53:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from dateutil.parser import parse as parse_date
from bson import json_util

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class DateMixin():
    """Solve issues with dates from mongodb data"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(cls.data_file) as handle:
            data = json.load(handle)

        for i, record in enumerate(data):
            # fix date in locations
            for j, location in enumerate(record['locations']):
                if 'date' in location:
                    location['date'] = parse_date(location['date']['$date'])
                    record['locations'][j] = location

            data[i] = record

        # dump data like mongodb does
        tmp = json.dumps(data, default=json_util.default)

        # tracking data
        cls.data = json.loads(tmp)


class VariantSheepTest(DateMixin, AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantSheep'
    ]

    data_file = f"{FIXTURES_DIR}/variantSheep.json"
    test_endpoint = '/api/variants/sheep/60ca279a8025a403796f644a'

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data[0])


class VariantSheepListTest(DateMixin, AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantSheep'
    ]

    data_file = f"{FIXTURES_DIR}/variantSheep.json"
    test_endpoint = '/api/variants/sheep'

    def test_get_variants(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)


class VariantGoatTest(DateMixin, AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantGoat'
    ]

    data_file = f"{FIXTURES_DIR}/variantGoat.json"
    test_endpoint = '/api/variants/goat/60ca4dabd8f09cfd319da0f8'

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data[0])


class VariantGoatListTest(DateMixin, AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantGoat'
    ]

    data_file = f"{FIXTURES_DIR}/variantGoat.json"
    test_endpoint = '/api/variants/goat'

    def test_get_variants(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)
