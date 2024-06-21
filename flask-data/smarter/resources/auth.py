#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:16:46 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import datetime

from flask import Response, request, current_app
from flask_jwt_extended import create_access_token, decode_token
from flask_restx import Resource
from mongoengine.errors import DoesNotExist

from database.models import User
from resources.errors import (
    UnauthorizedError, InternalServerError, SchemaValidationError)


class LoginApi(Resource):
    def post(self):
        """
        User authenticate method.
        ---
        tags:
          - Authorization
        description: Authenticate user with supplied credentials.
        parameters:
          - in: body
            name: body
            description: JSON parameters.
            schema:
              required:
              - username
              - password
              properties:
                username:
                  type: string
                  description: Your username
                password:
                  type: string
                  description: Your password
        responses:
          200:
            description: User successfully logged in.
          401:
            description: User login failed.
        """
        try:
            body = request.get_json()

            username = body.get('username')
            password = body.get('password')

            # TODO: use a flask_restx method
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

            # read token data
            claims = decode_token(access_token)

            current_app.logger.info(f"New token generated for '{username}'")

            response = Response(
                json.dumps({
                    'token': access_token,
                    'expires': str(
                        datetime.datetime.fromtimestamp(claims['exp']))
                }),
                mimetype="application/json",
                status=200)

            # add token to response headers - so SwaggerUI can use it
            response.headers.extend({'jwt-token': access_token})

            return response

        except (UnauthorizedError, DoesNotExist) as e:
            current_app.logger.error(e)
            raise UnauthorizedError

        except SchemaValidationError as e:
            current_app.logger.error(e)
            raise SchemaValidationError

        except Exception as e:
            current_app.logger.error(e)
            raise InternalServerError
