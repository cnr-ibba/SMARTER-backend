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

__version__ = "0.3.1"

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


class LoggingSMTPHandler(SMTPHandler):
    """Custom SMTP handler that logs when emails are sent"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def emit(self, record):
        """
        Emit a record and log the email sending action.
        If using localhost, simulate email by logging the content.
        """
        # Check if we're using localhost (development mode)
        is_localhost = (
            isinstance(self.mailhost, tuple) and
            self.mailhost[0] == 'localhost'
        ) or self.mailhost == 'localhost'

        if is_localhost:
            # Simulate email by logging the full content
            msg = self.format(record)
            self.logger.warning(
                f"\n{'='*60}\n"
                f"SIMULATED EMAIL (localhost mode)\n"
                f"{'='*60}\n"
                f"From: {self.fromaddr}\n"
                f"To: {', '.join(self.toaddrs)}\n"
                f"Subject: {self.getSubject(record)}\n"
                f"{'-'*60}\n"
                f"{msg}\n"
                f"{'='*60}\n"
            )
        else:
            # Real SMTP server configured
            try:
                self.logger.info(
                    f"Sending error email to {', '.join(self.toaddrs)} "
                    f"for {record.levelname}: {record.getMessage()[:100]}"
                )
                super().emit(record)
                self.logger.info("Error email sent successfully")
            except Exception as e:
                self.logger.error(f"Failed to send error email: {e}")
                self.handleError(record)


mail_handler = LoggingSMTPHandler(
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
    if config('DEBUG', cast=bool, default=False):
        # in debug mode, the default logging will be set to DEBUG level
        app.debug = True

    # deal with ObjectId in json responses
    app.json_encoder = CustomJSONEncoder

    # Swagger stuff
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SMARTER-backend API",
            "description": (
                "REST API service to interact and access SMARTER data. "
                "Provides methods to retrieve information on breeds, samples, "
                "variants, datasets and countries for Sheep and Goat species. "
                "Data is returned in JSON format and can be filtered using "
                "various query parameters. This is the same API used by the "
                "SMARTER-frontend web application."
            ),
            "termsOfService": None,
            "version": __version__
        },
        "externalDocs": {
            "description": "Full API Documentation",
            "url": "https://smarter-backend.readthedocs.io/en/latest/"
        },
        "basePath": "/smarter-api/",  # base path for blueprint registration
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
