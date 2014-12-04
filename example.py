#!/usr/bin/python
#-*- coding=utf-8 -*-

""" ping plus plus 例子
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


import pingpp

pingpp.api_key = "sk_test_uHmDyTKWffX1enbXDSmLCKe5"

ch = pingpp.Charge.objects.create(order_no="123ffffgdaf34", amount=10,
                                  app={'id': 'app_1Kenv5f5GiDCKWLW'},
                                  channel='upmp',
                                  currency='cny',
                                  client_ip='127.0.0.1',
                                  subject='iphone',
                                  body='hello')
print ch.id, ch


ch = pingpp.Charge.objects.get(id='ch_iH0yT4zLeDqT0i5qbPXzDaz1')
print ch.id, ch


chs = pingpp.Charge.objects.all()
print len(chs)
for ch in chs:
    print ch.id, ch

# TODO 模拟付款，之后再退款
#

re = pingpp.Refund.objects.create(charge_id=ch.id,
                                  amount=100,
                                  description="hello")
print re.id, re


re = pingpp.Refund.objects.get(charge_id=ch.id, refund_id=re.id)
print re


res = pingpp.Refund.objects.all(charge_id=ch.id)
print len(res)

for re in res:
    print re.id, re