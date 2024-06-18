#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:40:09 2021

@author: Paolo Cozzi <bunop@libero.it>
"""

from bson import ObjectId
from bson.errors import InvalidId

from flask import jsonify, current_app
from flask_restful import Resource, reqparse

from database.models import SampleSheep, SampleGoat
from resources.errors import MongoEngineValidationError, ObjectsNotExistsError

geojson = {
    "$project": {
        "type": "Feature",
        "geometry": "$locations",
        "properties": {
            "original_id": "$original_id",
            "smarter_id": "$smarter_id",
            "country": "$country",
            "species": "$species",
            "breed": "$breed",
            "breed_code": "$breed_code",
            "dataset": "$dataset_id",
            "type": "$type",
            "chip_name": "$chip_name",
            "sex": "$sex",
            "metadata": "$metadata",
            "phenotype": "$phenotype"
        }
    }
}


class GeoJSONMixin():
    model = None

    def get(self, id_):
        try:
            sample = self.model.objects().aggregate([
                {"$match": {
                    "_id": ObjectId(id_),
                    "locations": {"$exists": True}
                }},
                geojson
            ])

        except InvalidId as exc:
            current_app.logger.error(exc)
            raise MongoEngineValidationError

        try:
            result = next(sample)

        except StopIteration as exc:
            current_app.logger.warning(exc)
            raise ObjectsNotExistsError

        return jsonify(result)


class GeoJSONListMixin(Resource):
    model = None

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
        'dataset',
        action='append',
        dest="dataset_id",
        help="The dataset id")
    parser.add_argument(
        'type',
        help="The sample type (background/foreground)")
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

    def parse_args(self) -> list:
        # reading request parameters
        kwargs = self.parser.parse_args(strict=True)
        args = []

        # filter args
        kwargs = {key: val for key, val in kwargs.items() if val}

        # mind to ObjectId object
        if 'dataset_id' in kwargs:
            kwargs['dataset_id'] = [
                ObjectId(id_) for id_ in kwargs['dataset_id']]

        if 'geo_within_polygon' in kwargs:
            # get the geometry field
            geometry = kwargs.pop('geo_within_polygon')['geometry']

            if 'locations' not in kwargs:
                kwargs['locations'] = {}

            # add a new key to kwargs dictionary
            kwargs['locations']['$geoWithin'] = {}
            kwargs['locations']['$geoWithin']["$geometry"] = geometry

        if 'geo_within_sphere' in kwargs:
            value = kwargs.pop('geo_within_sphere')

            # convert radius in radians (Km expected)
            value[-1] = value[-1] / 6378.1

            if 'locations' not in kwargs:
                kwargs['locations'] = {}

            # add a new key to kwargs dictionary
            kwargs['locations']['$geoWithin'] = {}
            kwargs['locations']['$geoWithin']["$centerSphere"] = value

        return args, kwargs

    def get_context_data(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        # mind to list arguments
        for key in [
                'breed', 'breed_code', 'chip_name', 'country', 'dataset_id']:
            if key in kwargs:
                values = kwargs[key]

                # change values
                kwargs[key] = {'$in': values}

        current_app.logger.debug(f"{args}, {kwargs}")

        matches = {"locations": {"$exists": True}}

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                matches[key] = value

        current_app.logger.debug(f"Got matches: '{matches}'")

        collection = self.model.objects().aggregate([
            {"$match": matches},
            geojson,
            {"$group": {
                "_id": None,
                "features": {
                    "$push": "$$ROOT"
                }
            }},
            {"$project": {
                "_id": 0,
                "type": "FeatureCollection",
                "features": "$features"
            }}
        ])

        try:
            result = next(collection)

        except StopIteration as exc:
            current_app.logger.debug(f"No results for {matches}: {exc}")
            result = {
                "type": "FeatureCollection",
                "features": []
            }

        return jsonify(result)


class SampleSheepGeoJSONApi(GeoJSONMixin, Resource):
    model = SampleSheep

    def get(self, id_):
        """
        Get a single GeoJSON for Sheep
        ---
        tags:
          - GeoJSON
        description: Query SMARTER data about samples
        parameters:
          - in: path
            name: id_
            type: string
            description: The sample ObjectID
            required: true
        responses:
            '200':
              description: GeoJSON Feature
              content:
                application/json:
                  schema:
                    type: object
        """
        return super().get(id_)


class SampleGoatGeoJSONApi(GeoJSONMixin, Resource):
    model = SampleGoat

    def get(self, id_):
        """
        Get a single GeoJSON for Goat
        ---
        tags:
          - GeoJSON
        description: Query SMARTER data about samples
        parameters:
          - in: path
            name: id_
            type: string
            description: The sample ObjectID
            required: true
        responses:
            '200':
              description: GeoJSON Feature
              content:
                application/json:
                  schema:
                    type: object
        """
        return super().get(id_)


class SampleSheepGeoJSONListApi(GeoJSONListMixin, Resource):
    model = SampleSheep

    def get(self):
        """
        Get a GeoJSON for Sheep samples
        ---
        tags:
          - GeoJSON
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
        responses:
            '200':
              description: GeoJSON FeatureCollection
              content:
                application/json:
                  schema:
                    type: object
        """

        return self.get_context_data()

    def post(self):
        """
        Get a GeoJSON for Sheep samples
        ---
        tags:
          - GeoJSON
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

        return self.get_context_data()


class SampleGoatGeoJSONListApi(GeoJSONListMixin, Resource):
    model = SampleGoat

    def get(self):
        """
        Get a GeoJSON for Goat samples
        ---
        tags:
          - GeoJSON
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
        responses:
            '200':
              description: GeoJSON FeatureCollection
              content:
                application/json:
                  schema:
                    type: object
        """

        return self.get_context_data()

    def post(self):
        """
        Get a GeoJSON for Sheep samples
        ---
        tags:
          - GeoJSON
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

        return self.get_context_data()
