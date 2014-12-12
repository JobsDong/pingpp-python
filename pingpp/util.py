#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging

import pingpp.exception

RE_KEY = re.compile(r"{\w+}")
logger = logging.getLogger('pingpp')


def escape_uri(uri, kwargs):
    params = dict(kwargs.items())
    key_needs = [key_with_brace[1:-1]
                 for key_with_brace
                 in RE_KEY.findall(uri)]
    for key in key_needs:
        if key in params:
            params.pop(key)
        else:
            raise pingpp.exception.UriError("%s lack in kwargs" % key)
    return uri.format(**kwargs), params
