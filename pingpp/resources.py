#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


from query import Resource


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
