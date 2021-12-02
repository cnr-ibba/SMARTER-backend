#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:04:11 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, current_app
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from database.models import SampleGoat, SampleSheep
from common.views import ListView, ModelView


class SampleMixin():
    @jwt_required()
    def get(self, id_):
        sample = self.get_object(id_)
        return jsonify(sample)


class SampleListMixin():
    parser = reqparse.RequestParser()
    parser.add_argument('breed', help="Breed name")
    parser.add_argument('breed_code', help="Breed code name")
    parser.add_argument('chip_name', help="Chip name")
    parser.add_argument('country', help="Country name")
    parser.add_argument(
        'original_id', help="Sample name in original data source")
    parser.add_argument('smarter_id', help="Smarter id")
    parser.add_argument('dataset', help="The dataset id")
    parser.add_argument(
        'type',
        dest="type_",
        help="The sample type (background/foreground)")
    parser.add_argument(
        'locations__exists',
        help="Get data with GPS coordinates",
        type=bool)
    parser.add_argument(
        'phenotype__exists',
        help="Get data with phenotype",
        type=bool)

    def get_queryset(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        return queryset

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class SampleSheepApi(SampleMixin, ModelView):
    model = SampleSheep


class SampleSheepListApi(SampleListMixin, ListView):
    endpoint = 'samplesheeplistapi'
    model = SampleSheep


class SampleGoatApi(SampleMixin, ModelView):
    model = SampleGoat


class SampleGoatListApi(SampleListMixin, ListView):
    endpoint = 'samplegoatlistapi'
    model = SampleGoat
