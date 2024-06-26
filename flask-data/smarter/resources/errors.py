#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:15:08 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
    pass


class SchemaValidationError(HTTPException):
    pass


class MongoEngineValidationError(HTTPException):
    pass


class ObjectsNotExistsError(HTTPException):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "MongoEngineValidationError": {
        "message": ("This is not a valid ObjectId, it must be a 12-byte "
                    "input or a 24-character hex string"),
        "status": 400
    },
    "ObjectsNotExistsError": {
        "message": "Object does not exist",
        "status": 404
    }
}
