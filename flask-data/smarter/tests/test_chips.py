#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:37:31 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class SupportedChipTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'supportedChips'
    ]

    data_file = f"{FIXTURES_DIR}/supportedChips.json"
    test_endpoint = '/api/supported-chips/60c8c3a74c265e1880b28334'

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
            "/api/supported-chips/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_chip_not_found(self):
        response = self.client.get(
            "/api/supported-chips/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class SupportedChipListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'supportedChips'
    ]

    data_file = f"{FIXTURES_DIR}/supportedChips.json"
    test_endpoint = '/api/supported-chips'

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
