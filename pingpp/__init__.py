#!/usr/bin/python
#-*- coding=utf-8 -*-

""" pingplusplus 接口
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import resources


__all__ = ('Charge', 'Refund', 'api_key', 'api_url')

api_key = None

api_url = "https://api.pingplusplus.com/v1"

# FIXME buggy
Charge = resources.Charge
Refund = resources.Refund

Charge()
Refund()