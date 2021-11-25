#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:50:50 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import re

from mongoengine.queryset import Q
from flask import jsonify, current_app
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from database.models import Dataset
from common.views import ListView, ModelView


class DatasetListApi(ListView):
    endpoint = 'datasetlistapi'
    model = Dataset

    parser = reqparse.RequestParser()
    parser.add_argument('species', help="Species name")
    parser.add_argument(
        'type',
        dest="type_",
        action='append',
        help="Dataset type")
    parser.add_argument(
        'search', help="Search by dataset contents")
    parser.add_argument('sort', help="Sort results by this key")
    parser.add_argument('order', help="Sort key order")

    def get_queryset(self):
        # reading request parameters
        kwargs = self.parser.parse_args()
        args = []

        # filter args
        kwargs = {key: val for key, val in kwargs.items() if val}

        # deal with ordering stuff
        # HINT should this be placed in a mixin?
        sort = None

        if 'sort' in kwargs:
            sort = kwargs.pop('sort')

        if 'order' in kwargs:
            order = kwargs.pop('order')

            if sort and order == 'desc':
                sort = f"-{sort}"

        # mind to the _type arguments
        if 'type_' in kwargs:
            type_ = kwargs.pop('type_')

            # add a new key to kwargs dictionary
            kwargs['type___all'] = type_

        # deal with search fields
        if 'search' in kwargs:
            pattern = kwargs.pop("search")
            pattern = re.compile(pattern, re.IGNORECASE)
            args = [Q(file=pattern) | Q(contents=pattern)]

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class DatasetApi(ModelView):
    model = Dataset

    @jwt_required()
    def get(self, id_):
        dataset = self.get_object(id_)
        return jsonify(dataset)
