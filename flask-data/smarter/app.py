#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:50:23 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from bson import ObjectId
import logging
from logging.config import dictConfig
from logging.handlers import SMTPHandler

from decouple import config
from flask import Flask, redirect, url_for, has_request_context, request
from flask.logging import default_handler
from flask_restful import Api
from flask.json import JSONEncoder
from flask_cors import CORS
from flasgger import Swagger

from database.db import initialize_db, DB_ALIAS
from resources.errors import errors
from resources.routes import initialize_routes

__version__ = "0.3.0"

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

mail_handler = SMTPHandler(
    mailhost=(
        config('EMAIL_HOST', default='localhost'),
        config('EMAIL_PORT', cast=int, default=1025)
    ),
    fromaddr=config('DEFAULT_FROM_EMAIL', default="server-error@example.com"),
    toaddrs=[email.strip() for email in config(
        'ADMINS', default="admin@example.com").split(',')],
    subject='SMARTER-backend Application Error',
    credentials=(
        config('EMAIL_HOST_USER', default=None),
        config('EMAIL_HOST_PASSWORD', default=None)
    ),
    secure=()
)
mail_handler.setLevel(logging.ERROR)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
mail_handler.setFormatter(formatter)
default_handler.setFormatter(formatter)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return {
                "$oid": str(obj)
            }
        return JSONEncoder.default(self, obj)


# https://stackoverflow.com/a/56474420/4385116
def create_app():
    """This function create Flask app. Is required by wsgi because it need to
    be called after service is started and forked, not when importing the
    module during initialization. To start the flask app, first import
    the module and then create all the stuff by invoking this function
    You need call the run method on the returned values to start accepting
    requests

    Returns:
        Flask: a flask initialized application
    """

    app = Flask(__name__)
    CORS(app)
    api = Api(app, errors=errors)

    # check debug mode
    if config('DEBUG', cast=bool, default=True):
        # in debug mode, the default logging will be set to DEBUG level
        app.debug = True

    # deal with ObjectId in json responses
    app.json_encoder = CustomJSONEncoder

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
        'host': config(
            'MONGODB_SMARTER_DB',
            default='mongodb://mongo/smarter'
        ),
        'username': config('MONGODB_SMARTER_USER'),
        'password': config("MONGODB_SMARTER_PASS"),
        'authentication_source': 'admin',
        'alias': DB_ALIAS,
        # NOTE: This fixes "UserWarning: MongoClient opened before fork."
        # I'm not aware of side effects yet. Default value is/was "True"
        'connect': False
    }

    # connect to database
    initialize_db(app)

    app.logger.debug("Database initialized")
    app.logger.debug(f"Got encoder {app.json_encoder}")

    # add resources
    initialize_routes(api)

    app.logger.debug("Routes initialized")

    if not app.debug:
        app.logger.addHandler(mail_handler)

    # add a redirect for the index page
    @app.route('/smarter-api/')
    def index():
        return redirect(url_for('flasgger.apidocs'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
