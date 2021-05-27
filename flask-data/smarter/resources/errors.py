#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:15:08 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""


class InternalServerError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
}
