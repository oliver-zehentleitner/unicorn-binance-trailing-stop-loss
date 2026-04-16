#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: setup.py
#
# Part of ‘UNICORN Binance Trailing Stop Loss’
# Project website: https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss
# Documentation: https://unicorn-binance-trailing-stop-loss.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-trailing-stop-loss
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2022-2023, LUCIT Systems and Development (https://www.lucit.tech)
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
     version="1.1.0",
     author="LUCIT Systems and Development",
     author_email='info@lucit.tech',
     url="https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss",
     description="A Python library by LUCIT with a command line interface for a trailing stop loss and smart entry on "
                 "the Binance exchange.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     license='LSOSL - LUCIT Synergetic Open Source License',
     install_requires=['lucit-licensing-python>=1.8.1', 'Cython', 'requests', 'unicorn-binance-websocket-api>=2.1.1',
                       'unicorn-binance-rest-api>=2.2.0'],
     keywords='Binance, Binance Futures, Binance Margin, Binance Isolated Margin, Binance Testnet, Trailing Stop Loss, '
              'Smart Entry',
     project_urls={
        'Documentation': 'https://lucit-systems-and-development.github.io/unicorn-binance-trailing-stop-loss',
        'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/wiki',
        'Author': 'https://www.lucit.tech',
        'Changes': 'https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/changelog.html',
        'License': 'https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/license.html',
        'Issue Tracker': 'https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/issues',
        'Chat': 'https://gitter.im/unicorn-binance-suite/unicorn-binance-trailing-stop-loss',
        'Telegram': 'https://t.me/unicorndevs',
        'Get Support': 'https://www.lucit.tech/get-support.html',
        'LUCIT Online Shop': 'https://shop.lucit.services/software',
     },
     python_requires='>=3.7.0',
     package_data={'': ['unicorn_binance_local_depth_cache/*.so',
                        'unicorn_binance_local_depth_cache/*.dll']},
     entry_points={
         "console_scripts": [
             "ubtsl = unicorn_binance_trailing_stop_loss.cli:main",
         ]},
     classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Programming Language :: Python :: 3.7",
         "Programming Language :: Python :: 3.8",
         "Programming Language :: Python :: 3.9",
         "Programming Language :: Python :: 3.10",
         "Programming Language :: Python :: 3.11",
         "Programming Language :: Python :: 3.12",
         "License :: Other/Proprietary License",
         'Intended Audience :: Developers',
         "Intended Audience :: Financial and Insurance Industry",
         "Intended Audience :: Information Technology",
         "Intended Audience :: Science/Research",
         "Operating System :: OS Independent",
         "Topic :: Office/Business :: Financial :: Investment",
         'Topic :: Software Development :: Libraries :: Python Modules',
     ],
)
