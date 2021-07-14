#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:16:39 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import re
import json

from mongoengine.queryset import Q
from flask import jsonify, current_app, request
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_csv import send_csv

from database.models import Breed
from common.views import ListView, ModelView


class BreedListApi(ListView):
    endpoint = 'breedlistapi'
    model = Breed

    parser = reqparse.RequestParser()
    parser.add_argument('species', help="Species name")
    parser.add_argument('name', help="Breed name")
    parser.add_argument('code', help="Breed code name")
    parser.add_argument(
        'search', help="Search breed name and aliases by pattern")
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

        # deal with search fields
        if 'search' in kwargs:
            pattern = kwargs.pop("search")
            pattern = re.compile(pattern, re.IGNORECASE)
            args = [Q(name=pattern) | Q(aliases__fid=pattern)]

            # remove name from args if exists (i'm searching against it)
            if 'name' in kwargs:
                del(kwargs['name'])

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
        content_type = request.headers.get("Accept")
        self.object_list = self.get_queryset()

        if content_type == 'text/csv':
            return send_csv(
                [breed.to_dict() for breed in self.object_list],
                "test.csv",
                ["name", "species", "code", "n_individuals"])

        else:
            data = self.get_context_data()
            return jsonify(**data)


class BreedApi(ModelView):
    model = Breed

    @jwt_required()
    def get(self, id_):
        breed = self.get_object(id_)
        return jsonify(breed)
