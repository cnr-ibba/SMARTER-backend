#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:10:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import re

from urllib.parse import unquote

from flask import jsonify, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from database.models import VariantGoat, VariantSheep
from common.views import ListView

location_pattern = re.compile(r'(?P<chrom>\w+):(?P<start>\d+)-(?P<end>\d+)')


class VariantListMixin():
    parser = reqparse.RequestParser()
    parser.add_argument('name', help="Variant name")
    parser.add_argument('rs_id', help="rsID identifier")
    parser.add_argument('chip_name', help="Chip name")
    parser.add_argument('probeset_id', help="Affymetrix probeset id")
    parser.add_argument('cust_id', help="Affymetrix cust_id (illumina name)")
    parser.add_argument(
        'imported_from', help="Data source type")
    parser.add_argument(
        'version', help="Genome version")
    parser.add_argument('region', help="Sequence location (ex 1:1-10000")

    def get_queryset(self):
        # reading request parameters
        args = self.parser.parse_args()

        # filter args
        args = {key: val for key, val in args.items() if val}

        # add the $elemMatch clause if necessary
        args = self.__prepare_match(args)

        current_app.logger.info(args)

        if args:
            queryset = self.model.objects.filter(**args)

        else:
            queryset = self.model.objects.all()

        return queryset

    def __prepare_match(self, args):
        """Transform the args RequestParser dictionary and add a $elemMatch
        clause"""

        if any(['imported_from' in args, 'version' in args, 'region' in args]):
            elemMatch = {}

            if 'imported_from' in args:
                elemMatch['imported_from'] = args.pop('imported_from')

            if 'version' in args:
                elemMatch['version'] = args.pop('version')

            if 'region' in args:
                match = re.search(
                    location_pattern,
                    unquote(args.pop('region'))
                )

                if match:
                    elemMatch['chrom'] = match.group("chrom")
                    elemMatch['position__gte'] = match.group("start")
                    elemMatch['position__lte'] = match.group("end")

            args['locations__match'] = elemMatch

        return args

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