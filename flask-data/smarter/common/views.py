#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:34:05 2021

@author: Paolo Cozzi <paolo.cozzi@ibba.cnr.it>

This module is an attempt to define class based views like the django ones
"""

from mongoengine.errors import ValidationError, DoesNotExist
from flask import request, url_for, current_app
from flask_restful import Resource, reqparse
from flask_mongoengine2.documents import BaseQuerySet as QuerySet
from urllib.parse import urlencode

from resources.errors import MongoEngineValidationError, ObjectsNotExistsError


class ImproperlyConfigured(Exception):
    pass


class ModelView(Resource):
    queryset = None
    model = None

    def get_object(self, pk, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            try:
                obj = queryset.get(pk=pk)
                current_app.logger.debug(f"Got {obj}")

            except DoesNotExist as e:
                current_app.logger.warning(e)
                raise ObjectsNotExistsError

            except ValidationError as e:
                current_app.logger.error(e)
                raise MongoEngineValidationError

        return obj

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model.objects
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset


class ListView(Resource):
    queryset = None
    model = None
    object_list = None
    endpoint = None
    order_by = None
    page = 1
    size = 10

    parser = reqparse.RequestParser()

    def __init__(self) -> None:
        super().__init__()

        # add sort arguments
        self.parser.add_argument('sort', help="Sort results by this key")
        self.parser.add_argument('order', help="Sort key order")

        # add pagination arguments
        self.parser.add_argument('page', type=int, help="Results page number")
        self.parser.add_argument(
            'size',
            type=int,
            help="Number of results per page"
        )

    def parse_args(self) -> list:
        # reading request parameters
        kwargs = self.parser.parse_args(strict=True)
        args = []

        # filter args
        kwargs = {key: val for key, val in kwargs.items() if val}

        # deal with ordering stuff
        self.order_by = None

        if 'sort' in kwargs:
            self.order_by = kwargs.pop('sort')

        if 'order' in kwargs:
            order = kwargs.pop('order')

            if self.order_by and order == 'desc':
                self.order_by = f"-{self.order_by}"

        # remove pagination arguments
        if 'page' in kwargs:
            self.page = kwargs.pop('page')

        if 'size' in kwargs:
            self.size = kwargs.pop('size')

        return args, kwargs

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

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        return queryset

    def get_context_data(self):
        qs = self.object_list

        current_app.logger.debug(f"Got {qs}")

        # get a shallow copy of an immutable dict
        params = request.args.copy()

        paginated = qs.paginate(page=self.page, per_page=self.size)

        next_ = None
        prev = None

        if paginated.has_next:
            params['size'] = self.size
            params['page'] = self.page + 1
            next_ = url_for(self.endpoint) + '?' + urlencode(params)

        if paginated.has_prev:
            params['size'] = self.size
            params['page'] = self.page - 1
            prev = url_for(self.endpoint) + '?' + urlencode(params)

        return {
            'items': paginated.items,
            'total': paginated.total,
            'pages': paginated.pages,
            'page': paginated.page,
            'size': paginated.per_page,
            'next': next_,
            'prev': prev
        }
