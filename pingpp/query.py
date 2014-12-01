#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import requests
from requests.exceptions import ConnectionError, RequestException

from pingpp import api_key, api_url
from pingpp.exception import PingPPClientException, PingPPServiceException


class MultipleObjectsReturned(Exception):
    pass


class ObjectDoesNotExist(Exception):
    pass


class FieldTypeError(Exception):
    pass


class NotSupportError(Exception):
    pass


class QuerySet(object):

    def __init__(self, model, **kwargs):
        self.model = model
        self._kwargs = kwargs
        self._query = dict()
        self._iteration_num = None
        self._response_class = kwargs.get("response_class", Response)
        self._set_objects(responses)

    def __len__(self):
        if self._iteration_num is None:
            return self.count()
        return self._iteration_num

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get(self, *args, **kwargs):
        clone = self.filter(*args, **kwargs)
        num = len(clone._objects)
        if num > 1:
            raise MultipleObjectsReturned()
        elif not num:
            raise ObjectDoesNotExist()
        return clone[0]

    def filter(self, *args, **kwargs):
        return self._filter(*args, **kwargs)

    def _filter(self, *args, **kwargs):
        # TODO
        query = dict(self._query.items() + kwargs.items())
        clone = self._clone(self._get_responses(**query))
        clone._query.update({"id_in": clone._get_ids()})
        return clone

    def _clone(self, responses=None, klass=None, **kwargs):
        responses = responses or self._responses
        klass = klass or self.__class__
        clone = klass(model=self.model, responses=responses, query=self._query)
        clone.__dict__.update(kwargs)
        return clone

    def _get_responses(self, **kwargs):
        return self.model._client.get(**kwargs)

    def _set_objects(self):
        if self._objects is not None\
                and isinstance(self._objects, (tuple, list)):
            for i, obj in enumerate(self._objects):
                if isinstance(obj, dict) is True:
                    self._objects[i] = self._wrap_response(obj)
            return self._objects
        else:
            return []

    def _wrap_response(self, dic):
        return self._response_class(self.model, dic)


class Model(object):

    def __init__(self, **kwargs):
        self._fields = dict()
        self._fields.update(kwargs)

    def __setattr__(self, key, value):
        self._fields[key] = value

    def save(self):
        if hasattr(self, "id"):
            raise NotSupportError()
        else:
            requests.post(self._fields)
            # TODO update model dict


Model.objects = QuerySet(Model)