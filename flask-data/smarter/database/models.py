#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:09:30 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from .db import db


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
