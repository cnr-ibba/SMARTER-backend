#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:47:24 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from werkzeug.urls import url_encode

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class TestGetBreeds(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'breeds'
    ]

    test_endpoint = '/api/breeds'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/breeds.json") as handle:
            cls.data = json.load(handle)

        # get goat items
        cls.goats_data = list()

        for item in cls.data:
            if item['species'] == 'Goat':
                cls.goats_data.append(item)

    def test_get_breeds(self):
        response = self.app.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 4)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 4)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_pagination(self):
        payload = {'page': 1, 'size': 2}

        response = self.app.get(
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

        # get next page
        response = self.app.get(
            test['next'],
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 4)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data[2:])
        self.assertIsNone(test['next'])
        self.assertIsNotNone(test['prev'])
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_by_species(self):
        payload = {'species': 'Goat'}

        response = self.app.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.goats_data)
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_by_species_pagination(self):
        payload = {'species': 'Goat', 'size': 1}

        response = self.app.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.goats_data[:1])
        self.assertIsNone(test['prev'])
        self.assertIsNotNone(test['next'])
        self.assertEqual(response.status_code, 200)

        # get next page
        response = self.app.get(
            test['next'],
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.goats_data[1:])
        self.assertIsNone(test['next'])
        self.assertIsNotNone(test['prev'])
        self.assertEqual(response.status_code, 200)


class TestGetBreed(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'breeds'
    ]

    test_endpoint = '/api/breeds/608ab46e1031c98150016dbd'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/breeds.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_breed(self):
        response = self.app.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)
