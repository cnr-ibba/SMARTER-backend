#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:16:46 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import json

from flask import Response, request, current_app
from flask_restful import Resource

from resources.errors import InternalServerError


class LoginApi(Resource):
    def post(self):
        """
        Old User authenticate method. Has been removed after public release.
        ---
        tags:
          - Authorization
        description: Return a message telling users to update their client

        responses:
          200:
            description: A standard message
        """
        try:
            # consume request body but don't do anything with it
            _ = request.get_json()

            response = Response(
                json.dumps({
                    "token": "Token has been removed after public release",
                    "message": (
                        "Please update your Smarter API client to the latest "
                        "version")
                }),
                mimetype="application/json",
                status=200)

            return response

        except Exception as e:
            current_app.logger.error(e)
            raise InternalServerError
