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

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Texel'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'TEX'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_chip_name(self):
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

    def test_get_samples_by_multiple_chip_names(self):
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

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'Italy'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_original_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'original_id': 'sheep1'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_smarter_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'smarter_id': 'ITOA-TEX-000000001'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b58'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

        # this query doesn't return results
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b5b'}
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_locations__exists(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'locations__exists': 'True'}
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_phenotype__exists(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'phenotype__exists': 'True'}
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'background'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_pagination(self):
        payload = {'page': 1, 'size': 1}

        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string=payload,
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.data[:1])
        self.assertIsNone(test['prev'])
        self.assertIsNotNone(test['next'])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_sort_by_smarter_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'smarter_id',
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[-1])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_sort_by_smarter_id_desc(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'smarter_id',
                'order': 'desc'
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_unknown_arguments(self):
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

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Cashmere'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'CAS'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaGoatSNP50'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'France'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_original_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'original_id': 'ES_MAL0001'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_smarter_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'smarter_id': 'ESCH-MAL-000000001'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[0]])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b5b'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

        # this query doesn't return results
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b58'}
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_locations__exists(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'locations__exists': 'True'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_phenotype__exists(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'phenotype__exists': 'True'}
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 2)
        self.assertListEqual(test['items'], self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'foreground'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_samples_pagination(self):
        payload = {'page': 1, 'size': 1}

        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string=payload,
        )

        test = response.json

        self.assertEqual(test['total'], 2)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], self.data[:1])
        self.assertIsNone(test['prev'])
        self.assertIsNotNone(test['next'])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_sort_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'breed',
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[-1])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_sort_by_breed_desc(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'sort': 'breed',
                'order': 'desc'
            }
        )

        # get first result
        test = response.json['items'][0]

        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_samples_unknown_arguments(self):
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
