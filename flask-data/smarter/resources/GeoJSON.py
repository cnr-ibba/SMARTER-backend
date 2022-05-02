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
from flask_jwt_extended import jwt_required

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
        'country',
        help="Country name")
    parser.add_argument(
        'breed',
        help="Breed name")
    parser.add_argument(
        'breed_code',
        help="Breed code name")
    parser.add_argument(
        'chip_name',
        help="Chip name")
    parser.add_argument(
        'dataset',
        dest="dataset_id",
        help="The dataset id")
    parser.add_argument(
        'type',
        help="The sample type (background/foreground)")

    def parse_args(self) -> list:
        # reading request parameters
        kwargs = self.parser.parse_args(strict=True)
        args = []

        # filter args
        kwargs = {key: val for key, val in kwargs.items() if val}

        # mind to ObjectId object
        if 'dataset_id' in kwargs:
            kwargs['dataset_id'] = ObjectId(kwargs['dataset_id'])

        return args, kwargs

    def get(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        current_app.logger.debug(f"{args}, {kwargs}")

        matches = {"locations": {"$exists": True}}

        if len(kwargs) > 0:
            for key, value in kwargs.items():
                matches[key] = value

        current_app.logger.warning(f"Got matches: '{matches}'")

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

    @jwt_required()
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

    @jwt_required()
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

    @jwt_required()
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
            type: string
            description: Breed name
          - name: breed_code
            in: query
            type: string
            description: Breed code
          - name: chip_name
            in: query
            type: string
            description: Chip name
          - name: country
            in: query
            type: string
            description: Country where sample was collected
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

        return super().get()


class SampleGoatGeoJSONListApi(GeoJSONListMixin, Resource):
    model = SampleGoat

    @jwt_required()
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
            type: string
            description: Breed name
          - name: breed_code
            in: query
            type: string
            description: Breed code
          - name: chip_name
            in: query
            type: string
            description: Chip name
          - name: country
            in: query
            type: string
            description: Country where sample was collected
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
        return super().get()
