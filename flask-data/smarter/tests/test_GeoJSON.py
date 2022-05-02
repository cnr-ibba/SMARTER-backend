#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:43:33 2021

@author: Paolo Cozzi <bunop@libero.it>
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

    test_endpoint = (
        '/smarter-api/samples.geojson/sheep/608ab4b191a0d06725bc0938')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(f"{FIXTURES_DIR}/sampleSheep.json") as handle:
            cls.data = json.load(handle)[0]

    def test_get_sample_invalid(self):
        response = self.client.get(
            "/smarter-api/samples/sheep/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_sample_not_found(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class SampleGoatTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleGoat'
    ]

    test_endpoint = (
        '/smarter-api/samples.geojson/goat/6092940199215a3814492195')

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

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "Feature")
        self.assertIn('properties', test)
        self.assertIn('geometry', test)

    def test_get_sample_invalid(self):
        response = self.client.get(
            "/smarter-api/samples.geojson/goat/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_sample_not_found(self):
        response = self.client.get(
            "/smarter-api/samples.geojson/goat/604f75a61a08c53cebd09b58",
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

    test_endpoint = '/smarter-api/samples.geojson/sheep'

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

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Texel'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'TEX'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'Italy'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaOvineSNP50'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b58'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'background'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)


class SampleGoatListTest(AuthMixin, BaseCase):
    fixtures = [
        'user',
        'sampleGoat'
    ]

    test_endpoint = '/smarter-api/samples.geojson/goat'

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

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 2)

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Cashmere'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 1)
        self.assertEqual(
            test['features'][0]['properties']['smarter_id'],
            "ESCH-MAL-000000001"
        )

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'CAS'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 1)
        self.assertEqual(
            test['features'][0]['properties']['smarter_id'],
            "ESCH-MAL-000000001"
        )

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'Italy'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaGoatSNP50'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 2)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b5b'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 2)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'background'}
        )

        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 1)
        self.assertEqual(
            test['features'][0]['properties']['smarter_id'],
            "ESCH-MAL-000000001"
        )
