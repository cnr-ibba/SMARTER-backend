#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:04:11 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from database.models import SampleGoat, SampleSheep
from common.views import ListView


class SampleSheepApi(Resource):
    @jwt_required()
    def get(self, id_):
        sample = SampleSheep.objects(id=id_).get()
        return jsonify(sample)


class SampleSheepListApi(ListView):
    endpoint = 'samplesheeplistapi'
    model = SampleSheep

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()

        return jsonify(**data)


class SampleGoatApi(Resource):
    @jwt_required()
    def get(self, id_):
        sample = SampleGoat.objects(id=id_).get()
        return jsonify(sample)


class SampleGoatListApi(ListView):
    endpoint = 'samplegoatlistapi'
    model = SampleGoat

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()

        return jsonify(**data)
