#!/usr/bin/python
# -*- coding=utf-8 -*-

"""ping plus plus exception
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


class ClientError(Exception):
    """client exception
    """


class UriError(ClientError):
    """uri exception
    """


class ConnectError(ClientError):
    """client exception
    """


class RequestError(ClientError):
    """request exception
    """


class ObjectDoesNotExist(Exception):
    """object does not exist exception
    """


class NotSupportError(Exception):
    """not suppoert exception
    """


class ServerError(Exception):
    """server exception
    """


