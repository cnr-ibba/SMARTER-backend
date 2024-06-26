#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:06:11 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os
import json
import logging
import unittest
import pathlib

from bson.objectid import ObjectId
from pymongo.errors import BulkWriteError
from dateutil.parser import parse as parse_date

from app import create_app
from database.db import db, DB_ALIAS

# start application an override the default configuration
os.environ['MONGODB_SMARTER_DB'] = 'mongodb://mongo/test'
app = create_app()

# Get an instance of a logger
logger = logging.getLogger(__name__)


def sanitize_record(record):
    """Remove $oid values from data and replace with bson ObjectId"""

    for key, value in record.items():
        if isinstance(value, dict):
            if "$oid" in value:
                record[key] = ObjectId(value["$oid"])

            elif '$date' in value:
                logger.debug(f"fix '{key}': {value['$date']}")
                record[key] = parse_date(value['$date'])

            else:
                # call recursively this function
                record[key] = sanitize_record(value)

        elif isinstance(value, list):
            record[key] = sanitize_data(value)

    return record


def sanitize_data(data):
    """Process a list of records"""

    sanitized = list()

    for record in data:
        if isinstance(record, dict):
            sanitized.append(sanitize_record(record))

        else:
            sanitized.append(record)

    return sanitized


class BaseCase(unittest.TestCase):
    fixtures = []

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = app.test_client()
        cls.db = db.get_db(alias=DB_ALIAS)

        if cls.db.list_collection_names():
            logger.error(
                f"Database has data: {cls.db.list_collection_names()}")
            logger.error("Please drop data from it before applying tests")

        # try to upload data into database
        for fixture in cls.fixtures:
            logger.debug(f"Search for {fixture}")
            data_file = next(pathlib.Path('tests').glob(f"**/{fixture}.json"))

            logger.debug(f"Found {data_file}")

            with open(data_file) as handle:
                data = json.load(handle)
                data = sanitize_data(data)

                collection = cls.db[fixture]
                try:
                    collection.insert_many(data)

                except BulkWriteError as e:
                    logger.error(f"Cannot insert data: {e}")

        # create and empty header attributes (for compatibility)
        cls.headers = {}

    @classmethod
    def tearDownClass(cls):
        # Delete Database collections after the test is complete
        for collection in cls.db.list_collection_names():
            cls.db.drop_collection(collection)
