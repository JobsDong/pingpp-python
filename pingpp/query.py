#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


class QuerySet(object):

    def __get__(self, instance, type_=None):
        """ QuerySet shouldn't be accessible from instance.
        """
        if instance is not None:
            raise AttributeError("%s isn't accessible via %s instances" %
                                 (self.__class__.__name__, type_.__name__))
        return self

    def create(self):
        """ I think this method should be defined in Charge and Refund.
        QuerySet should only do query list. It returns a list of Charge objects
        or Refund objects.
        """
        pass

    def get(self):
        pass

    def filter(self):
        pass
