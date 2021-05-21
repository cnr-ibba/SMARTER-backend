#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:09:08 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask_mongoengine import MongoEngine

db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
