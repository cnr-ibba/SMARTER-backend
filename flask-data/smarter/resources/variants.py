#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:10:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from database.models import VariantGoat, VariantSheep
from common.views import ListView


class VariantSheepApi(Resource):
    @jwt_required()
    def get(self, id_):
        variant = VariantSheep.objects(id=id_).get()
        return jsonify(variant)


class VariantSheepListApi(ListView):
    endpoint = 'variantsheeplistapi'
    model = VariantSheep

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()

        return jsonify(**data)


class VariantGoatApi(Resource):
    @jwt_required()
    def get(self, id_):
        variant = VariantGoat.objects(id=id_).get()
        return jsonify(variant)


class VariantGoatListApi(ListView):
    endpoint = 'variantgoatlistapi'
    model = VariantGoat

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()

        return jsonify(**data)
