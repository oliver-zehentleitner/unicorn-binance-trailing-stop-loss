#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: example_binance_trailing_stop_loss.py
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

from unicorn_binance_trailing_stop_loss.manager import BinanceTrailingStopLossManager
import asyncio
import logging
import os

# Set up logging
logging.getLogger("unicorn_binance_trailing_stop_loss")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# Set up Trailing Stop Loss
api_key = ""
api_secret = ""
exchange = "binance.com"
market = "ETHUSDT"        # The stop loss order is created for the base asset (in this case ETH)
stop_loss_limit = "1.5%"  # The distance to the maximum price at which the stop loss order is trailed


async def trailing_stop_loss_engine():
    def callback_error(msg):
        # Is called up in the event of an error
        print(f"STOP LOSS ERROR - ENGINE IS SHUTTING DOWN! - {msg}")
        ubtsl.stop_manager()

    def callback_finished(msg):
        # Called when the stop loss order has been completely filled
        print(f"STOP LOSS FINISHED - ENGINE IS SHUTTING DOWN! - {msg}")
        ubtsl.stop_manager()

    def callback_partially_filled(msg):
        # Called when the stop loss order has been partially filled
        print(f"STOP LOSS PARTIALLY_FILLED - ENGINE IS STILL RUNNING! - {msg}")

    # Starting the Trailing Stop/Loss Engine
    with BinanceTrailingStopLossManager(api_key=api_key,
                                        api_secret=api_secret,
                                        callback_error=callback_error,
                                        callback_finished=callback_finished,
                                        callback_partially_filled=callback_partially_filled,
                                        exchange=exchange,
                                        market=market,
                                        print_notifications=True,
                                        stop_loss_limit=stop_loss_limit,
                                        warn_on_update=False) as ubtsl:

        while ubtsl.is_manager_stopping() is False:
            # This loop continues until the trailing stop loss engine is terminated
            await asyncio.sleep(1)

try:
    asyncio.run(trailing_stop_loss_engine())
except KeyboardInterrupt:
    print("\r\nGracefully stopping ...")
