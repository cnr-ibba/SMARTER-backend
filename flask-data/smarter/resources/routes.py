#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:22:59 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from .breeds import BreedsApi


def initialize_routes(api):
    api.add_resource(BreedsApi, '/api/breeds')
