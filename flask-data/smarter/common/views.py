#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:34:05 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>

This module is an attempt to define class based views like the django ones
"""

from flask import request, url_for
from flask_restful import Resource
from flask_mongoengine import QuerySet
from werkzeug.urls import url_encode


class ImproperlyConfigured(Exception):
    pass


class ListView(Resource):
    queryset = None
    model = None
    object_list = None
    endpoint = None

    def get_queryset(self):
        if self.queryset:
            queryset = self.queryset

            if isinstance(queryset, QuerySet):
                queryset = queryset.all()

        elif self.model:
            queryset = self.model.objects.all()

        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        # HINT: add ordering code?

        return queryset

    def get_context_data(self):
        qs = self.object_list

        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))

        # convert an immutable dict to a dictionary object
        params = request.args.to_dict()

        paginated = qs.paginate(page=page, per_page=size)

        next_ = None
        prev = None

        if paginated.has_next:
            params['size'] = size
            params['page'] = page + 1
            next_ = url_for(self.endpoint) + '?' + url_encode(params)

        if paginated.has_prev:
            params['size'] = size
            params['page'] = page - 1
            prev = url_for(self.endpoint) + '?' + url_encode(params)

        return {
            'items': paginated.items,
            'total': paginated.total,
            'pages': paginated.pages,
            'page': paginated.page,
            'size': paginated.per_page,
            'next': next_,
            'prev': prev
        }
