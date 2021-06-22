#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:10:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from database.models import VariantGoat, VariantSheep
from common.views import ListView


class VariantListMixin():
    parser = reqparse.RequestParser()
    parser.add_argument('name', help="Variant name")
    parser.add_argument('rs_id', help="rsID identifier")
    parser.add_argument('chip_name', help="Chip name")
    parser.add_argument('probeset_id', help="Affymetrix probeset id")

    def get_queryset(self):
        # reading request parameters
        args = self.parser.parse_args()

        # filter args
        args = {key: val for key, val in args.items() if val}

        current_app.logger.debug(args)

        if args:
            queryset = self.model.objects.filter(**args)

        else:
            queryset = self.model.objects.all()

        return queryset

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class VariantSheepApi(Resource):
    @jwt_required()
    def get(self, id_):
        variant = VariantSheep.objects(id=id_).get()
        return jsonify(variant)


class VariantSheepListApi(VariantListMixin, ListView):
    endpoint = 'variantsheeplistapi'
    model = VariantSheep


class VariantGoatApi(Resource):
    @jwt_required()
    def get(self, id_):
        variant = VariantGoat.objects(id=id_).get()
        return jsonify(variant)


class VariantGoatListApi(VariantListMixin, ListView):
    endpoint = 'variantgoatlistapi'
    model = VariantGoat
