#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:29:38 2022

@author: Paolo Cozzi <bunop@libero.it>
"""

import json
import pathlib

from werkzeug.urls import url_encode

from .base import BaseCase

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class TestGetCountryList(BaseCase):
    fixtures = [
        'user',
        'countries'
    ]

    test_endpoint = '/smarter-api/countries'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/countries.json") as handle:
            cls.data = json.load(handle)

    def test_get_countries(self):
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

    def test_get_countries_pagination(self):
        payload = {'page': 1, 'size': 1}

        response = self.client.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.data[:1])
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
        self.assertListEqual(test['items'], self.data[1:])
        self.assertIsNone(test['next'])
        self.assertIsNotNone(test['prev'])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_by_species(self):
        payload = {'species': 'Goat'}

        response = self.client.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertEqual(test['items'][0]['name'], "Italy")
        self.assertEqual(response.status_code, 200)

    def test_get_countries_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'name': 'Italy'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_by_alpha2_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'alpha_2': 'FR'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_by_wrong_alpha2_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'alpha_2': 'FRA'}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "is not an alpha2 country code",
            response.json['message']['alpha_2'])

    def test_get_countries_by_alpha3_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'alpha_3': 'ITA'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_by_wrong_alpha3_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'alpha_3': 'IT'}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "is not an alpha3 country code",
            response.json['message']['alpha_3'])

    def test_get_country_by_search(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'search': 'italian'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_sort_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'name',
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_sort_by_name_desc(self):
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

        self.assertEqual(test, self.data[1])
        self.assertEqual(response.status_code, 200)

    def test_get_countries_unknown_arguments(self):
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


class TestGetCountry(BaseCase):
    fixtures = [
        'user',
        'countries'
    ]

    test_endpoint = '/smarter-api/countries/621d0a5e4f7668dc81846f42'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/countries.json") as handle:
            cls.data = json.load(handle)[1]

    def test_get_countries(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)

    def test_get_countries_invalid(self):
        response = self.client.get(
            "/smarter-api/countries/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_countries_not_found(self):
        response = self.client.get(
            "/smarter-api/countries/621d0a5e4f7668dc81846f47",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)
