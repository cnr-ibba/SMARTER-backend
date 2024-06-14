#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:50:23 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import os

from bson import ObjectId
from json import JSONEncoder
from logging.config import dictConfig

from flask import Flask, redirect, url_for
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

from database.db import initialize_db, DB_ALIAS
from resources.errors import errors
from resources.routes import initialize_routes
from commands import usersbp

__version__ = "0.3.0.dev0"

# https://flask.palletsprojects.com/en/2.0.x/logging/#basic-configuration
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return {
                "$oid": str(obj)
            }
        return JSONEncoder.default(self, obj)


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
    CORS(app)
    api = Api(app, errors=errors)
    Bcrypt(app)
    JWTManager(app)

    # deal with ObjectId in json responses
    app.json_encoder = CustomJSONEncoder

    # workaround to make flasgger deal with jwt-token headers
    app.config["JWT_AUTH_URL_RULE"] = True

    # Swagger stuff
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SMARTER-backend API",
            "description": "REST API for SMARTER data",
            "termsOfService": None,
            "version": __version__
        },
        "basePath": "/smarter-api/",  # base bash for blueprint registration
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": '/smarter-api/apispec_1',
                "route": '/smarter-api/apispec_1.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
        "static_url_path": "/smarter-api/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/smarter-api/docs/"
    }

    Swagger(app, template=swagger_template, config=swagger_config)

    app.logger.debug("App initialized")

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
        app.logger.error(f"Setting custom host: {config['host']}")
        app.config['MONGODB_SETTINGS']['host'] = config['host']

    # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

    # connect to database
    initialize_db(app)

    app.logger.debug("Database initialized")
    app.logger.debug(f"Got encoder {app.json_encoder}")

    # you MUST register the blueprint
    app.register_blueprint(usersbp)

    # add resources
    initialize_routes(api)

    app.logger.debug("Routes initialized")

    # add a redirect for the index page
    @app.route('/smarter-api/')
    def index():
        return redirect(url_for('flasgger.apidocs'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
