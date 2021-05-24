#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:16:39 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
"""

from flask import jsonify, url_for, request
from flask_restful import Resource
from werkzeug.urls import url_encode

from database.models import Breed


class BreedsApi(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        params = {
            'species': request.args.get('species')
        }

        paginated = self.view_breeds(page, size, **params)

        next_ = None
        prev = None

        if paginated.has_next:
            params['size'] = size
            params['page'] = page + 1
            next_ = url_for('breedsapi') + '?' + url_encode(params)

        if paginated.has_prev:
            params['size'] = size
            params['page'] = page - 1
            prev = url_for('breedsapi') + '?' + url_encode(params)

        return jsonify(
            items=paginated.items,
            total=paginated.total,
            pages=paginated.pages,
            page=paginated.page,
            size=paginated.per_page,
            next=next_,
            prev=prev
        )

    def view_breeds(self, page=1, size=10, **kwargs):
        qs = Breed.objects

        if 'species' in kwargs:
            qs = qs.filter(species=kwargs['species'])

        return qs.paginate(page=page, per_page=size)
