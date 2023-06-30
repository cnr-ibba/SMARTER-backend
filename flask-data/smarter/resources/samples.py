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


class SampleListMixin():
    species = None

    parser = reqparse.RequestParser()
    parser.add_argument(
        'breed',
        action='append',
        help="Breed name")
    parser.add_argument(
        'breed_code',
        action='append',
        help="Breed code name")
    parser.add_argument(
        'chip_name',
        action='append',
        help="Chip name")
    parser.add_argument(
        'country',
        action='append',
        help="Country name")
    parser.add_argument(
        'original_id',
        help="Sample name in original data source")
    parser.add_argument(
        'alias',
        help="The sample alias in source dataset")
    parser.add_argument(
        'smarter_id',
        help="The smarter sample ID")
    parser.add_argument(
        'dataset',
        action='append',
        help="The dataset id")
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
    parser.add_argument(
      'geo_within_polygon',
      help="Filter Samples inside a polygon",
      type=dict,
      location='json'
    )
    parser.add_argument(
      'geo_within_sphere',
      help="Filter Samples inside a 2dshpere (center, radius in Km)",
      type=list,
      location='json'
    )

    def get_queryset(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        # mind to list arguments
        for key in ['breed', 'breed_code', 'chip_name', 'country', 'dataset']:
            if key in kwargs:
                value = kwargs.pop(key)

                # add a new key to kwargs dictionary
                kwargs[f'{key}__in'] = value

        if 'geo_within_polygon' in kwargs:
            # get the geometry field
            geometry = kwargs.pop('geo_within_polygon')['geometry']

            # add a new key to kwargs dictionary
            kwargs['locations__geo_within'] = geometry

        if 'geo_within_sphere' in kwargs:
            value = kwargs.pop('geo_within_sphere')

            # convert radius in radians (Km expected)
            value[-1] = value[-1] / 6378.1

            # add a new key to kwargs dictionary
            kwargs['locations__geo_within_sphere'] = value

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        return queryset


class SampleSheepApi(ModelView):
    model = SampleSheep

    @jwt_required()
    def get(self, id_):
        """
        Fetch a single Sheep sample
        ---
        tags:
          - Samples
        description: Fetch a single Sheep sample using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The sample ObjectID
            required: true
        responses:
            '200':
              description: The desidered sample
              content:
                application/json:
                  schema:
                    type: object
        """
        sample = self.get_object(id_)
        return jsonify(sample)


class SampleSheepListApi(SampleListMixin, ListView):
    endpoint = 'samplesheeplistapi'
    model = SampleSheep

    @jwt_required()
    def get(self):
        """
        Get samples information for Sheep
        ---
        tags:
          - Samples
        description: Query SMARTER data about samples
        parameters:
          - name: breed
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Breed name
          - name: breed_code
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Breed code
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: country
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Country where sample was collected
          - name: original_id
            in: query
            type: string
            description: The original sample name in source dataset
          - name: alias
            in: query
            type: string
            description: The sample alias in source dataset
          - name: smarter_id
            in: query
            type: string
            description: The smarter sample ID
          - name: dataset
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: The dataset ObjectID
          - name: type
            in: query
            type: string
            enum: ['foreground', 'background']
            description: Dataset type
          - name: locations__exists
            in: query
            type: bool
            description: Filter samples with a physical location
              (GPS coordinates)
          - name: phenotype__exists
            in: query
            type: bool
            description: Filter samples with a phenotype (any)
        responses:
            '200':
              description: Samples to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)

    @jwt_required()
    def post(self):
        """
        Get samples information for Sheep
        ---
        tags:
          - Samples
        description: Query SMARTER data about samples
        parameters:
          - in: body
            name: body
            description: Execute a gis query
            schema:
              properties:
                geo_within_polygon:
                  type: object
                  description: A Polygon feature
                  properties:
                    type:
                      type: string
                    properties:
                      type: object
                    geometry:
                      type: object
                geo_within_sphere:
                  type: array
                  description: A list with coordinates and radius in Km
        responses:
            '200':
              description: Samples to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class SampleGoatApi(ModelView):
    model = SampleGoat

    @jwt_required()
    def get(self, id_):
        """
        Fetch a single Goat sample
        ---
        tags:
          - Samples
        description: Fetch a single Goat sample using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The sample ObjectID
            required: true
        responses:
            '200':
              description: The desidered sample
              content:
                application/json:
                  schema:
                    type: object
        """
        sample = self.get_object(id_)
        return jsonify(sample)


class SampleGoatListApi(SampleListMixin, ListView):
    endpoint = 'samplegoatlistapi'
    model = SampleGoat

    @jwt_required()
    def get(self):
        """
        Get samples information for Goat
        ---
        tags:
          - Samples
        description: Query SMARTER data about samples
        parameters:
          - name: breed
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Breed name
          - name: breed_code
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Breed code
          - name: chip_name
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Chip name
          - name: country
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: Country where sample was collected
          - name: original_id
            in: query
            type: string
            description: The original sample name in source dataset
          - name: alias
            in: query
            type: string
            description: The sample alias in source dataset
          - name: smarter_id
            in: query
            type: string
            description: The smarter sample ID
          - name: dataset
            in: query
            type: array
            items:
              type: string
            collectionFormat: multi
            description: The dataset ObjectID
          - name: type
            in: query
            type: string
            enum: ['foreground', 'background']
            description: Dataset type
          - name: locations__exists
            in: query
            type: bool
            description: Filter samples with a physical location
              (GPS coordinates)
          - name: phenotype__exists
            in: query
            type: bool
            description: Filter samples with a phenotype (any)
        responses:
            '200':
              description: Samples to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)

    @jwt_required()
    def post(self):
        """
        Get samples information for Goat
        ---
        tags:
          - Samples
        description: Query SMARTER data about samples
        parameters:
          - in: body
            name: body
            description: Execute a gis query
            schema:
              properties:
                geo_within_polygon:
                  type: object
                  description: A Polygon feature
                  properties:
                    type:
                      type: string
                    properties:
                      type: object
                    geometry:
                      type: object
                geo_within_sphere:
                  type: array
                  description: A list with coordinates and radius in Km
        responses:
            '200':
              description: Samples to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)
