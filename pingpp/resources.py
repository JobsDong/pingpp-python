#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


import pingpp.http
import sys


class Query(object):

    def __get__(self, obj, type_=None):
        if obj is not None:
            raise AttributeError("%s isn't accessible via %s instances" %
                                 (self.__class__.__name__, type_.__name__))
        self.obj_type = type_
        return self

    def retrieve(self, resource_id, **kwargs):
        base = self.obj_type.get_typeurl()
        url = base + '/' + resource_id
        resp = pingpp.http.request("get", url, params=kwargs)
        return resp


class PingppObject(dict):
    __slots__ = ('_inMyRepr', '_unsaved_values', '_transient_values',
                 '_previous_metadata', 'api_key')

    def __new__(cls, *args, **kwargs):
        obj = dict.__new__(cls)
        obj._inMyRepr = False
        obj._unsaved_values = set()
        obj._transient_values = set()
        obj._previous_metadata = None
        obj.api_key = None
        return obj

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))
        super(PingppObject, self).__setitem__(k, v)
        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()
        self._unsaved_values.add(k)

    def __getitem__(self, k):
        try:
            return super(PingppObject, self).__getitem__(k)
        except KeyError as err:
            if k in self._transient_values:
                raise KeyError(
                    "%r.  HINT: The %r attribute was set in the past."
                    "It was then wiped when refreshing the object with "
                    "the result returned by Pingpp's API, probably as a "
                    "result of a save().  The attributes currently "
                    "available on this object are: %s" %
                    (k, k, ', '.join(self.keys())))
            else:
                raise err

    __dictiter__ = dict.__iter__

    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a PingppObject. "
            "To unset a property, set it to None.")

    def _repr(self):
        """ Avoid infinite recursion
        """
        if self._inMyRepr:
            return '{...}'
        try:
            isRootObject = False
            if not self._inMyRepr:
                isRootObject = True
                self._inMyRepr = True
            buf = []
            buf.append('{')
            comma = ''
            for k in self.__dictiter__():
                buf.append(comma)
                comma = ', '
                buf.append(repr(k))
                buf.append(': ')
                v = self[k]
                buf.append(repr(v))
                buf.append('}')

            if sys.version_info[0] < 3:
                return ''.join(buf).encode('utf-8')
            else:
                return ''.join(buf)
        finally:
            if isRootObject:
                self._inMyRepr = False

    def copy(self):
        newtmp = PingppObject(self)
        for k in self.__slots__:
            setattr(newtmp, k, getattr(self, k))
        return newtmp

    def iteritems(self):
        for k, v in dict.iteritems(self):
            yield k, v

    def items(self):
        return list((k, v) for k, v in dict.iteritems(self))

    def __iter__(self):
        for k in self.__dictiter__():
            yield k


class Charge(PingppObject):

    objects = Query()

    @classmethod
    def get_typeurl(cls):
        return 'charges'

    def get_url(self):
        return self.get_typeurl() + '/' + self.id


class Refund(PingppObject):

    def __init__(self, charge):
        self._charge = charge

    def _get_typeurl(self):
        return self._charge.get_url() + '/refunds'

'''
class Charge(Resource):
    class Meta:
        create_uri = 'charges'
        get_uri = 'charges/{id}'
        all_uri = 'charges'
        wrap_all_resp = lambda resp_dict: resp_dict['data']
        verbose_name = "支付信息"

class Refund(Resource):
    class Meta:
        create_uri = 'charges/{charge_id}/refunds'
        get_uri = 'charges/{charge_id}/refunds/{refund_id}'
        all_uri = 'charges/{charge_id}/refunds'
        wrap_all_resp = lambda resp_dict: resp_dict['data']
        verbose_name = "退款信息"
'''
