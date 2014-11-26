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
	def __init__(self, status, msg, err):
		self.args = (status, msg, err)
		self.status = status
		self.msg = msg
		self.err = err


class PingPPClientException(Exception):
	"""PingPP客户端错误
	"""
	def __init__(self, msg):
		self.msg = msg
		super(PingPPClientException, self).__init__(msg)


class PingPP(object):

	def __init__(self, api_key, timeout=None, human=HUMAN_MODE):
		self._api_key = api_key
		self._timeout = timeout or 60
		self._human = human

		if self._human:
			self._session = requests.Session()

	# -------- charge -----

	def create_charge(self, **kwargs):
		pass

	def list_charge(self, **kwargs):
		pass

	def retrive_charge(self, **kwargs):
		pass

	# ----- refund -----

	def create_refund(self):
		pass

	def retrieve_refund(self, id, **params):
		pass

	def list_refund(self):
		pass

	# --------- private -----
	def _do_http_request(self, method, uri, value=None, headers=None,
	                     params=None, callback=None):
		if headers is None:
			headers = []

		if hasattr(value, '__len__'):
			headers['Content-Length'] = len(value)
			length = len(value)
		elif value is not None:
			raise PingPPClientException('object type error')

		if self._human:
			return self._do_http_human(method, uri, value, headers, params)
		else:
			pass

	def _do_http_human(self, method, uri, value, headers, params):
		#TODO url
		try:
			resp = self._session.request(method, uri, data=value, headers=headers,
			                             timeout=self._timeout)
			resp.encoding = 'utf-8'

			status = resp.status_code
			if status / 100 == 2:
				if method == 'Get':
					content = resp.text
				elif method == 'Put' or method == 'HEAD':
					content = resp.headers.items()
			else:
				msg = resp.reason
				err = resp.text
		except requests.exceptions.ConnectionError as e:
			raise PingPPClientException(str(e))
		except requests.exceptions.RequestException as e:
			raise PingPPClientException(str(e))
		except Exception as e:
			raise PingPPClientException(str(e))

		if msg:
			raise PingPPServiceException(status, msg, err)

		return content

