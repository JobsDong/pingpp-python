#!/usr/bin/python
# -*- coding=utf-8 -*-


__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']

import json
import requests
import re

import pingpp
from pingpp.exception import UriError


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


def post(uri, params):
    headers = {'content-type': 'application/json'}
    real_uri, real_params = escape_uri(uri, params)
    data = json.dumps(real_params)
    resp = requests.post("%s/%s" % (pingpp.api_url, real_uri),
                         auth=(pingpp.api_key, ''),
                         data=data, headers=headers)
    resp.encoding = 'utf-8'
    return resp.json()


def get(uri, params):
    headers = {'content-type': 'application/json'}
    real_uri, real_params = escape_uri(uri, params)
    resp = requests.get("%s/%s" % (pingpp.api_url, real_uri),
                        auth=(pingpp.api_key, ''),
                        params=real_params, headers=headers)
    resp.encoding = 'utf-8'
    return resp.json()