#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:16:46 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import logging
import datetime

from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mongoengine.errors import DoesNotExist

from database.models import User
from resources.errors import (
    UnauthorizedError, InternalServerError, SchemaValidationError)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()

            username = body.get('username')
            password = body.get('password')

            # TODO: use a flask_restful method
            if not username or not password:
                raise SchemaValidationError

            user = User.objects.get(username=username)

            # calling custom user function (which uses bcrypt)
            authorized = user.check_password(password)

            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)

            access_token = create_access_token(
                identity=str(user.id),
                expires_delta=expires)

            return Response(
                json.dumps({
                    'token': access_token,
                }),
                mimetype="application/json",
                status=200)

        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError

        except SchemaValidationError:
            raise SchemaValidationError

        except Exception as e:
            logger.error(e)
            raise InternalServerError
