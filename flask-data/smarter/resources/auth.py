#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:16:46 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import datetime

from flask import Response, request, current_app
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mongoengine.errors import DoesNotExist

from database.models import User
from resources.errors import (
    UnauthorizedError, InternalServerError, SchemaValidationError)


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

            current_app.logger.info(f"New token generated for '{username}'")

            return Response(
                json.dumps({
                    'token': access_token,
                }),
                mimetype="application/json",
                status=200)

        except (UnauthorizedError, DoesNotExist) as e:
            current_app.logger.error(e)
            raise UnauthorizedError

        except SchemaValidationError as e:
            current_app.logger.error(e)
            raise SchemaValidationError

        except Exception as e:
            current_app.logger.error(e)
            raise InternalServerError
