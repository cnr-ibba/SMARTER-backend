#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:50:50 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from database.models import Dataset
from common.views import ListView


class DatasetsApi(ListView):
    endpoint = 'datasetsapi'
    model = Dataset

    def get_queryset(self):
        # read additional arguments from URL
        species = request.args.get('species')

        # get queryset from base class
        qs = super().get_queryset()

        if species:
            qs = qs.filter(species=species)

        return qs

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()

        return jsonify(**data)


class DatasetApi(Resource):
    @jwt_required()
    def get(self, id_):
        dataset = Dataset.objects(id=id_).get()
        return jsonify(dataset)
