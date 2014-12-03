#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" resource queryset
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import http

from exception import NotSupportError


class QuerySet(object):

    def __init__(self, model, objs=None):
        self.model = model
        self._objs = objs

    def __len__(self):
        return len(self._objs)

    def __iter__(self):
        return iter(self._objs)

    def __getitem__(self, index):
        return self._objs[index]

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get(self, **kwargs):
        resp = http.request("get", self.model._meta.get_uri, params=kwargs)
        return self.model(**self.model._meta.wrap_get_resp(resp))

    def filter(self, **kwargs):
        resp = http.request("get", self.model._meta.filter_uri, params=kwargs)
        objs = [self.model(**self.model._meta.wrap_get_resp(resp))
                for resp in self.model._meta.wrap_filter_resp(resp)]
        clone = self.__class__(self.model, objs)
        return clone


DEFAULT_WRAPS = dict(
    wrap_create_resp=lambda r: dict(r),
    wrap_get_resp=lambda r: dict(r),
    wrap_filter_resp=lambda r: list(r),
)


class Options(object):

    def __init__(self, meta, model_name):
        # default attrs
        attrs = dict(DEFAULT_WRAPS)
        attrs.update({
            "create_uri": model_name.lower(),
            "get_uri": "%s/{id}" % model_name.lower(),
            "filter_uri": model_name.lower(),
        })

        # meta attrs
        if meta:
            meta_attrs = meta.__dict__.copy()
            for name in self.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]

        for attr_name in attrs.keys():
            if attr_name in meta_attrs:
                setattr(self, attr_name, meta_attrs.pop(attr_name))
            elif hasattr(meta, attr_name):
                setattr(self, attr_name, getattr(meta, attr_name))
            else:
                setattr(self, attr_name, attrs[attr_name])


class ResourceBase(type):
    """
    Metaclass for all resources
    """

    def __new__(mcs, name, bases, attrs):
        super_new = super(ResourceBase, mcs).__new__
        parents = [b for b in bases if isinstance(b, ResourceBase)]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        # create the class
        module = attrs.pop('__module__')
        new_class = super_new(mcs, name, bases, {'__module__': module})

        # meta
        meta = attrs.pop('Meta', None)
        if not meta:
            meta = getattr(new_class, 'Meta', None)

        setattr(new_class, "_meta", Options(meta, name))

        # attr
        for n, v in attrs.items():
            setattr(new_class, n, v)

        # queryset
        setattr(new_class, "objects", QuerySet(new_class))

        return new_class


class Resource(object):
    __metaclass__ = ResourceBase

    def __init__(self, **kwargs):
        self._fields = {}
        self._fields.update(kwargs)

    def __getattr__(self, key):
        if key not in self._fields:
            raise AttributeError
        else:
            return self._fields[key]

    def __str__(self):
        return '<%s object>' % self.__class__.__name__

    def save(self):
        if hasattr(self, "id"):
            raise NotSupportError("not support update operation")
        else:
            resp = http.request("post", self._meta.create_uri,
                                data=self._fields)
            self._fields.update(self._meta.wrap_create_resp(resp))