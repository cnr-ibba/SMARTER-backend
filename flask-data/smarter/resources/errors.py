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


class UnauthorizedError(HTTPException):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    # flask_jwt_extended.exceptions.NoAuthorizationError:
    "NoAuthorizationError": {
        "message": "Missing Authorization Header",
        "status": 401
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
}
