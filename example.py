#!/usr/bin/python
#-*- coding=utf-8 -*-

""" pingplusplus 接口
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


import pingpp
from pingpp import Charge, Refund


pingpp.api_key = "API_KEY"

def charge_create():
	ch = Charge.objects.create()
	print ch

def charge_save():
	ch = Charge()
	ch.save()

def charge_filter():
	chs = Charge.objects.filter()

def charge_get():
	ch = Charge.objects.get()

def refund_create():
	ch = Charge.objects.create()
	print ch

def refund_save():
	re = Refund()
	re.save()

def refund_filter():
	res = Refund.objects.filter()

def refund_get():
	re = Refund.objects.get()
