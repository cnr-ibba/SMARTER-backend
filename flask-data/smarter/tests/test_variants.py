#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:53:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class VariantSheepTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantSheep'
    ]

    test_endpoint = '/api/variants/sheep/60ca279a8025a403796f644a'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/variantSheep.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)


class VariantSheepListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantSheep'
    ]

    test_endpoint = '/api/variants/sheep'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/variantSheep.json") as handle:
            cls.data = json.load(handle)

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


class VariantGoatTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantGoat'
    ]

    test_endpoint = '/api/variants/goat/60ca4dabd8f09cfd319da0f8'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/variantGoat.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)


class VariantGoatListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'variantGoat'
    ]

    test_endpoint = '/api/variants/goat'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/variantGoat.json") as handle:
            cls.data = json.load(handle)

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
