#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:22:59 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from .auth import LoginApi
from .breeds import BreedListApi, BreedApi
from .chips import SupportedChipApi, SupportedChipListApi
from .datasets import DatasetListApi, DatasetApi
from .info import SmarterInfoApi
from .samples import (
    SampleSheepApi, SampleSheepListApi, SampleGoatApi, SampleGoatListApi)
from .GeoJSON import (
    SampleSheepGeoJSONApi, SampleGoatGeoJSONApi, SampleSheepGeoJSONListApi,
    SampleGoatGeoJSONListApi)
from .variants import (
    VariantSheepApi, VariantGoatApi, VariantSheepOAR3Api, VariantSheepOAR4Api,
    VariantGoatCHI1Api, VariantGoatARS1Api)


def initialize_routes(api):
    api.add_resource(LoginApi, '/smarter-api/auth/login')

    api.add_resource(SmarterInfoApi, '/smarter-api/info')

    api.add_resource(BreedListApi, '/smarter-api/breeds')
    api.add_resource(BreedApi, '/smarter-api/breeds/<string:id_>')

    api.add_resource(SupportedChipListApi, '/smarter-api/supported-chips')
    api.add_resource(
        SupportedChipApi, '/smarter-api/supported-chips/<string:id_>')

    api.add_resource(DatasetListApi, '/smarter-api/datasets')
    api.add_resource(DatasetApi, '/smarter-api/datasets/<string:id_>')

    api.add_resource(SampleSheepListApi, '/smarter-api/samples/sheep')
    api.add_resource(SampleSheepApi, '/smarter-api/samples/sheep/<string:id_>')

    api.add_resource(
        SampleSheepGeoJSONListApi,
        '/smarter-api/samples.geojson/sheep')
    api.add_resource(
        SampleSheepGeoJSONApi,
        '/smarter-api/samples.geojson/sheep/<string:id_>')

    api.add_resource(SampleGoatListApi, '/smarter-api/samples/goat')
    api.add_resource(SampleGoatApi, '/smarter-api/samples/goat/<string:id_>')

    api.add_resource(
        SampleGoatGeoJSONListApi,
        '/smarter-api/samples.geojson/goat')
    api.add_resource(
        SampleGoatGeoJSONApi,
        '/smarter-api/samples.geojson/goat/<string:id_>')

    api.add_resource(VariantSheepOAR3Api, '/smarter-api/variants/sheep/OAR3')
    api.add_resource(VariantSheepOAR4Api, '/smarter-api/variants/sheep/OAR4')
    api.add_resource(
        VariantSheepApi, '/smarter-api/variants/sheep/<string:id_>')

    api.add_resource(VariantGoatCHI1Api, '/smarter-api/variants/goat/CHI1')
    api.add_resource(VariantGoatARS1Api, '/smarter-api/variants/goat/ARS1')
    api.add_resource(VariantGoatApi, '/smarter-api/variants/goat/<string:id_>')
