#!/usr/bin/python
# -*- coding=utf-8 -*-

"""http request
"""

__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import json
import requests
import requests.exceptions
import re

import pingpp
from pingpp.exception import (UriError, ConnectError, RequestError,
                              ClientError, ServerError)


def escape_uri(uri, kwargs):
    re_key = re.compile(r"{\w+}")
    params = dict(kwargs.items())
    key_needs = [key_with_brace[1:-1]
                 for key_with_brace
                 in re_key.findall(uri)]
    for key in key_needs:
        if key in params:
            params.pop(key)
        else:
            raise UriError("%s lack in uri" % key)
    return uri.format(**kwargs), params


def extract_error_resp(resp):
    try:
        error_dict = resp.json()['error']
    except:
        error_type, error_msg, error_code, error_param = \
            "unknown_error", resp.reason, resp.status_code, ''
    else:
        error_type = error_dict.get('type', 'unknown_error')
        error_msg = error_dict.get('message', '')
        error_code = error_dict.get('code', '')
        error_param = error_dict.get('param', '')

    return error_type, error_msg, error_code, error_param


def request(method, uri, params=None, data=None):
    """ only dict param or dict data accepted
    """
    # header
    headers = {'content-type': 'application/json'}

    # uri, param, data
    try:
        if method.lower() == "get":
            real_uri, real_params = escape_uri(uri, params)
            resp = requests.get("%s/%s" % (pingpp.api_url, real_uri),
                                auth=(pingpp.api_key, ''), params=real_params,
                                headers=headers)
        else:
            real_uri, real_data = escape_uri(uri, data)
            real_data = json.dumps(real_data)
            resp = requests.post("%s/%s" % (pingpp.api_url, real_uri),
                                 auth=(pingpp.api_key, ''), data=real_data,
                                 headers=headers)
        resp.encoding = 'utf-8'
    except requests.exceptions.ConnectionError as e:
        raise ConnectError(str(e))
    except requests.exceptions.RequestException as e:
        raise RequestError(str(e))
    except Exception as e:
        raise ClientError(e)
    else:
        if resp.status_code / 100 == 2:
            return resp.json()
        elif resp.status_code / 100 == 4:
            raise RequestError('request error, type:%s, msg:%s, code:%s,'
                               ' param:%s' % extract_error_resp(resp))
        elif resp.status_code / 100 == 5:
            raise ServerError('server error, type:%s, msg:%s, code:%s,'
                              ' param:%s' % extract_error_resp(resp))
        else:
            raise ClientError('client error, type:%s, msg:%s, code:%s,'
                              ' param:%s' % extract_error_resp(resp))

