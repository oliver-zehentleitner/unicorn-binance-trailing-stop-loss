#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unittest_binance_trailing_stop_loss.py
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

from unicorn_binance_trailing_stop_loss.cli import main
from unicorn_binance_trailing_stop_loss.manager import BinanceTrailingStopLossManager
import logging
import unittest
import os

BINANCE_COM_API_KEY = ""
BINANCE_COM_API_SECRET = ""

logging.getLogger("unicorn_binance_trailing_stop_loss.unicorn_binance_trailing_stop_loss_engine_manager")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

print(f"Starting unittests:")


def callback_error(msg):
    print(f"STOP LOSS ERROR - ENGINE IS SHUTTING DOWN! - {msg}")
    UBTSL.stop_manager()


def callback_finished(msg):
    print(f"STOP LOSS FINISHED - ENGINE IS SHUTTING DOWN! - {msg}")
    UBTSL.stop_manager()


UBTSL = BinanceTrailingStopLossManager(callback_error=callback_error,
                                       callback_finished=callback_finished,
                                       api_key="aaa",
                                       api_secret="bbb",
                                       exchange="binance.com-testnet",
                                       keep_threshold="20%",
                                       reset_stop_loss_price=True,
                                       send_to_email_address="blah@example.com",
                                       send_from_email_address="blub@example.com",
                                       send_from_email_password="pass",
                                       send_from_email_server="mail.example.com",
                                       send_from_email_port=25,
                                       stop_loss_limit="1.5%",
                                       market="BTCUSDT",
                                       stop_loss_order_type="LIMIT",
                                       stop_loss_price=88,
                                       telegram_bot_token="telegram_bot_token",
                                       telegram_send_to="telegram_send_to")


class TestBinanceComManager(unittest.TestCase):
    def test_stop(self):
        self.assertTrue(UBTSL.stop_manager())

    def test_cli(self):
        try:
            main()
        except SystemExit:
            pass


if __name__ == '__main__':
    unittest.main()
