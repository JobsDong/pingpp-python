#!/usr/bin/python
#-*- coding=utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


from query import QuerySet


class Charge(object):

	objects = QuerySet()

	def save(self):
		pass

	def delete(self):
		pass


class Refund(object):

	objects = QuerySet()

	def save(self):
		pass

	def delete(self):
		pass