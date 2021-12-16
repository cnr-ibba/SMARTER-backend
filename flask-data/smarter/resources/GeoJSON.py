#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 12:40:09 2021

@author: Paolo Cozzi <bunop@libero.it>
"""

from bson import ObjectId
from bson.errors import InvalidId

from flask import jsonify, current_app
from flask_restful import Resource
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

    def get(self):
        collection = self.model.objects().aggregate([
            {"$match": {"locations": {"$exists": True}}},
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
            current_app.logger.warning(exc)
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
        Get a GeoJSON for all Sheep samples
        ---
        tags:
          - GeoJSON
        description: Query SMARTER data about samples
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
        Get a GeoJSON for all Goat samples
        ---
        tags:
          - GeoJSON
        description: Query SMARTER data about samples
        responses:
            '200':
              description: GeoJSON FeatureCollection
              content:
                application/json:
                  schema:
                    type: object
        """
        return super().get()
