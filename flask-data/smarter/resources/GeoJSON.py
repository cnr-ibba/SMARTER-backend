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


class SampleSheepGeoJSONApi(GeoJSONMixin, Resource):
    model = SampleSheep

    @jwt_required()
    def get(self, id_):
        return super().get(id_)


class SampleGoatGeoJSONApi(GeoJSONMixin, Resource):
    model = SampleGoat

    @jwt_required()
    def get(self, id_):
        return super().get(id_)
