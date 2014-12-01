#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import requests

api_url = "https://api.pingplusplus.com/v1"

class MultipleObjectsReturned(Exception):
    pass


class ObjectDoesNotExist(Exception):
    pass


class FieldTypeError(Exception):
    pass


class NotSupportError(Exception):
    pass


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
            raise KeyError

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get(self, **kwargs):
        clone = self.filter(**kwargs)
        num = len(clone._objs)
        if num > 1:
            raise MultipleObjectsReturned()
        elif not num:
            raise ObjectDoesNotExist()
        return clone[0]

    def filter(self, **kwargs):
        return self._filter(**kwargs)

    def _filter(self, **kwargs):
        query = dict(kwargs.items())
        clone = self._clone(self._get_responses(**query))
        return clone

    def _clone(self, responses=None):
        objs = [self._wrap_response(response)
                for response in responses]
        clone = self.__class__(self.model, objs)
        return clone

    def _get_responses(self, **kwargs):
        resp = requests.get("%s/%s" % (api_url, "charges"),
                            auth=('sk_test_uHmDyTKWffX1enbXDSmLCKe5', ''),
                            params=kwargs)
        import json
        a = json.loads(resp.text)
        print a
        if isinstance(a, (tuple, list)):
            return a
        else:
            return [a]


    def _wrap_response(self, response):
        return self.model(**response)


class Model(object):

    objects = None
    _fields = dict()

    def __init__(self, **kwargs):
        self._fields.update(kwargs)

    def __setattr__(self, key, vaZlue):
        self._fields[key] = value

    def save(self):
        if hasattr(self, "id"):
            raise NotSupportError()
        else:
            import json
            print self._fields
            resp = requests.post("%s/%s" % (api_url, "charges"),
                                 auth=('sk_test_uHmDyTKWffX1enbXDSmLCKe5', ''),
                                 json=self._fields)
            resp.encoding = 'utf-8'
            print resp.json()
            self._fields.update(resp.json())
            # TODO update model dict

Model.objects = QuerySet(Model)