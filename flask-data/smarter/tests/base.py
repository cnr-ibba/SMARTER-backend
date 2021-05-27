#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:06:11 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import unittest
import pathlib

from app import create_app
from database.db import db, DB_ALIAS

# start application with custom values
app = create_app(config={'host': 'mongodb://mongo/test'})


class BaseCase(unittest.TestCase):
    fixtures = []

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.db = db.get_db(alias=DB_ALIAS)

        # try to upload data into database
        for fixture in cls.fixtures:
            data_file = next(pathlib.Path('tests').glob(f"**/{fixture}.json"))
            with open(data_file) as handle:
                data = json.load(handle)
                collection = cls.db[fixture]
                collection.insert_many(data)

    @classmethod
    def tearDownClass(cls):
        # Delete Database collections after the test is complete
        for collection in cls.db.list_collection_names():
            cls.db.drop_collection(collection)
