#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:50:23 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os
import logging

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt

from database.db import initialize_db, DB_ALIAS
from resources.errors import errors
from resources.routes import initialize_routes
from commands import usersbp

# Get an instance of a logger
logger = logging.getLogger(__name__)


# https://stackoverflow.com/a/56474420/4385116
def create_app(config={}):
    """This function create Flask app. Is required by wsgi because it need to
    be called after service is started and forked, not when importing the
    module during initialization. To start the flask app, first import
    the module and then create all the stuff by invoking this function
    You need call the run method on the returned values to start acception
    requests

    Args:
        config (dict): pass parameters to this app (not yet defined)

    Returns:
        Flask: a flask initialized application
    """

    app = Flask(__name__)
    api = Api(app, errors=errors)
    Bcrypt(app)

    # http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/#configuration
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://mongo/smarter',
        'username': os.getenv("MONGODB_SMARTER_USER"),
        'password': os.getenv("MONGODB_SMARTER_PASS"),
        'authentication_source': 'admin',
        'alias': DB_ALIAS,
        # NOTE: This fixes "UserWarning: MongoClient opened before fork."
        # I'm not aware of side effects yet. Default value is/was "True"
        'connect': False
    }

    # override configuration with custom values
    if 'host' in config:
        logger.error(f"Setting custom host: {config['host']}")
        app.config['MONGODB_SETTINGS']['host'] = config['host']

    # connect to database
    initialize_db(app)

    # you MUST register the blueprint
    app.register_blueprint(usersbp)

    # add resources
    initialize_routes(api)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
