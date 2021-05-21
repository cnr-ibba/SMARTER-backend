#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:50:23 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


if __name__ == '__main__':
    app.run(debug=True)
