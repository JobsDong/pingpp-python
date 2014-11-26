#!/usr/bin/python
#-*- coding=utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


class Charge(object):

	__slots__ = ('id', 'object', 'created', 'livemode', 'paid', 'refunded',
	'app', 'channel', 'order_no', 'client_ip', 'amount', 'amount_settle',
	'currency', 'subject', 'body', 'extra', 'time_expire', 'time_settle',
	'transaction_no', 'refunds', 'amount_refunded', 'failure_code',
	'failure_msg', 'metadata', 'credential', 'description')

	def __init__(self,id, object, created, livemode, paid, refunded,
					  app, channel, order_no, client_ip, amount, amount_settle,
					  currency, subject, body, extra, time_expire, time_settle,
					  transaction_no, refunds, amount_refunded, failure_code,
					  failure_msg, metadata, credential, description):
		pass

	@classmethod
	def list(limit=10, starting_after=None, ending_before=None, app=None,
	         channel=None, paid=None, refunded=None):
		pass

	@classmethod
	def reteive(id):
		pass

	@classmethod
	def create(order_no, app, channel, amount, client_ip, currency, subject, body,
	           extra=None, time_expire=None, metadata=None, description=None):
		pass