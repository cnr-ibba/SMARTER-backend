#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:37:31 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from werkzeug.urls import url_encode

from .base import BaseCase

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class SupportedChipTest(BaseCase):
    fixtures = [
        'user',
        'supportedChips'
    ]

    data_file = f"{FIXTURES_DIR}/supportedChips.json"
    test_endpoint = '/smarter-api/supported-chips/60c8c3a74c265e1880b28334'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(cls.data_file) as handle:
            cls.data = json.load(handle)

    def test_get_chip(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_chip_invalid(self):
        response = self.client.get(
            "/smarter-api/supported-chips/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_chip_not_found(self):
        response = self.client.get(
            "/smarter-api/supported-chips/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class SupportedChipListTest(BaseCase):
    fixtures = [
        'user',
        'supportedChips'
    ]

    data_file = f"{FIXTURES_DIR}/supportedChips.json"
    test_endpoint = '/smarter-api/supported-chips'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(cls.data_file) as handle:
            cls.data = json.load(handle)

    def test_get_chips(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 4)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 4)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_chips_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'name': 'AffymetrixAxiomOviCan'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[-1]])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_by_species(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'species': 'Goat'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[-2]])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_by_manufacturer(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'manufacturer': 'affymetrix'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[-1]])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_pagination(self):
        payload = {'page': 1, 'size': 2}

        response = self.client.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 4)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data[:2])
        self.assertIsNone(test['prev'])
        self.assertIsNotNone(test['next'])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_sort_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'name',
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[-1])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_sort_by_name_desc(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'name',
                'order': 'desc'
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_chips_unknown_arguments(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'foo': 'bar',
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            "Unknown arguments: foo", response.json['message'])
