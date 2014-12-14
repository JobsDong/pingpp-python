#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>', 'iceout']

import json
import sys

import pingpp
import pingpp.http
import pingpp.util


class Query(object):

    def __get__(self, obj, type_=None):
        if obj is not None:
            raise AttributeError("%s isn't accessible via %s instances" %
                                 (self.__class__.__name__, type_.__name__))
        self.obj_type = type_
        return self

    def retrieve(self, **kwargs):
        url, real_kwargs = pingpp.http.escape_uri(self.obj_type._get_uri(),
                                                  kwargs)
        resp = pingpp.http.request("get", url, params=real_kwargs)
        return self.obj_type.construct(resp, pingpp.api_key)

    def all(self, **kwargs):
        url, real_kwargs = pingpp.http.escape_uri(self.obj_type._all_uri(),
                                                  kwargs)
        resp = pingpp.http.request("get", url,
                                   params=real_kwargs)
        objs = convert_to_pingpp_object(resp, pingpp.api_key)
        return objs

    def create(self, **kwargs):
        url, real_kwargs = pingpp.http.escape_uri(self.obj_type._create_uri(),
                                                  kwargs)
        resp = pingpp.http.request("post", url, data=real_kwargs)
        return self.obj_type.construct(resp, pingpp.api_key)


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
            self[k] = convert_to_pingpp_object(v, self.api_key)

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
            return ''.join(buf)
        finally:
            if isRootObject:
                self._inMyRepr = False

    def __str__(self):
        unicode_repr = json.dumps(self, ensure_ascii=False,
                                  sort_keys=False, indent=2).encode('utf8')

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

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
        obj = cls()
        obj.api_key = api_key
        obj._refesh_content(resp)
        return obj

    def _refesh_content(self, resp, partial=False):
        if partial:
            self._unsaved_values = (self._unsaved_values - set(resp))
        else:
            removed = set(self.keys()) - set(resp)
            self._transient_values = self._transient_values | removed
            self._unsaved_values = set()
            self.clear()
        self._transient_values = self._transient_values - set(resp)
        self._previous_metadata = resp.get('metadata')
        for k, v in dict(resp).iteritems():
            super(PingppObject, self).__setitem__(
                k, convert_to_pingpp_object(v, self.api_key))


class CreateMixin(object):

    @classmethod
    def create(cls, api_key=None, **kwargs):
        if api_key is None:
            api_key = pingpp.api_key
        url = cls.class_url()
        response = pingpp.http.request('post', url, params=kwargs)
        return convert_to_pingpp_object(response, api_key)


class UpdateMixin(object):

    def save(self):
        updated_params = self.serialize(self)

        if getattr(self, 'metadata', None):
            updated_params['metadata'] = self.serialize_metadata()
        if updated_params:
            self._refesh_content(
                pingpp.http.request('post', self.get_url(),
                                    updated_params))
        else:
            pingpp.util.logger.debug("Trying to save already saved object %r",
                                     self)
        return self

    def serialize_metadata(self):
        if 'metadata' in self._unsaved_values:
            # the metadata object has been reassigned
            # i.e. as object.metadata = {key: val}
            metadata_update = self['metadata']
            previous = self._previous_metadata or {}
            keys_to_unset = set(previous.keys()) - \
                set(self['metadata'].keys())
            for key in keys_to_unset:
                metadata_update[key] = ""

            return metadata_update
        else:
            return self.serialize(self['metadata'])

    def serialize(self, obj):
        params = {}
        if obj._unsaved_values:
            for k in obj._unsaved_values:
                if k == 'id':
                    continue
                v = obj[k]
                params[k] = v if v is not None else ""
        return params


class DeleteMixin(object):
    def delete(self, **kwargs):
        self._refesh_content(pingpp.http.request('delete', self.get_url(),
                             kwargs))
        return self


class RefreshMixin(object):
    def refresh(self):
        self._refesh_content(self.request('get', self.get_url()))
        return self


class Charge(UpdateMixin, RefreshMixin, PingppObject):

    __slots__ = ('objects',)
    objects = Query()

    def __init__(self, *args, **kwargs):
        super(Charge, self).__init__(*args, **kwargs)

    @classmethod
    def get_typeuri(cls):
        return 'charges'

    @classmethod
    def _get_uri(self):
        return self.get_typeuri() + '/{charge_id}'

    @classmethod
    def _create_uri(cls):
        return cls.get_typeuri()

    @classmethod
    def _all_uri(cls):
        return cls.get_typeuri()

    def get_url(self):
        return self.get_typeuri() + '/' + self['id']

    def get_refunds_url(self):
        return self.get_url() + '/' + Refund.get_typeuri()

    def refresh_refunds(self, **kwargs):
        self._refesh_content(self.request('get', self.get_refunds_url(),
                             params=kwargs))
        return self

    def create_refund(self, **kwargs):
        """ Maybe use Refund.objects.create(charge_id=...) is more intuitive.
        """
        url, real_kwargs = pingpp.http.escape_uri(Refund._create_uri(),
                                                  {'charge_id': self['id']})
        resp = pingpp.http.request("post", url, params=kwargs)
        return Refund.construct(resp, pingpp.api_key)


class Refund(RefreshMixin, PingppObject):

    __slots__ = ('_charge_id', 'objects')
    objects = Query()

    def __init__(self, charge_id, *args, **kwargs):
        self._charge_id = charge_id
        super(Refund, self).__init__(*args, **kwargs)

    @classmethod
    def get_typeuri(cls):
        return 'refunds'

    @classmethod
    def _get_uri(cls):
        return Charge.get_typeuri() + '/{charge_id}/' + cls.get_typeuri()\
            + '/{refund_id}'

    @classmethod
    def _create_uri(cls):
        return Charge.get_typeuri() + '/{charge_id}/' + cls.get_typeuri()

    @classmethod
    def _all_uri(cls):
        return Charge.get_typeuri() + '/{charge_id}/' + cls.get_typeuri()

    def get_url(self):
        return Charge.get_typeuri() + '/' + self._charge_id + '/' + \
            self.get_typeuri() + '/' + self['id']

    @classmethod
    def construct(cls, resp, api_key):
        obj = cls(resp['charge'], **resp)
        obj.api_key = api_key
        return obj

types = {'charge': Charge, 'refund': Refund}
