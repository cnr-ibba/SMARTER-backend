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


class TestGetBreedList(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'breeds'
    ]

    test_endpoint = '/smarter-api/breeds'

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

    def test_get_breeds_pagination(self):
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

        # get next page
        response = self.client.get(
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

        response = self.client.get(
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

        response = self.client.get(
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
        response = self.client.get(
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

    def test_get_breed_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'name': 'Texel'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_by_multiple_names(self):
        response = self.client.get(
            self.test_endpoint + (
                "?name=Texel&"
                "name=Merino"),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data[:2])
        self.assertEqual(response.status_code, 200)

    def test_get_breed_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'code': 'TEX'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_by_multiple_codes(self):
        response = self.client.get(
            self.test_endpoint + (
                "?code=TEX&"
                "code=MER"),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data[:2])
        self.assertEqual(response.status_code, 200)

    def test_get_breed_by_species(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'species': 'Sheep'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data[:2])
        self.assertEqual(response.status_code, 200)

    def test_get_breed_by_search(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'search': 'merino'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

        # the same query in goat species return no results
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'search': 'merino',
                'species': 'Goat'
            }
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_breeds_sort_by_name(self):
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

    def test_get_breeds_sort_by_name_desc(self):
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

    def test_get_breeds_unknown_arguments(self):
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


class TestGetBreed(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'breeds'
    ]

    test_endpoint = '/smarter-api/breeds/608ab46e1031c98150016dbd'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/breeds.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)

    def test_get_breed_invalid(self):
        response = self.client.get(
            "/smarter-api/breeds/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_breed_not_found(self):
        response = self.client.get(
            "/smarter-api/breeds/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)
