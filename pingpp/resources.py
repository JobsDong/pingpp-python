#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


import pingpp.http
import pingpp.api_key
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
        return self.obj_type.construct(resp, pingpp.api_key)

    def all(self, **kwargs):
        resp = pingpp.http.request("get", self.model._meta.all_uri, params=kwargs)
        objs = [self.model(**self.model._meta.wrap_get_resp(resp))
                for resp in self.model._meta.wrap_all_resp(resp)]
        clone = self.__class__(self.model, objs)
        return clone

def convert_to_pingpp_object(resp, api_key):

    if isinstance(resp, list):
        return [convert_to_pingpp_object(i, api_key) for i in resp]
    elif isinstance(resp, dict) and not isinstance(resp, PingppObject):
        resp = resp.copy()
        klass_name = resp.get('object')
        if klass_name == 'list':
            return convert_to_pingpp_object(resp['data'], api_key)
        else:
            klass = types.get(klass_name, PingppObject)
            return klass.construct(resp, api_key)
    else:
        return resp


class PingppObject(dict):
    """ PingppObject

    Extends dict is not a good idea.
    """
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

    def __repr__(self):
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

    @classmethod
    def construct(cls, resp, api_key):
        obj = cls(resp)
        obj.api_key = api_key
        return obj


class CreateMixin(object):

    @classmethod
    def create(cls, api_key=None, **kwargs):
        if api_key is None:
            api_key = pingpp.api_key
        url = cls.class_url()
        response = pingpp.http.request('post', url, params=kwargs)
        return convert_to_pingpp_object(response, api_key)


class UpdateMixin(object):
    pass


class DeleteMixin(object):
    def delete(self, **kwargs):
        self.refresh_from(pingpp.http.request('delete', self.get_url(),
                          kwargs))
        return self


class RefreshMixin(object):
    def refresh(self):
        self.refresh_from(self.request('get', self.get_url()))
        return self


class Charge(UpdateMixin, RefreshMixin, PingppObject):

    __slots__ = ('objects',)
    objects = Query()

    def __init__(self, *args, **kwargs):
        super(Charge, self).__init__(*args, **kwargs)

    @classmethod
    def get_typeurl(cls):
        return 'charges'

    def get_url(self):
        return self.get_typeurl() + '/' + self.id

    def get_refunds_url(self):
        return self.get_url() + '/refunds'

    def refresh_refunds(self, **kwargs):
        self.refresh_from(self.request('get', self.get_refunds_url(),
                          params=kwargs))
        return self


class Refund(RefreshMixin, PingppObject):

    __slots__ = ('_charge', 'objects')
    objects = Query()

    def __init__(self, charge, amount, desc):
        self._charge = charge

    def get_url(self):
        return self._charge.get_refunds_url() + '/' + self[id]


types = {'charge': Charge, 'refund': Refund}
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
