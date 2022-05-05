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

    def check_no_results(self, response):
        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), 0)

    def test_get_samples(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Texel'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_breeds(self):
        response = self.client.get(
            self.test_endpoint + (
                "?breed=Texel&"
                "breed=Merino"),
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'TEX'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_breed_codes(self):
        response = self.client.get(
            self.test_endpoint + (
                "?breed_code=TEX&"
                "breed_code=MER"),
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaOvineSNP50'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_chip_names(self):
        response = self.client.get(
            self.test_endpoint + (
                "?chip_name=IlluminaOvineSNP50&"
                "chip_name=AffymetrixAxiomOviCan"),
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'Italy'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_countries(self):
        response = self.client.get(
            self.test_endpoint + (
                "?country=Italy&"
                "country=France"),
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b58'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_dataset_ids(self):
        response = self.client.get(
            self.test_endpoint + (
                "?dataset=604f75a61a08c53cebd09b58&"
                "dataset=604f75a61a08c53cebd09b5b"),
            headers=self.headers
        )

        self.check_no_results(response)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'background'}
        )

        self.check_no_results(response)


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

    def check_no_results(self, response):
        self.check_results(response, n_of_results=0)

    def check_both_results(self, response):
        self.check_results(response, n_of_results=2)

    def check_first_result(self, response):
        self.check_results(response, n_of_results=1)

        test = response.json

        self.assertEqual(
            test['features'][0]['properties']['smarter_id'],
            "ESCH-MAL-000000001"
        )

    def check_results(self, response, n_of_results=0):
        test = response.json

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(test, dict)
        self.assertEqual(test['type'], "FeatureCollection")
        self.assertIn('features', test)
        self.assertIsInstance(test['features'], list)
        self.assertEqual(len(test['features']), n_of_results)

    def test_get_samples(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_breed(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed': 'Cashmere'}
        )

        self.check_first_result(response)

    def test_get_samples_by_multiple_breeds(self):
        response = self.client.get(
            self.test_endpoint + (
                "?breed=Cashmere&"
                "breed=Bari"),
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_breed_code(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'breed_code': 'CAS'}
        )

        self.check_first_result(response)

    def test_get_samples_by_multiple_breed_codes(self):
        response = self.client.get(
            self.test_endpoint + (
                "?breed_code=CAS&"
                "breed_code=BRI"),
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaGoatSNP50'}
        )

        self.check_both_results(response)

    def test_get_samples_by_multiple_chip_names(self):
        response = self.client.get(
            self.test_endpoint + (
                "?chip_name=IlluminaGoatSNP50&"
                "chip_name=AffymetrixAxiomOviCan"),
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_country(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'country': 'Italy'}
        )

        self.check_no_results(response)

    def test_get_samples_by_multiple_countries(self):
        response = self.client.get(
            self.test_endpoint + (
                "?country=France&"
                "country=Italy"),
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_dataset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'dataset': '604f75a61a08c53cebd09b5b'}
        )

        self.check_both_results(response)

    def test_get_samples_by_multiple_dataset_ids(self):
        response = self.client.get(
            self.test_endpoint + (
                "?dataset=604f75a61a08c53cebd09b5b&"
                "dataset=604f75a61a08c53cebd09b5b"),
            headers=self.headers
        )

        self.check_both_results(response)

    def test_get_samples_by_type(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'type': 'background'}
        )

        self.check_first_result(response)
