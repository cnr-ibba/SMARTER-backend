#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:09:08 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import mongoengine
import flask_mongoengine2.connection
from flask_mongoengine2 import MongoEngine
from pymongo import ReadPreference, uri_parser

db = MongoEngine()

DB_ALIAS = "smarterdb"


def initialize_db(app):
    db.init_app(app)


def _sanitize_settings(settings):
    """Given a dict of connection settings, sanitize the keys and fall
    back to some sane defaults.
    """
    # Remove the "MONGODB_" prefix and make all settings keys lower case.
    resolved_settings = {}
    for k, v in settings.items():
        if k.startswith("MONGODB_"):
            k = k[len("MONGODB_"):]
        k = k.lower()
        resolved_settings[k] = v

    # Handle uri style connections
    if "://" in resolved_settings.get("host", ""):
        # this section pulls the database name from the URI
        # PyMongo requires URI to start with mongodb:// to parse
        # this workaround allows mongomock to work
        uri_to_check = resolved_settings["host"]

        if uri_to_check.startswith("mongomock://"):
            uri_to_check = uri_to_check.replace("mongomock://", "mongodb://")

        uri_dict = uri_parser.parse_uri(uri_to_check)
        resolved_settings["db"] = uri_dict["database"]

    # Add a default name param or use the "db" key if exists
    if resolved_settings.get("db"):
        resolved_settings["name"] = resolved_settings.pop("db")
    else:
        resolved_settings["name"] = "test"

    # Add various default values.
    # TODO do we have to specify it here? MongoEngine should take care of that
    resolved_settings["alias"] = resolved_settings.get(
        "alias", mongoengine.DEFAULT_CONNECTION_NAME
    )
    # TODO this is the default host in pymongo.mongo_client.MongoClient,
    # we may not need to explicitly set a default here
    resolved_settings["host"] = resolved_settings.get(
        "host", "localhost"
    )
    # TODO this is the default port in pymongo.mongo_client.MongoClient,
    # we may not need to explicitly set a default here
    resolved_settings["port"] = resolved_settings.get(
        "port", 27017
    )

    # Default to ReadPreference.PRIMARY if no read_preference is supplied
    resolved_settings["read_preference"] = resolved_settings.get(
        "read_preference", ReadPreference.PRIMARY
    )

    # Clean up empty values
    for k, v in list(resolved_settings.items()):
        if v is None:
            del resolved_settings[k]

    # add a custom setting for mongodb connection
    resolved_settings['uuidRepresentation'] = 'standard'

    return resolved_settings


# override class method
flask_mongoengine2.connection._sanitize_settings = _sanitize_settings
