#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:10:51 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

import re

from urllib.parse import unquote

from flask import jsonify, current_app
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from database.models import VariantGoat, VariantSheep, SmarterInfo
from common.views import ListView, ModelView

location_pattern = re.compile(r'(?P<chrom>\w+):(?P<start>\d+)-(?P<end>\d+)')


class VariantMixin():
    @jwt_required()
    def get(self, id_):
        variant = self.get_object(id_)
        return jsonify(variant)


class VariantListMixin():
    assembly = None
    coordinate_system = {}

    parser = reqparse.RequestParser()
    parser.add_argument('name', help="Variant name")
    parser.add_argument('rs_id', help="rsID identifier")
    parser.add_argument(
        'chip_name',
        action='append',
        help="Chip name")
    parser.add_argument('probeset_id', help="Affymetrix probeset id")
    parser.add_argument('cust_id', help="Affymetrix cust_id (illumina name)")
    parser.add_argument('region', help="Sequence location (ex 1:1-10000")

    def __init__(self) -> None:
        super().__init__()

        # get supported assemblies from database
        info = SmarterInfo.objects.get(pk="smarter")
        working_assemblies = info["working_assemblies"]
        self.coordinate_system = {
            'version': working_assemblies[self.assembly][0],
            'imported_from': working_assemblies[self.assembly][1]
        }

    def get_queryset(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        # mind to the multiple arguments
        if 'chip_name' in kwargs:
            chip_name = kwargs.pop('chip_name')

            # add a new key to kwargs dictionary
            kwargs['chip_name__all'] = chip_name

        # add the $elemMatch clause if necessary
        kwargs = self.__prepare_match(kwargs)

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        # limit to certain fields
        return queryset.fields(
            elemMatch__locations=self.coordinate_system.copy(),
            name=1,
            rs_id=1,
            chip_name=1,
            probeset_id=1,
            sequence=1,
            cust_id=1
        )

    def __prepare_match(self, kwargs):
        """Transform the kwargs RequestParser dictionary and add a $elemMatch
        clause"""

        elemMatch = self.coordinate_system.copy()

        if 'region' in kwargs:
            match = re.search(
                location_pattern,
                unquote(kwargs.pop('region'))
            )

            if match:
                elemMatch['chrom'] = match.group("chrom")
                elemMatch['position__gte'] = match.group("start")
                elemMatch['position__lte'] = match.group("end")

        kwargs['locations__match'] = elemMatch

        return kwargs

    @jwt_required()
    def get(self):
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class VariantSheepApi(VariantMixin, ModelView):
    model = VariantSheep


class VariantSheepOAR3Api(VariantListMixin, ListView):
    endpoint = 'variantsheepoar3api'
    model = VariantSheep
    assembly = "OAR3"


class VariantSheepOAR4Api(VariantListMixin, ListView):
    endpoint = 'variantsheepoar4api'
    model = VariantSheep
    assembly = "OAR4"


class VariantGoatApi(VariantMixin, ModelView):
    model = VariantGoat


class VariantGoatListApi(VariantListMixin, ListView):
    endpoint = 'variantgoatlistapi'
    model = VariantGoat


class VariantGoatCHI1Api(VariantListMixin, ListView):
    endpoint = 'variantgoatchi1api'
    model = VariantGoat
    assembly = "CHI1"


class VariantGoatARS1Api(VariantListMixin, ListView):
    endpoint = 'variantgoatars1api'
    model = VariantGoat
    assembly = "ARS1"
