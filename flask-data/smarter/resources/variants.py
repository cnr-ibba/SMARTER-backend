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


class VariantListMixin():
    assembly = None
    coordinate_system = {}

    def check_region(value):
        if not re.search(location_pattern, unquote(value)):
            raise ValueError(
                f"The value '{value}' is is not a valid region, "
                f"it must be <chrom>:<start>-<end>"
            )

        return value

    parser = reqparse.RequestParser()
    parser.add_argument('name', help="Variant name")
    parser.add_argument('rs_id', help="rsID identifier")
    parser.add_argument(
        'chip_name',
        action='append',
        help="Chip name")
    parser.add_argument('probeset_id', help="Affymetrix probeset id")
    parser.add_argument('cust_id', help="Affymetrix cust_id (illumina name)")
    parser.add_argument(
        'region',
        help="Sequence location (ex 1:1-10000): {error_msg}",
        type=check_region)

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

        if 'probeset_id' in kwargs:
            probeset_id = kwargs.pop('probeset_id')
            kwargs['probesets__probeset_id'] = probeset_id

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
            probesets=1,
            affy_snp_id=1,
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


class VariantSheepApi(ModelView):
    model = VariantSheep

    @jwt_required()
    def get(self, id_):
        """
        Fetch a single Sheep SNP
        ---
        tags:
          - Variants
        description: Fetch a single Sheep SNP using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The SNP ObjectID
            required: true
        responses:
            '200':
              description: The desidered SNP
              content:
                application/json:
                  schema:
                    type: object
        """
        variant = self.get_object(id_)
        return jsonify(variant)


class VariantSheepOAR3Api(VariantListMixin, ListView):
    endpoint = 'variantsheepoar3api'
    model = VariantSheep
    assembly = "OAR3"

    @jwt_required()
    def get(self):
        """
        Get SNPs on Sheep OAR3 Assembly
        ---
        tags:
          - Variants
        description: Query SMARTER data on Sheep OAR3 Assembly
        parameters:
          - name: name
            in: query
            type: string
            description: The SNP name
          - name: rs_id
            in: query
            type: string
            description: The SNP rsID identifier
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: probeset_id
            in: query
            type: string
            description: Affymetrix probeset id
          - name: cust_id
            in: query
            type: string
            description: Affymetrix cust_id (illumina name)
          - name: region
            in: query
            type: string
            description: Filter SNPs by position (chrom:start-end)
        responses:
            '200':
              description: Datasets to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class VariantSheepOAR4Api(VariantListMixin, ListView):
    endpoint = 'variantsheepoar4api'
    model = VariantSheep
    assembly = "OAR4"

    @jwt_required()
    def get(self):
        """
        Get SNPs on Sheep OAR4 Assembly
        ---
        tags:
          - Variants
        description: Query SMARTER data on Sheep OAR4 Assembly
        parameters:
          - name: name
            in: query
            type: string
            description: The SNP name
          - name: rs_id
            in: query
            type: string
            description: The SNP rsID identifier
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: probeset_id
            in: query
            type: string
            description: Affymetrix probeset id
          - name: cust_id
            in: query
            type: string
            description: Affymetrix cust_id (illumina name)
          - name: region
            in: query
            type: string
            description: Filter SNPs by position (chrom:start-end)
        responses:
            '200':
              description: Datasets to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class VariantGoatApi(ModelView):
    model = VariantGoat

    @jwt_required()
    def get(self, id_):
        """
        Fetch a single Goat SNP
        ---
        tags:
          - Variants
        description: Fetch a single Goat SNP using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The SNP ObjectID
            required: true
        responses:
            '200':
              description: The desidered SNP
              content:
                application/json:
                  schema:
                    type: object
        """
        variant = self.get_object(id_)
        return jsonify(variant)


class VariantGoatCHI1Api(VariantListMixin, ListView):
    endpoint = 'variantgoatchi1api'
    model = VariantGoat
    assembly = "CHI1"

    @jwt_required()
    def get(self):
        """
        Get SNPs on Goat CHI1 Assembly
        ---
        tags:
          - Variants
        description: Query SMARTER data on Goat CHI1 Assembly
        parameters:
          - name: name
            in: query
            type: string
            description: The SNP name
          - name: rs_id
            in: query
            type: string
            description: The SNP rsID identifier
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: probeset_id
            in: query
            type: string
            description: Affymetrix probeset id
          - name: cust_id
            in: query
            type: string
            description: Affymetrix cust_id (illumina name)
          - name: region
            in: query
            type: string
            description: Filter SNPs by position (chrom:start-end)
        responses:
            '200':
              description: Datasets to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class VariantGoatARS1Api(VariantListMixin, ListView):
    endpoint = 'variantgoatars1api'
    model = VariantGoat
    assembly = "ARS1"

    @jwt_required()
    def get(self):
        """
        Get SNPs on Goat ARS1 Assembly
        ---
        tags:
          - Variants
        description: Query SMARTER data on Goat ARS1 Assembly
        parameters:
          - name: name
            in: query
            type: string
            description: The SNP name
          - name: rs_id
            in: query
            type: string
            description: The SNP rsID identifier
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: probeset_id
            in: query
            type: string
            description: Affymetrix probeset id
          - name: cust_id
            in: query
            type: string
            description: Affymetrix cust_id (illumina name)
          - name: region
            in: query
            type: string
            description: Filter SNPs by position (chrom:start-end)
        responses:
            '200':
              description: Datasets to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)
