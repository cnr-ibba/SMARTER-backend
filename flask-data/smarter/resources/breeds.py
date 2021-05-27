#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:16:39 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from database.models import Breed
from common.views import ListView


class BreedsApi(ListView):
    endpoint = 'breedsapi'
    model = Breed

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


class BreedApi(Resource):
    @jwt_required()
    def get(self, id_):
        breed = Breed.objects(id=id_).get()
        return jsonify(breed)
