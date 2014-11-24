#!/usr/bin/python
#-*- coding=utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


HUMAN_MODE = False

try:
	import requests
	HUMAN_MODE = True
except ImportError:
	pass


class PingPPServiceException(Exception):
	"""PingPP服务器内部错误
	"""


class PingPPClientException(Exception):
	"""PingPP客户端错误
	"""


class PingPP(object):

	def __init__(self, api_key, timeout=None, human=HUMAN_MODE):
		self._api_key = api_key
		self._timeout = timeout or 60
		self._human = human

		if self._human:
			self._session = requests.Session()

	#-------- charge -----

	def list_charge(self):
		pass

	def create_charge(self, **kwargs):
		pass

	def retrieve_charge(self, charge_id, expand=None):
		pass

	#----- refund -----

	def create_refund(self):
		pass

	def retrieve_refund(self, id, **params):
		pass

	def list_refund(self):
		pass
