#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:50:23 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os

from flask import Flask, Response
from flask_restful import Resource, Api

from database.db import initialize_db
from database.models import User


class HelloWorld(Resource):
    def get(self):
        users = User.objects.to_json()
        return Response(
            users,
            mimetype="application/json",
            status=200)


# https://stackoverflow.com/a/56474420/4385116
def create_app(config=None):
    app = Flask(__name__)
    api = Api(app)

    # http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/#configuration
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://mongo/smarter',
        'username': os.getenv("MONGODB_SMARTER_USER"),
        'password': os.getenv("MONGODB_SMARTER_PASS"),
        'authentication_source': 'admin',
        # NOTE: This fixes "UserWarning: MongoClient opened before fork."
        # I'm not aware of side effects yet. Default value is/was "True"
        'connect': False
    }

    # connect to database
    initialize_db(app)

    api.add_resource(HelloWorld, '/')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
