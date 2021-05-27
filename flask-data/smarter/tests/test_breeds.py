#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:47:24 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from .base import BaseCase, AuthMixin


class TestGetBreeds(AuthMixin, BaseCase):
    fixtures = [
        'user',
    ]

    test_endpoint = '/api/breeds'

    def test_empty_response(self):
        response = self.app.get(
            self.test_endpoint,
            headers=self.headers
        )

        reference = {
            'items': [],
            'next': None,
            'page': 1,
            'pages': 0,
            'prev': None,
            'size': 10,
            'total': 0
        }

        self.assertDictEqual(response.json, reference)
        self.assertEqual(response.status_code, 200)
