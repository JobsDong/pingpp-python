#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement


__author__ = ['"wuyadong" <wuyadong311521@gmail.com>']


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys
import pingpp

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pingpp',
    version=pingpp.__version__,
    description='ping plus plus SDK for Python',
    platforms='Platform Independent',
    author='wuyadong zhangxuanyi',
    author_email='wuyadong311521@gmail.com',
    url='https://github.com/jobsdong/pingpp-python',
    packages=['pingpp'],
    install_requires=['requests>=2.2.1'],
    keywords=['pingpp', 'python', 'sdk'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)