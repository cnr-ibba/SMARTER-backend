#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 11:23:00 2022

@author: Paolo Cozzi <bunop@libero.it>
"""

import re

from mongoengine.queryset import Q
from flask import jsonify, current_app
from flask_restful import reqparse

from database.models import Country
from common.views import ListView, ModelView


class CountryListApi(ListView):
    endpoint = 'countrylistapi'
    model = Country

    def check_alpha2(value):
        if len(value) != 2:
            raise ValueError(
                f"The value '{value}' is not an alpha2 country code. ")

        return value.upper()

    def check_alpha3(value):
        if len(value) != 3:
            raise ValueError(
                f"The value '{value}' is not an alpha3 country code. ")

        return value.upper()

    parser = reqparse.RequestParser()
    parser.add_argument('species', help="Species name")
    parser.add_argument('name', help="Country name")
    parser.add_argument(
        'alpha_2',
        type=check_alpha2,
        help='Alpha 2 code: {error_msg}'
    )
    parser.add_argument(
        'alpha_3',
        type=check_alpha3,
        help='Alpha 3 code: {error_msg}'
    )
    parser.add_argument(
        'search', help="Search country name and official name by pattern")

    def get_queryset(self):
        # parse request arguments and deal with generic arguments
        args, kwargs = self.parse_args()

        # deal with search fields
        if 'search' in kwargs:
            pattern = kwargs.pop("search")
            pattern = re.compile(pattern, re.IGNORECASE)
            args = [Q(name=pattern) | Q(official_name=pattern)]

            # remove name from args if exists (i'm searching against it)
            if 'name' in kwargs:
                del (kwargs['name'])

        current_app.logger.info(f"{args}, {kwargs}")

        if args or kwargs:
            queryset = self.model.objects.filter(*args, **kwargs)

        else:
            queryset = self.model.objects.all()

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        return queryset

    def get(self):
        """
        Get information on Countries
        ---
        tags:
          - Countries
        description: Query SMARTER data about countries
        parameters:
          - name: species
            in: query
            type: string
            enum: ['Sheep', 'Goat']
            description: The desired species
          - name: name
            in: query
            type: string
            description: Country name
          - name: alpha_2
            in: query
            type: string
            description: Alpha 2 code
          - name: alpha_3
            in: query
            type: string
            description: Alpha 3 code
          - name: search
            in: query
            type: string
            description: Search country name and official name by pattern
        responses:
            '200':
              description: Countries to be returned
              content:
                application/json:
                  schema:
                    type: array
        """
        self.object_list = self.get_queryset()
        data = self.get_context_data()
        return jsonify(**data)


class CountryApi(ModelView):
    model = Country

    def get(self, id_):
        """
        Fetch a single Country
        ---
        tags:
          - Countries
        description: Fetch a single country using ObjectID
        parameters:
          - in: path
            name: id_
            type: string
            description: The country ObjectID
            required: true
        responses:
            '200':
              description: The desired country
              content:
                application/json:
                  schema:
                    type: object
        """

        country = self.get_object(id_)
        return jsonify(country)
