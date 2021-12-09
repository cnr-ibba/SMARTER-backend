#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 15:37:00 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, current_app
from flask_restful import reqparse
from flask_jwt_extended import jwt_required

from database.models import SupportedChip
from common.views import ListView, ModelView


class SupportedChipApi(ModelView):
    model = SupportedChip

    @jwt_required()
    def get(self, id_):
        """
        Fetch a single chip
        ---
        tags:
          - Supported Chips
        description: Fetch a single chip using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The chip ObjectID
            required: true
        responses:
            '200':
              description: The desidered chip
              content:
                application/json:
                  schema:
                    type: object
        """
        variant = self.get_object(id_)
        return jsonify(variant)


class SupportedChipListApi(ListView):
    model = SupportedChip
    endpoint = "supportedchiplistapi"

    parser = reqparse.RequestParser()
    parser.add_argument('species', help="Species name")
    parser.add_argument('manifacturer', help="Chip manifacturer")
    parser.add_argument('name', help="Chip name")

    def get_queryset(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        return queryset

    @jwt_required()
    def get(self):
        """
        Get information on chips
        ---
        tags:
          - Supported Chips
        description: Query SMARTER data about chips
        parameters:
          - name: species
            in: query
            type: string
            description: The desidered species (Sheep or Goat)
          - name: name
            in: query
            type: string
            description: Chip name
          - name: manifacturer
            in: query
            type: string
            description: Chip manifacturer (affymetrix or illumina)
        responses:
            '200':
              description: Chips to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)
