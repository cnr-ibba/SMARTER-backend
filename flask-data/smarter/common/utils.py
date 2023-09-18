#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:17:28 2023

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import six

from flask import current_app
from flask_restful.reqparse import Argument, Namespace, RequestParser
from werkzeug.datastructures import MultiDict


# werkzeug has changed how to reply to non-json requests
# https://github.com/flask-restful/flask-restful/issues/936
class CustomArgument(Argument):
    def source(self, request):
        """Pulls values off the request in the provided location
        :param request: The flask request object to parse arguments from
        """
        if isinstance(self.location, six.string_types):
            value = getattr(request, self.location, MultiDict())
            if callable(value):
                value = value()
            if value is not None:
                return value
        else:
            values = MultiDict()
            for location in self.location:
                if not request.is_json and location == 'json':
                    current_app.logger.error(f"Skipping location: {location}")
                    continue

                value = getattr(request, location, None)
                if callable(value):
                    value = value()
                if value is not None:
                    values.update(value)
            return values

        return MultiDict()


class CustomRequestParser(RequestParser):
    def __init__(
            self, argument_class=CustomArgument, namespace_class=Namespace,
            trim=False, bundle_errors=False):

        self.args = []
        self.argument_class = argument_class
        self.namespace_class = namespace_class
        self.trim = trim
        self.bundle_errors = bundle_errors
