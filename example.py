#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>', 'iceout']

import pingpp
import pingpp.http
import requests

pingpp.api_key = "KEY"

ch = pingpp.Charge.objects.retrieve(charge_id='ch_id')
print ch

chs = pingpp.Charge.objects.all()
print len(chs)
# for ch in chs:
#     print ch

ch = pingpp.Charge.objects.create(order_no="adf9fhr1hr3hhhj12a",
                                  amount=100,
                                  app={'id': 'app_id'},
                                  channel='upmp',
                                  currency='cny',
                                  client_ip='127.0.0.1',
                                  subject='apple',
                                  body='一天一个苹果')
requests.get(
    'https://api.pingplusplus.com/notify/charges/'+ch['id']+'?livemode=false')

refund = pingpp.Refund.objects.create(charge_id=ch['id'],
                                      amount=10,
                                      description="太贵了,打个折")

refund = pingpp.Refund.objects.retrieve(
    charge_id=ch['id'],
    refund_id=refund['id'])
print refund, type(refund)


refunds = pingpp.Refund.objects.all(charge_id=ch['id'])
print len(refunds)
