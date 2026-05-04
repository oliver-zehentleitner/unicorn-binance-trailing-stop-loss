#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# File: dev/pypi/remove_files.sh
#
# Part of ‘UNICORN Binance Trailing Stop Loss’
# Project website: https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html
# Github: https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss
# Documentation: https://unicorn-binance-trailing-stop-loss.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-trailing-stop-loss

#
# License: MIT
# https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/LICENSE
#
# Author: Oliver Zehentleitner
#
# Copyright (c) 2022-2026, Oliver Zehentleitner (https://about.me/oliver-zehentleitner)
# All rights reserved.

rm ./build -r
rm ./dist -r
rm ./unicorn_binance_trailing_stop_loss.egg-info -r
