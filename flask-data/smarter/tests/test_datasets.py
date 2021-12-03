#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:39:27 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from werkzeug.urls import url_encode

from .base import BaseCase, AuthMixin

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class TestGetDatasetList(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'dataset'
    ]

    test_endpoint = '/api/datasets'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/dataset.json") as handle:
            cls.data = json.load(handle)

        # get goat items
        cls.goats_data = list()

        for item in cls.data:
            if item['species'] == 'Goat':
                cls.goats_data.append(item)

    def test_get_datasets(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        print(response.json)

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_by_species(self):
        payload = {'species': 'Goat'}

        response = self.client.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.goats_data)
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_pagination(self):
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

    def test_get_datasets_by_species_pagination(self):
        payload = {'species': 'Goat', 'size': 1}

        response = self.client.get(
            "?".join([self.test_endpoint, url_encode(payload)]),
            headers=self.headers
        )

        test = response.json

        # only one result for goats
        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.goats_data)
        self.assertIsNone(test['prev'])
        self.assertIsNone(test['next'])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'foreground'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_by_multiple_types(self):
        response = self.client.get(
            self.test_endpoint + "?type=genotypes&type=background",
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_by_search(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'search': 'test.map'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_sort_by_file(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'file',
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[1])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_sort_by_file_desc(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'file',
                'order': 'desc'
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_unknown_arguments(self):
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

    def test_get_datasets_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaOvineSNP50'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_datasets_by_multiple_chip_names(self):
        response = self.client.get(
            self.test_endpoint + (
                "?chip_name=IlluminaOvineSNP50&"
                "chip_name=AffymetrixAxiomOviCan"),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)


class TestGetDataset(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'dataset'
    ]

    test_endpoint = '/api/datasets/604f75a61a08c53cebd09b58'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/dataset.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_dataset(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data)

    def test_get_breed_invalid(self):
        response = self.client.get(
            "/api/datasets/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_breed_not_found(self):
        response = self.client.get(
            "/api/datasets/608ab46e1031c98150016dbd",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)
