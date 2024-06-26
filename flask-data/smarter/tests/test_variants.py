#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:53:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import pathlib

from dateutil.parser import parse as parse_date
from bson import json_util

from .base import BaseCase

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


class DateMixin():
    """Solve issues with dates from mongodb data"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(cls.data_file) as handle:
            data = json.load(handle)

        for i, record in enumerate(data):
            # fix date in locations
            for j, location in enumerate(record['locations']):
                if 'date' in location:
                    location['date'] = parse_date(location['date']['$date'])
                    record['locations'][j] = location

            data[i] = record

        # dump data like mongodb does
        tmp = json.dumps(data, default=json_util.default)

        # tracking data
        cls.data = json.loads(tmp)


class VariantSheepTest(DateMixin, BaseCase):
    fixtures = [
        'user',
        'variantSheep'
    ]

    data_file = f"{FIXTURES_DIR}/variantSheep.json"
    test_endpoint = '/smarter-api/variants/sheep/60ca279a8025a403796f644a'

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_invalid(self):
        response = self.client.get(
            "/smarter-api/variants/sheep/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_variant_not_found(self):
        response = self.client.get(
            "/smarter-api/variants/sheep/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class VariantSheepListMixin(DateMixin):
    # print out all the differences
    maxDiff = None

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

    def test_get_variant_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'name': '250506CS3900140500001_312.1'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_rs_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'rs_id': 'rs55630642'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_chip_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'chip_name': 'IlluminaOvineHDSNP'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_probeset_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'probeset_id': 'AX-123240316'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_cust_id(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'cust_id': '250506CS3900140500001_312_01'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_region(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'region': '23:26298007-26298027'
            }
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_chrom(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'region': '23'
            }
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_wrong_region(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'region': '23:26298007'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "is not a valid region",
            response.json['message']['region'])

    def test_get_variant_by_region_quote(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'region': '23%3A26298007-26298027'
            }
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_pagination(self):
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

    def test_get_variant_sort_by_name(self):
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

    def test_get_variant_sort_by_name_desc(self):
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

        self.assertEqual(test, self.data[-1])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_unknown_arguments(self):
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

    def test_get_variant_by_multiple_chips(self):
        response = self.client.get(
            self.test_endpoint + (
                "?chip_name=IlluminaOvineSNP50&chip_name=IlluminaOvineHDSNP"),
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)


class VariantSheepOAR3Test(VariantSheepListMixin, BaseCase):
    fixtures = [
        'user',
        'smarterInfo',
        'variantSheep'
    ]

    data_file = f"{FIXTURES_DIR}/variantSheep.json"
    test_endpoint = '/smarter-api/variants/sheep/OAR3'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # need to drop unwanted information from location
        OAR3 = {
            'version': 'Oar_v3.1',
            'imported_from': 'SNPchiMp v.3'
        }

        for i, variant in enumerate(cls.data):
            for j, location in enumerate(variant['locations']):
                if (location['version'] == OAR3['version'] and
                        location['imported_from'] == OAR3['imported_from']):
                    break

            variant['locations'] = [location]

            # drop unwanted keys
            del variant['sender']
            del variant['illumina_top']

            cls.data[i] = variant


class VariantSheepOAR4Test(DateMixin, BaseCase):
    fixtures = [
        'user',
        'smarterInfo',
        'variantSheep'
    ]

    data_file = f"{FIXTURES_DIR}/variantSheep.json"
    test_endpoint = '/smarter-api/variants/sheep/OAR4'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # need to drop unwanted information from location
        OAR4 = {
            'version': 'Oar_v4.0',
            'imported_from': 'SNPchiMp v.3'
        }

        for i, variant in enumerate(cls.data):
            for j, location in enumerate(variant['locations']):
                if (location['version'] == OAR4['version'] and
                        location['imported_from'] == OAR4['imported_from']):
                    break

            variant['locations'] = [location]

            # drop unwanted keys
            del variant['sender']
            del variant['illumina_top']

            cls.data[i] = variant

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


class VariantGoatTest(DateMixin, BaseCase):
    fixtures = [
        'user',
        'variantGoat'
    ]

    data_file = f"{FIXTURES_DIR}/variantGoat.json"
    test_endpoint = '/smarter-api/variants/goat/60ca4dabd8f09cfd319da0f8'

    def test_get_variant(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertEqual(test, self.data[0])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_invalid(self):
        response = self.client.get(
            "/smarter-api/variants/goat/foo",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("not a valid ObjectId", test["message"])
        self.assertEqual(response.status_code, 400)

    def test_get_variant_not_found(self):
        response = self.client.get(
            "/smarter-api/variants/goat/604f75a61a08c53cebd09b58",
            headers=self.headers
        )

        test = response.json

        self.assertIsInstance(test, dict)
        self.assertIn("Object does not exist", test["message"])
        self.assertEqual(response.status_code, 404)


class VariantGoatListMixin(DateMixin):
    # print out all the differences
    maxDiff = None

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

    def test_get_variant_by_name(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={'name': '1_10408764_AF-PAKI'}
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_by_chip_name(self):
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

    def test_get_variant_by_region(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers,
            query_string={
                'region': '1:10408754-10408774'
            }
        )

        test = response.json

        self.assertEqual(test['total'], 1)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 1)
        self.assertListEqual(test['items'], [self.data[1]])
        self.assertEqual(response.status_code, 200)

    def test_get_variant_pagination(self):
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

    def test_get_variant_sort_by_name(self):
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

    def test_get_samples_sort_by_name_desc(self):
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

        self.assertEqual(test, self.data[-1])
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


class VariantGoatARS1Test(VariantGoatListMixin, BaseCase):
    fixtures = [
        'user',
        'smarterInfo',
        'variantGoat'
    ]

    data_file = f"{FIXTURES_DIR}/variantGoat.json"
    test_endpoint = '/smarter-api/variants/goat/ARS1'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # need to drop unwanted information from location
        ARS1 = {
            'version': 'ARS1',
            'imported_from': 'manifest'
        }

        for i, variant in enumerate(cls.data):
            for j, location in enumerate(variant['locations']):
                if (location['version'] == ARS1['version'] and
                        location['imported_from'] == ARS1['imported_from']):
                    break

            variant['locations'] = [location]

            # drop unwanted keys
            del variant['sender']
            del variant['illumina_top']

            cls.data[i] = variant


class VariantGoatCHI1Test(DateMixin, BaseCase):
    fixtures = [
        'user',
        'smarterInfo',
        'variantGoat'
    ]

    data_file = f"{FIXTURES_DIR}/variantGoat.json"
    test_endpoint = '/smarter-api/variants/goat/CHI1'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # need to drop unwanted information from location
        CHI1 = {
            'version': 'CHI1',
            'imported_from': 'manifest'
        }

        for i, variant in enumerate(cls.data):
            for j, location in enumerate(variant['locations']):
                if (location['version'] == CHI1['version'] and
                        location['imported_from'] == CHI1['imported_from']):
                    break

            variant['locations'] = [location]

            # drop unwanted keys
            del variant['sender']
            del variant['illumina_top']

            cls.data[i] = variant

    def test_get_variants(self):
        response = self.client.get(
            self.test_endpoint,
            headers=self.headers
        )

        test = response.json

        self.assertEqual(test['total'], 0)
        self.assertIsInstance(test['items'], list)
        self.assertEqual(len(test['items']), 0)
        self.assertListEqual(test['items'], [])
        self.assertEqual(response.status_code, 200)
