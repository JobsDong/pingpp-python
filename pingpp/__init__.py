#!/usr/bin/python
#-*- coding=utf-8 -*-

""" pingplusplus 接口
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

from resources import Charge, Refund

api_key = None

api_url = "https://api.pingplusplus.com/v1"

__all__ = ('Charge', 'Refund', 'api_key', 'api_url')