#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:26:29 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class SampleSheepTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleSheep'
    ]

    test_endpoint = '/api/samples/sheep/608ab4b191a0d06725bc0938'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/sampleSheep.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_sample(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)

    def test_get_sample_invalid(self):
        response = self.client.get(
            "/api/samples/sheep/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_sample_not_found(self):
        response = self.client.get(
            "/api/samples/sheep/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class SampleSheepListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleSheep'
    ]

    test_endpoint = '/api/samples/sheep'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/sampleSheep.json") as handle:
            cls.data = json.load(handle)

    def test_get_samples(self):
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


class SampleGoatTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleGoat'
    ]

    test_endpoint = '/api/samples/goat/6092940199215a3814492195'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/sampleGoat.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_sample(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)

    def test_get_sample_invalid(self):
        response = self.client.get(
            "/api/samples/goat/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_sample_not_found(self):
        response = self.client.get(
            "/api/samples/goat/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class SampleGoatListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleGoat'
    ]

    test_endpoint = '/api/samples/goat'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/sampleGoat.json") as handle:
            cls.data = json.load(handle)

    def test_get_samples(self):
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
