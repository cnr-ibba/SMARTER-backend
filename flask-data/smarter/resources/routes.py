#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:22:59 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from .auth import LoginApi
from .breeds import BreedApiList, BreedApi
from .chips import SupportedChipApi, SupportedChipListApi
from .datasets import DatasetsApi, DatasetApi
from .samples import (
    SampleSheepApi, SampleSheepListApi, SampleGoatApi, SampleGoatListApi)
from .variants import (
    VariantSheepApi, VariantSheepListApi, VariantGoatApi, VariantGoatListApi)


def initialize_routes(api):
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(BreedApiList, '/api/breeds')
    api.add_resource(BreedApi, '/api/breeds/<string:id_>')

    api.add_resource(SupportedChipListApi, '/api/supported-chips')
    api.add_resource(SupportedChipApi, '/api/supported-chips/<string:id_>')

    api.add_resource(DatasetsApi, '/api/datasets')
    api.add_resource(DatasetApi, '/api/datasets/<string:id_>')

    api.add_resource(SampleSheepListApi, '/api/samples/sheep')
    api.add_resource(SampleSheepApi, '/api/samples/sheep/<string:id_>')

    api.add_resource(SampleGoatListApi, '/api/samples/goat')
    api.add_resource(SampleGoatApi, '/api/samples/goat/<string:id_>')

    api.add_resource(VariantSheepListApi, '/api/variants/sheep')
    api.add_resource(VariantSheepApi, '/api/variants/sheep/<string:id_>')

    api.add_resource(VariantGoatListApi, '/api/variants/goat')
    api.add_resource(VariantGoatApi, '/api/variants/goat/<string:id_>')
