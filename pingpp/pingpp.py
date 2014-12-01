#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


from query import Model


class Charge(Model):

    def __init__(self, **kwargs):
        super(Charge, self).__init__(**kwargs)


class Refund(Model):

    def __init__(self, **kwargs):
        super(Refund, self).__init__(**kwargs)



if __name__ == "__main__":
    charge = Charge.objects.create(order_no='12345678g9', amount=100,
                                   app={'id':'app_1Kenv5f5GiDCKWLW'},
                                   channel='upmp', currency='cny',
                                   client_ip='127.0.0.1', subject='iphone',
                                   body='hello')
    print charge
    charges = Charge.objects.filter()
    print len(charges)
