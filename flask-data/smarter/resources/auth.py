#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:16:46 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json
import datetime

from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from mongoengine.errors import DoesNotExist

from database.models import User
from resources.errors import UnauthorizedError, InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(username=body.get('username'))

            # calling custom user function (which uses bcrypt)
            authorized = user.check_password(body.get('password'))

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

        except Exception:
            raise InternalServerError
