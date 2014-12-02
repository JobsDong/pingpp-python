#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import http

from exception import NotSupportError

api_url = "https://api.pingplusplus.com/v1"


class QuerySet(object):

    def __init__(self, model, objs=None):
        self.model = model
        self._objs = objs

    def __len__(self):
        return len(self._objs)

    def __getitem__(self, index):
        if index < len(self._objs):
            return self._objs[index]
        else:
            raise StopIteration

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get(self, **kwargs):
        resp = http.get(self.model.get_uri(), kwargs)
        return self.model(**self.model.wrap_get_resp(resp))

    def filter(self, **kwargs):
        resps = http.get(self.model.filter_uri(), kwargs)
        objs = [self.model(**self.model.wrap_create_resp(resp))
                for resp in self.model.wrap_filter_resps(resps)]
        clone = self.__class__(self.model, objs)
        return clone


class Model(object):

    def __new__(cls, *args, **kwargs):
        base = cls.configure_class()
        if not hasattr(base, 'objects'):
            base.objects = QuerySet(base)

        instance = super(Model, cls).__new__(base)
        return instance

    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self._fields = dict()
        self._fields.update(kwargs)

    def __getattr__(self, key):
        return self._fields[key]

    def __str__(self):
        return str(self._fields)

    def save(self):
        if hasattr(self, "id"):
            raise NotSupportError("not support update operation")
        else:
            resp = http.post(self.create_uri(), self._fields)
            self._fields.update(self.wrap_create_resp(resp))

    # POST
    @classmethod
    def create_uri(cls):
        raise NotImplementedError

    @classmethod
    def wrap_create_resp(cls, resp_dict):
        raise NotImplementedError

    @classmethod
    def get_uri(cls):
        raise NotImplementedError

    @classmethod
    def wrap_get_resp(cls, resp_dict):
        raise NotImplementedError

    @classmethod
    def filter_uri(cls):
        raise NotImplementedError

    @classmethod
    def wrap_filter_resps(cls, resp_dict):
        raise NotImplementedError

    @classmethod
    def configure_class(cls):
        raise NotImplementedError