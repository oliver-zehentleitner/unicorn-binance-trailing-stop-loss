#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: setup.py
#
# Part of 'UNICORN Binance Trailing Stop Loss'
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss
# Github: https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss
# PyPI: https://pypi.org/project/unicorn-binance-trailing-stop-loss
#
# License: MIT
# https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/LICENSE
#
# Author: Oliver Zehentleitner
#
# Copyright (c) 2022-2026, Oliver Zehentleitner (https://about.me/oliver-zehentleitner)
# All rights reserved.

from setuptools import setup
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     ext_modules=cythonize(
        ['unicorn_binance_trailing_stop_loss/__init__.py',
         'unicorn_binance_trailing_stop_loss/cli.py',
         'unicorn_binance_trailing_stop_loss/manager.py'],
        annotate=False),
     name='unicorn-binance-trailing-stop-loss',
     version="1.3.1",
     author="Oliver Zehentleitner",
     author_email='',
     url="https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss",
     description="A Python library with a command line interface for a trailing stop loss and smart entry on "
                 "the Binance exchange.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     license='MIT',
     install_requires=['Cython', 'requests', 'unicorn-binance-websocket-api>=2.13.0',
                       'unicorn-binance-rest-api>=2.2.0'],
     keywords='Binance, Binance Futures, Binance Margin, Binance Isolated Margin, Binance Testnet, Trailing Stop Loss, '
              'Smart Entry',
     project_urls={
        'Documentation': 'https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss',
        'Wiki': 'https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/wiki',
        'Author': 'https://about.me/oliver-zehentleitner',
        'Changes': 'https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/changelog.html',
        'License': 'https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/LICENSE',
        'Issue Tracker': 'https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/issues',
        'Telegram': 'https://t.me/unicorndevs',
     },
     python_requires='>=3.9.0',
     package_data={'': ['unicorn_binance_trailing_stop_loss/*.so',
                        'unicorn_binance_trailing_stop_loss/*.dll']},
     entry_points={
         "console_scripts": [
             "ubtsl = unicorn_binance_trailing_stop_loss.cli:main",
         ]},
     classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3.10",
         "Programming Language :: Python :: 3.11",
         "Programming Language :: Python :: 3.12",
         "Programming Language :: Python :: 3.13",
         "Programming Language :: Python :: 3.14",
         "License :: OSI Approved :: MIT License",
         'Intended Audience :: Developers',
         "Intended Audience :: Financial and Insurance Industry",
         "Intended Audience :: Information Technology",
         "Intended Audience :: Science/Research",
         "Operating System :: OS Independent",
         "Topic :: Office/Business :: Financial :: Investment",
         'Topic :: Software Development :: Libraries :: Python Modules',
     ],
)
