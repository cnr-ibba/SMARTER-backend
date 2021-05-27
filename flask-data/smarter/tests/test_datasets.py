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


class TestGetDatasets(AuthMixin, BaseCase):
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
