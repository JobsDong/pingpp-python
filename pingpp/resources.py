#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


from query import Model


class Charge(Model):

    # POST
    @classmethod
    def create_uri(cls):
        return 'charges'

    @classmethod
    def wrap_create_resp(cls, resp_dict):
        # TODO relation
        kwargs = dict(resp_dict.items())
        return kwargs

    @classmethod
    def get_uri(cls):
        return 'charges/{id}'

    @classmethod
    def wrap_get_resp(cls, resp_dict):
        return resp_dict

    @classmethod
    def filter_uri(cls):
        return 'charges'

    @classmethod
    def wrap_filter_resps(cls, resp_dict):
        kwargs = dict(resp_dict.items())
        return kwargs['data']

    @classmethod
    def configure_class(cls):
        return Charge


class Refund(Model):

    # POST
    @classmethod
    def create_uri(cls):
        return 'charges/{charge_id}/refunds'

    @classmethod
    def wrap_create_resp(cls, resp_dict):
        # TODO relation
        kwargs = dict(resp_dict.items())
        return kwargs

    @classmethod
    def get_uri(cls):
        return 'charges/{charge_id}/refunds/{refund_id}'

    @classmethod
    def wrap_get_resp(cls, resp_dict):
        return resp_dict

    @classmethod
    def filter_uri(cls):
        return 'charges/{charge_id}/refunds'

    @classmethod
    def wrap_filter_resps(cls, resp_dict):
        kwargs = dict(resp_dict.items())
        return kwargs['data']

    @classmethod
    def configure_class(cls):
        return Refund
