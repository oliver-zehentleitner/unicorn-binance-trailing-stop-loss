#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_trailing_stop_loss/manager.py
#
# Part of ‘UNICORN Binance Trailing Stop Loss’
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
# Copyright (c) 2022-2025, Oliver Zehentleitner (https://about.me/oliver-zehentleitner)
# All rights reserved.

from unicorn_binance_rest_api import BinanceRestApiManager, BinanceAPIException
from unicorn_binance_websocket_api import BinanceWebSocketApiManager, UnknownExchange
from typing import Optional, Union
import cython
import datetime
import logging
import math
import platform
import smtplib
import requests
import socket
import ssl
import sys
import threading
import time

__app_name__ = "unicorn-binance-trailing-stop-loss"
__version__ = "1.3.1"
__logger__ = logging.getLogger("unicorn_binance_trailing_stop_loss")


class BinanceTrailingStopLossManager(threading.Thread):
    """
    Manage stop/loss orders on the Binance exchange.

    Initialising the class spawns a new thread in which a stop/loss order is placed and trailed until it is
    completely fulfilled.

    Optional support for:
        - Telegram and Email notifications - see `send_*` and `telegram_*` parameters.
        - Setting "success" and "error" callback functions - see `callback_finished` and `callback_error` parameters.
        - Handling of partial fills - see `callback_partially_filled` parameter, note that partial fills are
        currently not directly handled by the engine.
        - Smart entry - by setting the `engine` param to `jump-in-and-trail`, it offers the possibility to buy
        spot, future and margin assets with a limit or market order and then to trail a stop/loss order until sold.

    Supported exchanges: binance.com, binance.com-testnet, binance.com-futures, binance.com-margin,
    binance.com-isolated_margin

    # Authentication parameters

    :param api_key: Provide the Binance API key.
    :type api_key: str
    :param api_secret: Provide the Binance API secret.
    :type api_secret: str

    # Engine Control parameters

    :param disable_colorama: set to True to disable the use of `colorama <https://pypi.org/project/colorama/>`_
    :type disable_colorama: bool
    :param engine: Activate standard trailing stop/loss with `trail` (default), or activate the experimental smart
    entry method by setting `jump-in-and-trail`
    :type engine: str
    :param start_engine: Start the trailing stop loss engine. Default is True
    :type start_engine: bool
    :param test: Specify the subsystem to test. Supported options are : "notification", "binance-connectivity"
                and "streams". The streams test needs a valid exchange and market. Note that this value MUST be None
                or the engine will NOT start! Only tests will be performed.
    :type test: str

    # Stop loss parameters

    :param stop_loss_order_type: Order type. Possible values are `limit` and `market`. If neither is
    set, the algorithm will NOT run.
    :type stop_loss_order_type: str

    :param stop_loss_price: Price at which the stop/loss order is submitted. Valid until it gets overwritten
    by a higher price.
    :type stop_loss_price: float

    :param stop_loss_limit: Stop loss limit in percent or as fixed float value
    :type stop_loss_limit: str

    :param stop_loss_start_limit: The stop/loss order is trailed with the distance defined in `stop_loss_limit`. For
                                 different initial parameters, you can use `stop_loss_start_limit`. This value will be
                                 used instead of the `stop_loss_limit` value until this value is caught up and then
                                 trailed.
    :type stop_loss_start_limit: str

    :param stop_loss_trigger_gap: Gap between stop price and limit order price, use integer or percent
    values.
    :type stop_loss_trigger_gap: str

    :param reset_stop_loss_price: Reset an existing stop_loss_price and force a new one to be calculated. Only True
                                  evaluates to True, anything else is False!
    :type reset_stop_loss_price: bool

    :param keep_threshold: Percentage to keep when selling. Providing % symbol is optional , i.e. "1" is equal to
    "1%". If empty, the full balance is sold.
    :type keep_threshold: str

    :param borrow_threshold: TODO provide description
    :type borrow_threshold: str

    # Callback parameters

    :param callback_error: Callback to call if error occurs.
    :type callback_error: function or None
    :param callback_finished: Callback to call if stop_loss gets filled.
    :type callback_finished: function or None
    :param callback_partially_filled: Callback to call if stop_loss is only partially filled.
    :type callback_partially_filled: function or None

    # Exchange & Market parameters

    :param exchange: Exchange endpoint to connected to: binance.com, binance.com-futures, binance.com-margin,
                     binance.com-isolated_margin
    :type exchange: str
    :param market: Market to enforce stop/loss on, e.g. "ETHBTC"
    :type market: str
    :param trading_fee_use_bnb: Whether to use BNB for a discount on trading fees.  Default is False. See:
                                https://www.binance.com/en/support/faq/115000583311 for details.
    :type trading_fee_use_bnb: bool

    # Logging and Notification parameters

    :param current_price: Current market price. Used for logging purposes only, updated automatically from the stream.
    :type current_price: float
    :param print_notifications: Print user friendly information to terminal.
    :param send_to_email_address: Receiver's email address
    :type send_to_email_address: str
    :param send_from_email_address: Sender's email address
    :type send_from_email_address: str
    :param send_from_email_password: SMTP auth password
    :type send_from_email_password: str
    :param send_from_email_server: SMTP server hostname or IP
    :type send_from_email_server: str
    :param send_from_email_port: SMTP server port
    :type send_from_email_port: int
    :param telegram_bot_token: Telegram API Token
    :type telegram_bot_token: str
    :param telegram_send_to: Receiver's UserId (i.e. not username) on Telegram.
    :type telegram_send_to: str

    # Unicorn Binance Suite parameters

    :param warn_on_update: set to `False` to disable the update warning
    :type warn_on_update: bool
    :param ubra_manager: Provide a shared unicorn_binance_rest_api.manager instance
    :type ubra_manager: BinanceRestApiManager
    :param ubwa_manager: Provide a shared unicorn_binance_websocket_api.manager instance.
    :type ubwa_manager: BinanceWebSocketApiManager
    """

    def __init__(self,
                 api_key: str = None,
                 api_secret: str = None,
                 borrow_threshold: str = None,
                 callback_error: Optional[type(abs)] = None,
                 callback_finished: Optional[type(abs)] = None,
                 callback_partially_filled: Optional[type(abs)] = None,
                 disable_colorama: bool = False,
                 engine: str = "trail",
                 exchange: str = "binance.com",
                 keep_threshold: str = None,
                 market: str = None,
                 print_notifications: bool = False,
                 reset_stop_loss_price: bool = False,
                 send_to_email_address: str = None,
                 send_from_email_address: str = None,
                 send_from_email_password: str = None,
                 send_from_email_server: str = None,
                 send_from_email_port: int = None,
                 start_engine: bool = True,
                 stop_loss_limit: str = None,
                 stop_loss_order_type: str = None,
                 stop_loss_price: float = None,
                 stop_loss_start_limit: str = None,
                 stop_loss_trigger_gap: str = "0.01",
                 telegram_bot_token: str = None,
                 telegram_send_to: str = None,
                 test: str = None,
                 trading_fee_discount_futures_percent: float = 10.0,
                 trading_fee_discount_margin_percent: float = 25.0,
                 trading_fee_discount_spot_percent: float = 25.0,
                 trading_fee_percent: float = 0.1,
                 trading_fee_use_bnb: bool = False,
                 ubra_manager: Optional[Union[BinanceRestApiManager]] = None,
                 ubwa_manager: Optional[Union[BinanceWebSocketApiManager]] = None,
                 warn_on_update=True):
        threading.Thread.__init__(self)
        self.name = __app_name__
        self.logger = __logger__
        self.version = __version__
        self.logger.info(f"New instance of {self.get_user_agent()}-{'compiled' if cython.compiled else 'source'} on "
                         f"{str(platform.system())} {str(platform.release())} for exchange {exchange} started")
        self.api_key = api_key
        self.api_secret = api_secret
        self.borrow_threshold = borrow_threshold
        self.callback_error = callback_error
        self.callback_finished = callback_finished
        self.callback_partially_filled = callback_partially_filled
        self.current_price: float = 0.0
        self.engine = engine
        self.exchange = exchange
        self.exchange_info: dict = {}
        self.keep_threshold = keep_threshold
        self.last_update_check_github = {'timestamp': time.time(), 'status': {'tag_name': None}}
        self.lock_create_stop_loss_order = threading.Lock()
        self.precision_price: int = 8
        self.precision_quantity: int = 8
        self.print_notifications = print_notifications
        self.reset_stop_loss_price = True if reset_stop_loss_price is True else False
        self.send_to_email_address = send_to_email_address
        self.send_from_email_address = send_from_email_address
        self.send_from_email_password = send_from_email_password
        self.send_from_email_server = send_from_email_server
        self.send_from_email_port = send_from_email_port
        self.start_engine = start_engine
        self.stop_loss_asset_name: str = ""
        self.stop_loss_asset_amount: float = 0.0
        self.stop_loss_asset_amount_free: float = 0.0
        self.stop_loss_limit = stop_loss_limit
        self.market = market
        self.stop_loss_order_id: int = 0
        self.stop_loss_order_type = stop_loss_order_type
        self.stop_loss_price: float = None if stop_loss_price is None else float(stop_loss_price)
        self.stop_loss_start_limit = stop_loss_start_limit
        self.stop_loss_quantity: float = 0.0
        self.stop_loss_trigger_gap = stop_loss_trigger_gap
        self.stop_loss_request: bool = False
        self.stop_manager_request: bool = False
        self.symbol_info: dict = {}
        self.telegram_bot_token = telegram_bot_token
        self.telegram_send_to = telegram_send_to
        self.test = test
        self.trade_stream_id = None
        self.trading_fee_discount_futures_percent = trading_fee_discount_futures_percent
        self.trading_fee_discount_margin_percent = trading_fee_discount_margin_percent
        self.trading_fee_discount_spot_percent = trading_fee_discount_spot_percent
        self.trading_fee_percent = trading_fee_percent
        self.trading_fee_use_bnb = trading_fee_use_bnb
        self.user_stream_id = None
        self.ubra = ubra_manager
        self.ubwa = ubwa_manager

        self.ubra: BinanceRestApiManager = ubra_manager or BinanceRestApiManager(api_key=self.api_key,
                                                                                 api_secret=self.api_secret,
                                                                                 exchange=self.exchange,
                                                                                 disable_colorama=disable_colorama,
                                                                                 warn_on_update=warn_on_update)
        if warn_on_update and self.is_update_available():
            update_msg = f"Release {self.name}_{self.get_latest_version()} is available, please consider updating! " \
                         f"(Changelog: https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/changelog.html)"
            print(update_msg)
            self.logger.warning(update_msg)
        try:
            self.ubwa: BinanceWebSocketApiManager = ubwa_manager or \
                                                        BinanceWebSocketApiManager(exchange=self.exchange,
                                                                                   output_default="UnicornFy",
                                                                                   disable_colorama=disable_colorama,
                                                                                   high_performance=True,
                                                                                   warn_on_update=warn_on_update,
                                                                                   ubra_manager=self.ubra,
                                                                                   show_secrets_in_logs=True)
        except UnknownExchange:
            self.logger.critical("BinanceTrailingStopLossManager() - Please use a valid exchange!")
            if test is None or "streams" in str(test):
                if self.print_notifications:
                    print(f"Please use a valid exchange!")
                sys.exit(1)
        if test is None and start_engine is True:
            msg = f"Starting the ubtsl engine"
            self.logger.info(msg)
            if self.print_notifications:
                print(msg)
            self.start()
        elif test == "notification":
            msg = f"Starting notification test"
            self.logger.info(msg)
            if self.print_notifications:
                print(msg)
            notification_text = f"Subject: unicorn-binance-trailing-stop-loss notification test\n\nTest notification"
            if self.send_email_notification(notification_text):
                msg = f"E-Mail sent, please check for incoming messages!"
                self.logger.info(msg)
                if self.print_notifications:
                    print(msg)
            if self.send_telegram_notification(notification_text):
                msg = f"Telegram sent, please check for incoming messages!"
                self.logger.info(msg)
                if self.print_notifications:
                    print(msg)
        elif test == "binance-connectivity":
            msg = f"Starting connectivity test to Binance API"
            self.logger.info(msg)
            if self.print_notifications:
                print(msg)
            try:
                response = self.ubra.get_account()
                if response['makerCommission']:
                    if self.print_notifications:
                        msg = f"Connection to Binance API successfully established!"
                        self.logger.error(msg)
                        if self.print_notifications:
                            print(msg)
            except BinanceAPIException as error_msg:
                self.logger.error(error_msg)
                if self.print_notifications:
                    print(error_msg)
        elif "streams" in str(test):
            msg = f"Starting streams test"
            test_time_in_seconds = str(test).replace("streams", "")
            if test_time_in_seconds == "":
                test_time_in_seconds = 0
            else:
                test_time_in_seconds = int(test_time_in_seconds)
            self.logger.info(msg)
            if self.print_notifications:
                print(msg)
            self.start_streams()
            try:
                i = 0
                while self.is_manager_stopping() is False:
                    i += 1
                    self.ubwa.print_summary(title=f"UNICORN Binance Trailing Stop Loss {self.version} - "
                                                  f"Testing streams")
                    print(f"Press CTRL+C to leave this test!\r\n")
                    if test_time_in_seconds == 0 or test_time_in_seconds > i:
                        time.sleep(1)
                    else:
                        break
            except KeyboardInterrupt:
                print("\nStopping ... just wait a few seconds!")
                self.stop_manager()
                sys.exit(0)
        else:
            if test is not None:
                msg = f"Stopping, test `{test}` is an invalid option!"
                self.logger.error(msg)
                if self.print_notifications:
                    print(msg)

    def __enter__(self):
        self.logger.debug(f"Entering 'with-context' ...")
        return self

    def __exit__(self, exc_type, exc_value, error_traceback):
        self.logger.debug(f"Leaving 'with-context' ...")
        self.stop_manager()
        if exc_type:
            self.logger.critical(f"An exception occurred: {exc_type} - {exc_value} - {error_traceback}")

    def calculate_stop_loss_amount(self,
                                   amount: float
                                   ) -> Optional[float]:
        """
        Calculate the tradeable stop/loss asset amount (= owning and free - trading fee)

        :param amount: The full owning asset amount.
        :type amount: float

        :return: float or None
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.calculate_stop_loss_amount() - Calculation stop/loss "
                          f"amount without trading fee")
        fee = self.trading_fee_percent
        final_fee = 0
        if self.exchange == "binance.com":
            final_fee = fee
        elif self.exchange == "binance.com-futures":
            final_fee = fee
        elif self.exchange == "binance.com-margin":
            final_fee = fee / 100 * (100-self.trading_fee_discount_margin_percent)
        elif self.exchange == "binance.com-isolated_margin":
            final_fee = fee / 100 * (100-self.trading_fee_discount_margin_percent)
        amount_without_fee = amount/100*(100-final_fee)
        return amount_without_fee

    @staticmethod
    def calculate_stop_loss_price(price: Union[str, float] = None,
                                  limit: Union[str, float] = None
                                  ) -> Optional[float]:
        """
        Calculate the stop/loss price.

        :param price: Base price used for the calculation
        :type price: float, str
        :param limit: Stop loss limit in percent or as fixed float value
        :type limit: float, str

        :return: float or None
        """
        __logger__.debug(f"BinanceTrailingStopLossManager.calculate_stop_loss_price() - Calculation stop/loss price "
                         f"of base price: {price}, limit: {limit}")
        price = float(price)
        if "%" in str(limit):
            limit_percent = float(limit.rstrip("%"))
            sl_price = float(price / 100) * float(100.0 - limit_percent)
        else:
            sl_price = price - float(limit)
        return BinanceTrailingStopLossManager.round_decimals_down(sl_price, 2)

    def cancel_open_stop_loss_order(self) -> bool:
        """
        Cancel all open stop/loss orders.

        :return: bool
        """
        open_orders = self.get_open_orders(market=self.market)
        if open_orders:
            for open_order in open_orders:
                if open_order['type'] == "STOP_LOSS_LIMIT":
                    self.logger.info(f"BinanceTrailingStopLossManager.cancel_open_stop_loss_order() - Cancelling "
                                     f"open STOP_LOSS_LIMIT order (orderID={open_order['orderId']}) "
                                     f"with stop_loss_price={open_order['price']}.")
                    try:
                        if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                            canceled_order = self.ubra.cancel_order(symbol=self.market,
                                                                    orderId=open_order['orderId'])
                        elif self.exchange == "binance.com-isolated_margin":
                            canceled_order = self.ubra.cancel_margin_order(symbol=self.market,
                                                                           isIsolated="TRUE",
                                                                           orderId=open_order['orderId'])
                        elif self.exchange == "binance.com-margin":
                            canceled_order = self.ubra.cancel_margin_order(symbol=self.market,
                                                                           orderId=open_order['orderId'])
                        elif self.exchange == "binance.com-futures":
                            canceled_order = self.ubra.futures_cancel_order(symbol=self.market,
                                                                            orderId=open_order['orderId'])
                        else:
                            self.logger.info(
                                f"BinanceTrailingStopLossManager.create_stop_loss_order() - Invalid exchange "
                                f"`{self.exchange}`")
                            if self.print_notifications:
                                print(f"Invalid exchange `{self.exchange}`")
                            return False
                    except BinanceAPIException as error_msg:
                        self.logger.error(f"BinanceTrailingStopLossManager.cancel_open_stop_loss_order() - "
                                          f"error_msg: {error_msg}")
                        return False
                    self.logger.info(f"BinanceTrailingStopLossManager.cancel_open_stop_loss_order() - New "
                                     f"order_status of orderID={canceled_order['orderId']} is"
                                     f" {canceled_order['status']}.")
                    return True
        self.logger.info(f"BinanceTrailingStopLossManager.cancel_open_stop_loss_order() - No open order for "
                         f"cancellation found!")
        return False

    def create_stop_loss_order(self,
                               stop_loss_price: float = None,
                               current_price: float = None) -> bool:
        """
        Create a stop/loss order!

        :param stop_loss_price: Price to set for the SL order.
        :type stop_loss_price: float
        :param current_price: Current price is optional and only used for logging.
        :type current_price: float

        :return: bool
        """
        order_is_placed = False
        with self.lock_create_stop_loss_order:
            if self.stop_loss_price is None and stop_loss_price is not None:
                self.set_stop_loss_price(stop_loss_price)
            elif self.stop_loss_price is not None and stop_loss_price is None:
                self.set_stop_loss_price(self.stop_loss_price)
            elif self.stop_loss_price is not None and stop_loss_price is not None:
                if stop_loss_price > self.stop_loss_price:
                    self.set_stop_loss_price(stop_loss_price)
                else:
                    stop_loss_price = self.stop_loss_price
            if self.cancel_open_stop_loss_order():
                return True
            total, free = self.update_stop_loss_asset_amount()
            if self.keep_threshold is not None:
                stop_loss_quantity = self.round_decimals_down(self.update_stop_loss_quantity(total=total,
                                                                                             free=free),
                                                              self.precision_quantity)
            else:
                stop_loss_quantity = self.calculate_stop_loss_amount(free)

            free = free - stop_loss_quantity
            self.stop_loss_asset_amount_free = free

            if current_price is not None:
                current_price_str = f"current_price={current_price}, "
            else:
                current_price_str = ""
            self.logger.info(f"BinanceTrailingStopLossManager.create_stop_loss_order() - Creating stop/loss "
                             f"order: {current_price_str}"
                             f"stop_price={self.get_stop_loss_trigger_price(stop_loss_price)}, "
                             f"sell_price={stop_loss_price}, "
                             f"owning_amount={total}, "
                             f"owning_amount_free={free}, "
                             f"stop_loss_quantity={stop_loss_quantity}")
            if stop_loss_quantity == 0:
                msg = f"Empty stop_loss_quantity in create_stop_loss_order()"
                self.logger.error(f"BinanceTrailingStopLossManager.create_stop_loss_order() - {msg}")
                if self.print_notifications:
                    print(f"Stopping because stop_loss_quantity is zero!")
                self.send_email_notification(msg)
                self.send_telegram_notification(msg)
                self.stop_manager()
                if self.callback_error is not None:
                    self.callback_error(msg)
                return False
            while order_is_placed is False:
                try:
                    if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                        new_order = self.ubra.create_order(symbol=self.market,
                                                           side="SELL",
                                                           type="STOP_LOSS_LIMIT",
                                                           price=self.stop_loss_price,
                                                           stopPrice=self.get_stop_loss_trigger_price(stop_loss_price),
                                                           quantity=str(round(stop_loss_quantity,
                                                                              self.precision_quantity)),
                                                           timeInForce="GTC")
                    elif self.exchange == "binance.com-isolated_margin":
                        new_order = self.ubra.create_margin_order(symbol=self.market,
                                                                  isIsolated="TRUE",
                                                                  side="SELL",
                                                                  type="STOP_LOSS_LIMIT",
                                                                  price=self.stop_loss_price,
                                                                  stopPrice=self.get_stop_loss_trigger_price(stop_loss_price),
                                                                  quantity=str(round(stop_loss_quantity,
                                                                                     self.precision_quantity)),
                                                                  timeInForce="GTC")
                    elif self.exchange == "binance.com-margin":
                        new_order = self.ubra.create_margin_order(symbol=self.market,
                                                                  side="SELL",
                                                                  type="STOP_LOSS_LIMIT",
                                                                  price=self.stop_loss_price,
                                                                  stopPrice=self.get_stop_loss_trigger_price(stop_loss_price),
                                                                  quantity=str(round(stop_loss_quantity,
                                                                                     self.precision_quantity)),
                                                                  timeInForce="GTC")
                    elif self.exchange == "binance.com-futures":
                        new_order = self.ubra.futures_create_order(symbol=self.market,
                                                                   side="SELL",
                                                                   type="STOP_LOSS_LIMIT",
                                                                   price=self.stop_loss_price,
                                                                   stopPrice=self.get_stop_loss_trigger_price(stop_loss_price),
                                                                   quantity=str(round(stop_loss_quantity,
                                                                                      self.precision_quantity)),
                                                                   timeInForce="GTC")
                    else:
                        self.logger.info(f"BinanceTrailingStopLossManager.create_stop_loss_order() - Invalid exchange "
                                         f"`{self.exchange}`")
                        if self.print_notifications:
                            print(f"Invalid exchange `{self.exchange}`")
                        return False
                    self.stop_loss_order_id = new_order['orderId']
                    self.logger.info(f"BinanceTrailingStopLossManager.create_stop_loss_order() - Created stop/loss "
                                     f"order for market {new_order['symbol']} - Response: {new_order}.")
                    if self.print_notifications:
                        print(f"Created stop/loss order for market {new_order['symbol']}: "
                              f"stop_loss_price={self.stop_loss_price} and "
                              f"stop_loss_quantity={self.stop_loss_quantity}")
                    order_is_placed = True
                except BinanceAPIException as error_msg:
                    if "code=-2010" in str(error_msg):
                        waiting_time = 5
                        self.logger.info(f"BinanceTrailingStopLossManager.create_stop_loss_order() - Retrying in "
                                         f"{waiting_time} seconds")
                        if self.print_notifications:
                            print(f"Retrying in {waiting_time} seconds")
                        time.sleep(waiting_time)
                    else:
                        self.logger.error(f"BinanceTrailingStopLossManager.create_stop_loss_order() - {error_msg}")
                        if self.print_notifications:
                            print(f"Can not create stop/loss order! error: {error_msg}")
                        return False
            return True

    @staticmethod
    def get_latest_release_info():
        """
        Get info about the latest available release
        :return: dict or False
        """
        try:
            respond = requests.get('https://api.github.com/repos/oliver-zehentleitner/unicorn-binance-trailing'
                                   '-stop-loss/releases/latest')
            latest_release_info = respond.json()
            return latest_release_info
        except KeyError as error_msg:
            __logger__.error(f"BinanceTrailingStopLossManager.get_latest_release_info() - {error_msg}")
            return False

    def get_latest_version(self) -> Optional[str]:
        """
        Get the version of the latest available release (cache time 1 hour)
        :return: str or None
        """
        # Do a fresh request if status is None or last timestamp is older 1 hour
        if self.last_update_check_github['status']['tag_name'] is None or \
                (self.last_update_check_github['timestamp']+(60*60) < time.time()):
            latest_release = self.get_latest_release_info()
            try:
                self.last_update_check_github['status']['tag_name'] = latest_release['tag_name']
            except KeyError as error_msg:
                self.logger.error(f"BinanceTrailingStopLossManager.get_latest_version() - KeyError: {error_msg}")
                return None
        return self.last_update_check_github['status']['tag_name']

    def get_exchange_info(self) -> Union[dict, bool]:
        """
        Get the exchange info.

        :return: dict or bool
        """
        if self.exchange == "binance.com" or self.exchange == "binance.com-testnet" or \
                self.exchange == "binance.com-margin" or self.exchange == "binance.com-isolated_margin":
            self.exchange_info = self.ubra.get_exchange_info()
        elif self.exchange == "binance.com-futures":
            self.exchange_info = self.ubra.futures_exchange_info()
        else:
            self.logger.error(f"BinanceTrailingStopLossManager.get_exchange_info() - Invalid exchange "
                              f"`{self.exchange}`")
            if self.print_notifications:
                print(f"Invalid exchange `{self.exchange}`")
            return False

        for item in self.exchange_info['symbols']:
            if item['symbol'] == self.market:
                return item
        return False

    def get_open_orders(self,
                        market: str = None) -> Optional[dict]:
        """
        Get the open orders on a given market.

        :return: dict or None
        """
        try:
            if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                open_orders = self.ubra.get_open_orders(symbol=market)
            elif self.exchange == "binance.com-futures":
                open_orders = self.ubra.futures_get_open_orders(symbol=market)
            elif self.exchange == "binance.com-margin":
                open_orders = self.ubra.get_open_margin_orders(symbol=market)
            elif self.exchange == "binance.com-isolated_margin":
                open_orders = self.ubra.get_open_margin_orders(symbol=market, isIsolated="TRUE")
            else:
                return None
            return open_orders
        except BinanceAPIException as error_msg:
            self.logger.error(f"BinanceTrailingStopLossManager.get_open_orders() - {error_msg}")
            return None

    def get_owning_amount(self,
                          base_asset: str = None) -> Optional[tuple]:
        """
        Get the owning amount of the stop/loss asset.

        :return: tuple (total, free) or None
        """
        try:
            if self.exchange == "binance.com" or self.exchange == "binance.com-testnet":
                account_info = self.ubra.get_account()
            elif self.exchange == "binance.com-futures":
                account_info = self.ubra.futures_account()
            elif self.exchange == "binance.com-margin":
                account_info = self.ubra.get_margin_account()
            elif self.exchange == "binance.com-isolated_margin":
                account_info = self.ubra.get_isolated_margin_account()
            else:
                self.logger.error(f"BinanceTrailingStopLossManager.get_owning_amount() - Invalid exchange "
                                  f"`{self.exchange}`")
                if self.print_notifications:
                    print(f"Invalid exchange `{self.exchange}`")
                return None
        except BinanceAPIException as error_msg:
            self.logger.error(f"BinanceTrailingStopLossManager.get_owning_amount() - {error_msg}")
            return None

        if self.exchange == "binance.com":
            for item in account_info['balances']:
                base_asset_pool = item
                if base_asset_pool['asset'] == base_asset:
                    self.logger.info(f"BinanceTrailingStopLossManager.get_owning_amount() - Owning "
                                     f"{base_asset_pool['asset']}: free={base_asset_pool['free']}, "
                                     f"total={base_asset_pool['free']})")
                    return float(base_asset_pool['free']), float(base_asset_pool['free'])
        else:
            for item in account_info['assets']:
                base_asset_pool = item['baseAsset']
                if base_asset_pool['asset'] == base_asset:
                    self.logger.info(f"BinanceTrailingStopLossManager.get_owning_amount() - Owning "
                                     f"{base_asset_pool['asset']}: free={base_asset_pool['free']}, "
                                     f"total={base_asset_pool['totalAsset']} "
                                     f"(interest={base_asset_pool['interest']})")
                    return float(base_asset_pool['totalAsset']), float(base_asset_pool['free'])
        return None

    @staticmethod
    def get_precision(step_size=None):
        if step_size is None:
            return None
        parts = str(step_size).split('.')
        if len(parts) == 2:
            count = 0
            for char in parts[1]:
                count += 1
                if char == '1':
                    return count
            return count
        else:
            return 0

    def get_stop_loss_asset_amount(self) -> Optional[float]:
        """
        Get the current stop/loss asset amount.

        :return: float
        """
        return self.round_decimals_down(self.stop_loss_asset_amount, self.precision_quantity)

    def get_stop_loss_asset_amount_free(self) -> Optional[float]:
        """
        Get the free current stop/loss asset amount.

        :return: float
        """
        return self.round_decimals_down(self.stop_loss_asset_amount_free, self.precision_quantity)

    def get_stop_loss_price(self) -> Optional[float]:
        """
        Get the current stop loss price.

        :return: float
        """
        if self.exchange == "binance.com":
            if self.symbol_info['quoteAsset'] == "USDT":
                return self.round_decimals_down(self.stop_loss_price, 2)
            else:
                return self.stop_loss_price
        else:
            if self.symbol_info['quote'] == "USDT":
                return self.round_decimals_down(self.stop_loss_price, 2)
            else:
                return self.stop_loss_price

    def get_stop_loss_trigger_price(self,
                                    stop_loss_price: float = 0.0) -> Optional[float]:
        """
        Get the current stop/loss trigger price - if this price gets touched the limit order will get placed in the
        orderbook.

        :return: float
        """
        if "%" in self.stop_loss_trigger_gap:
            gap_percent = float(self.stop_loss_trigger_gap.rstrip("%"))
            trigger_gap = float(self.get_stop_loss_price()/100)*float(100.0-gap_percent)
        else:
            trigger_gap = float(self.stop_loss_trigger_gap)
        trigger_gap = float(self.round_decimals_down(trigger_gap, self.precision_quantity))
        precision = self.precision_quantity

        if stop_loss_price == 0:
            stop_loss_price = self.stop_loss_price
        trigger_price = round(stop_loss_price + trigger_gap, 2)
        if len(str(trigger_price).split(".")[1]) <= precision:
            return trigger_price
        else:
            return self.round_decimals_down(trigger_price, precision)

    def get_symbol_info(self,
                        symbol: str = None) -> Optional[dict]:
        """
         Get the symbol info of the stop/loss asset.

         :return: dict
         """
        try:
            if self.exchange == "binance.com":
                symbol_info = self.ubra.get_symbol_info(symbol=symbol)
            elif self.exchange == "binance.com-futures":
                symbol_info = self.ubra.get_symbol_info(symbol=symbol)
            elif self.exchange == "binance.com-margin":
                symbol_info = self.ubra.get_margin_symbol(symbol=symbol)
            elif self.exchange == "binance.com-isolated_margin":
                symbol_info = self.ubra.get_isolated_margin_symbol(symbol=symbol)
            else:
                symbol_info = None
            return symbol_info
        except BinanceAPIException as error_msg:
            self.logger.error(f"BinanceTrailingStopLossManager.get_symbol_info() - {error_msg}")
            if "APIError(code=-2008): Invalid Api-Key ID" in error_msg:
                if self.print_notifications:
                    print(f"ERROR: Not able to fetch `symbol_info`. {error_msg}")
                sys.exit(1)
            return None

    def get_user_agent(self):
        """
        Get the user_agent string "lib name + lib version + python version"
        :return:
        """
        user_agent = f"{self.name}_{str(self.get_version())}-python_{str(platform.python_version())}"
        return user_agent

    @staticmethod
    def get_version() -> str:
        """
        Get the package/module version
        :return: str
        """
        return __version__

    def is_manager_stopping(self):
        """
        Returns `True` if the manager has a stop request, 'False' if not.

        :return: bool
        """
        if self.stop_manager_request is False:
            return False
        else:
            return True

    def is_update_available(self) -> bool:
        """
        Is a new release of this package available?
        :return: bool
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.is_update_available() - Starting the request")
        installed_version = self.get_version()
        if ".dev" in installed_version:
            installed_version = installed_version[:-4]
        if self.get_latest_version() == installed_version:
            return False
        elif self.get_latest_version() is None:
            return False
        else:
            return True

    def process_userdata_stream(self,
                                stream_data: dict = None,
                                stream_buffer_name=False):
        """
        Process the received data of the userData stream.

        :return: bool
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream(stream_data={stream_data}, "
                          f"stream_buffer_name={stream_buffer_name}) started")
        if self.is_manager_stopping() is False:
            if stream_data['event_type'] == "executionReport":
                if stream_data['order_id'] == self.stop_loss_order_id:
                    if stream_data['current_order_status'] == "FILLED":
                        msg = f"Subject: unicorn-binance-trailing-stop-loss '{self.market}'\n\n" \
                              f"STOP LOSS FILLED at price {stream_data['order_price']} (order_id={stream_data['order_id']})"
                        msg_short = f"STOP LOSS FILLED at price {stream_data['order_price']} " \
                                    f"(order_id={stream_data['order_id']})"
                        log_msg_short = " ".join(msg_short.strip())
                        self.logger.info(f"BinanceTrailingStopLossManager.process_userdata_stream() - {log_msg_short}")
                        if self.print_notifications:
                            print(msg_short)
                        self.send_telegram_notification(msg)
                        self.send_email_notification(msg)
                        self.stop_manager()
                        if self.callback_finished is not None:
                            self.callback_finished(stream_data)
                        return True
                    elif stream_data['current_order_status'] == "CANCELED":
                        self.logger.info(f"BinanceTrailingStopLossManager.process_userdata_stream() - "
                                         f"Received CANCELED event, trigger creation of new order")
                        if self.print_notifications:
                            print("Received CANCELED event, creating a new order")
                        self.create_stop_loss_order(self.stop_loss_price, current_price=self.current_price)
                        return False
                    elif stream_data['current_order_status'] == "PARTIALLY_FILLED":
                        self.logger.warning(f"BinanceTrailingStopLossManager.process_userdata_stream() - "
                                            f"Received PARTIALLY_FILLED event")
                        if self.print_notifications:
                            print("Received PARTIALLY_FILLED event")
                        if self.callback_partially_filled is not None:
                            self.callback_partially_filled(stream_data)
                        return False
                    elif stream_data['current_order_status'] == "NEW":
                        self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - Received event: "
                                          f"{str(stream_data)}")
                    else:
                        self.logger.critical(f"BinanceTrailingStopLossManager.process_userdata_stream() - Received unknown"
                                             f" event: {str(stream_data)}")
                        if self.print_notifications:
                            print("Unknown, please report:", str(stream_data))
                elif stream_data['current_order_status'] == "NEW":
                    self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - Received event: "
                                      f"{str(stream_data)}")
                elif stream_data['current_order_status'] == "CANCELED":
                    self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - Received event: "
                                      f"{str(stream_data)}")
                else:
                    self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - "
                                      f"Received stream_data: {stream_data}")
                    if self.print_notifications:
                        print("Unknown, please report:", str(stream_data))
            elif stream_data['event_type'] == "outboundAccountPosition":
                self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - Received: {stream_data}")
            else:
                self.logger.debug(f"BinanceTrailingStopLossManager.process_userdata_stream() - "
                                  f"Received unknown stream_data: {stream_data}")
                if self.print_notifications:
                    print("Unknown, please report:", str(stream_data))

    def process_price_feed_stream(self,
                                  stream_data: dict = None,
                                  stream_buffer_name=False) -> bool:
        """
        Process the price feed data:
        Control current price and update `stop_loss_price` or trigger stop/loss if needed.

        :return: bool
        """
        if "streams" in str(self.test):
            self.logger.debug(f"BinanceTrailingStopLossManager.process_price_feed_stream() - Not processing in test "
                              f"mode")
            return True
        self.logger.debug(f"BinanceTrailingStopLossManager.process_price_feed_stream(stream_data={stream_data}, "
                          f"stream_buffer_name={stream_buffer_name}) started")
        if self.is_manager_stopping() is False:
            if stream_data.get('price'):
                self.current_price = stream_data.get('price')
                sl_price = self.calculate_stop_loss_price(stream_data.get('price'), self.stop_loss_limit)
                if self.stop_loss_price is None:
                    self.logger.info(f"BinanceTrailingStopLossManager.process_price_feed_stream() - Setting "
                                     f"stop_loss_price from None to {sl_price}!")
                    if self.print_notifications:
                        print(f"Setting stop_loss_price from None to {sl_price}!")
                    self.create_stop_loss_order(sl_price, current_price=stream_data.get('price'))
                elif self.stop_loss_price < sl_price:
                    self.logger.info(f"BinanceTrailingStopLossManager.process_price_feed_stream() - Setting "
                                     f"stop_loss_price from {self.stop_loss_price} to {sl_price}!")
                    if self.print_notifications:
                        print(f"Setting stop_loss_price from {self.stop_loss_price} to {sl_price}!")
                    self.create_stop_loss_order(sl_price, current_price=stream_data.get('price'))

    @staticmethod
    def round_decimals_down(number: float,
                            decimals: int = 2) -> float:
        """
        Returns a value rounded down to a specific number of decimal places.
        :param number: The decimal number to round down.
        :type number: float
        :param decimals: How many decimals you want to keep.
        :type decimals: int
        :return: float
        """
        if not isinstance(decimals, int):
            raise TypeError("BinanceTrailingStopLossManager.round_decimals_down() - Decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("BinanceTrailingStopLossManager.round_decimals_down() - Decimal places has to be 0 or "
                             "more")
        elif decimals == 0:
            return math.floor(number)
        else:
            factor = 10 ** decimals
            return math.floor(number * factor) / factor

    def start_streams(self) -> bool:
        """
        Procedure to start the web streams

        :return: bool
        """
        if self.exchange == "binance.com-isolated_margin":
            symbol = self.market
        else:
            symbol = False
        self.user_stream_id = self.ubwa.create_stream("arr", "!userData",
                                                      api_key=self.api_key,
                                                      api_secret=self.api_secret,
                                                      process_stream_data=self.process_userdata_stream,
                                                      symbols=symbol,
                                                      stream_label="UserData")
        self.trade_stream_id = self.ubwa.create_stream(channels="aggTrade",
                                                       markets=self.market,
                                                       process_stream_data=self.process_price_feed_stream,
                                                       stream_label="PriceFeed")
        return True

    def run(self) -> None:
        """
        Start Stop/Loss with provided settings!

        :return: None
        """
        self.start_streams()

        if self.stop_loss_start_limit:
            limit = self.stop_loss_start_limit
        else:
            limit = self.stop_loss_limit

        if self.engine == "jump-in-and-trail":
            self.logger.info(f"Starting jump-in-and-trail engine")
            if self.print_notifications:
                print(f"Starting `jump-in-and-trail` engine")

            buy_order = None
            buy_price = None

            if self.exchange == "binance.com-isolated_margin":
                isolated_margin_account = self.ubra.get_isolated_margin_account()

                for item in isolated_margin_account['assets']:
                    if item['symbol'] == self.market:
                        if self.borrow_threshold:
                            loan_details = self.ubra.get_margin_loan_details()
                            print(f"Loan details: {loan_details}")
                            # Todo: Take loan -> gain free quote asset

                        amount_to_buy = isolated_margin_account['assets'][0]['quoteAsset']['free']

                        try:
                            buy_order = self.ubra.create_margin_order(symbol=self.market,
                                                                      isIsolated="TRUE",
                                                                      side="BUY",
                                                                      type="MARKET",
                                                                      quoteOrderQty=amount_to_buy,
                                                                      sideEffectType="MARGIN_BUY")

                            print(f"Buy order: {buy_order}")

                            # Todo: Calc real buy price (average)
                            buy_price = buy_order['fills'][0]['price']

                            self.stop_loss_price = self.calculate_stop_loss_price(price=buy_price,
                                                                                  limit=limit)

                        except BinanceAPIException as error_msg:
                            msg = f"Stopping because of Binance API exception: {error_msg}"
                            logging.critical(msg)
                            if self.print_notifications:
                                print(msg)
                            if self.callback_error is not None:
                                self.callback_error(msg)
                            return None

                        # We expect only one match, so we leave if we found one
                        break
            else:
                msg = f"Option `jump-in-and-trail` in parameter `engine` is not supported for exchange " \
                      f"'{self.exchange}'!"
                self.logger.critical(msg)
                if self.print_notifications:
                    print(msg)
                sys.exit(1)
            self.logger.info(f"Jumped in with buy order: {buy_order}")
            if self.print_notifications:
                print(f"Jumped in with buy price: {buy_price}")
        elif self.engine == "trail":
            msg = f"Starting `trail` engine"
            self.logger.info(msg)
            if self.print_notifications:
                print(msg)
        else:
            msg = f"Engine `{self.engine}` is not supported!"
            self.logger.critical(msg)
            if self.print_notifications:
                print(msg)
            sys.exit(1)
        self.logger.info(f"BinanceTrailingStopLossManager.run() - Starting trailing stop/loss on {self.exchange} "
                         f"for the market {self.market}")
        if self.print_notifications:
            print(f"Starting trailing stop/loss on {self.exchange} for the market {self.market}")
        self.logger.debug(f"BinanceTrailingStopLossManager.run() - reset_stop_loss_price="
                          f"{self.reset_stop_loss_price}")
        self.symbol_info = self.get_symbol_info(symbol=self.market)

        symbol_info_symbols = self.ubra.get_exchange_info(**{'symbol': self.market})['symbols']
        for symbols in symbol_info_symbols:
            if symbols.get('filters') is not None:
                for filters in symbols.get('filters'):
                    if filters.get('filterType') == "LOT_SIZE":
                        self.precision_quantity = self.get_precision(filters['stepSize'])

        self.logger.info(f"BinanceTrailingStopLossManager.run() -  used_weight: {self.ubra.get_used_weight()}")
        if self.symbol_info is None:
            self.logger.critical(f"BinanceTrailingStopLossManager.run() - `symbol_info` is None")
            if self.print_notifications:
                print(f"ERROR: `symbol_info` is None -> Stopping!")
            self.stop_manager()
            sys.exit(1)
        if self.exchange == "binance.com":
            self.stop_loss_asset_name = self.symbol_info['baseAsset']
        else:
            self.stop_loss_asset_name = self.symbol_info['base']
        self.exchange_info = self.get_exchange_info()
        self.update_stop_loss_asset_amount()

        self.logger.info(f"BinanceTrailingStopLossManager.start() - Waiting till streams are running")
        if self.ubwa.wait_till_stream_has_started(self.user_stream_id) and \
                self.ubwa.wait_till_stream_has_started(self.trade_stream_id):
            time.sleep(5)
            self.logger.info(f"BinanceTrailingStopLossManager.start() - UserData and Trade streams are running!")

        if self.stop_loss_price is None or self.stop_loss_price == 0.0:
            if self.reset_stop_loss_price is not True:
                open_orders = self.get_open_orders(market=self.market)
                if open_orders:
                    for open_order in open_orders:
                        if open_order['type'] == "STOP_LOSS_LIMIT":
                            self.logger.info(f"BinanceTrailingStopLossManager.start() - Found open STOP_LOSS_LIMIT "
                                             f"order with stop_loss_price={open_order['price']}.")
                            self.create_stop_loss_order(float(open_order['price']))
                else:
                    self.logger.info(f"BinanceTrailingStopLossManager.start() - No open STOP_LOSS_LIMIT orders found!")
            else:
                self.logger.info(f"BinanceTrailingStopLossManager.start() - Resetting old stop_loss_price!")
        else:
            self.logger.info(f"BinanceTrailingStopLossManager.start() - Using provided stop_loss_price="
                             f"{self.stop_loss_price}")
            self.create_stop_loss_order(self.stop_loss_price)

    def send_email_notification(self,
                                message: str = None) -> bool:
        """
        Send a notification via email!

        :param message: Text to send via email.
        :type message: str

        :return:
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.send_email_notification() - msg: {message}")
        if self.send_to_email_address \
                and self.send_from_email_address \
                and self.send_from_email_server \
                and self.send_from_email_port:
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL(self.send_from_email_server, self.send_from_email_port, context=context) as server:
                    server.login(self.send_from_email_address, self.send_from_email_password)
                    server.sendmail(self.send_from_email_address, self.send_to_email_address, message)
                    self.logger.info(f"BinanceTrailingStopLossManager.send_email_notification() - Email sent!")
                    if self.print_notifications:
                        print("Email sent!")
                    return True
            except socket.gaierror as error_msg:
                self.logger.info(f"BinanceTrailingStopLossManager.send_email_notification() - {error_msg}")
                if self.print_notifications:
                    print(f"ERROR: Email not sent! {error_msg}")
        else:
            self.logger.debug(f"BinanceTrailingStopLossManager.send_email_notification() - Data for email dispatch not "
                              f"available")
            return False

    def send_telegram_notification(self,
                                   message: str = None) -> bool:
        """
        Send a notification via telegram!

        :param message: Text to send via Telegram.
        :type message: str

        :return:
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.send_telegram_message() - msg: {message}")
        if self.telegram_send_to \
                and self.telegram_bot_token:
            date = datetime.datetime.now().strftime("%H:%M:%S")
            msg = message.replace("%25", "%")
            logging.info(" ".join([msg, "at", date]))
            request_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage?chat_id=" \
                          f"{self.telegram_send_to}&parse_mode=HTML&text={message}"
            response = requests.get(request_url)
            self.logger.info(f"BinanceTrailingStopLossManager.send_telegram_message() - response: {response}")
            return True
        else:
            self.logger.debug(f"BinanceTrailingStopLossManager.send_telegram_message() - Data for Telegram dispatch "
                              f"not available")
            return False

    def stop(self) -> bool:
        """
        Stop stop_loss! :)

        :return: bool
        """
        return self.stop_manager()

    def stop_manager(self, close_api_session: bool = True) -> bool:
        """
        Stop stop_loss! :)

        :return: bool
        """
        self.logger.info(f"BinanceTrailingStopLossManager.stop_manager() - Gracefully stopping "
                         f"unicorn-binance-trailing-stop-loss engine")
        self.stop_manager_request = True
        if self.ubwa is not None:
            self.ubwa.stop_manager()
        if self.ubra is not None:
            self.ubra.stop_manager()
        return True

    def set_stop_loss_price(self, stop_loss_price: float = None) -> bool:
        """
        Set the stop/loss price.

        :param stop_loss_price: Price to set for the SL order.
        :type stop_loss_price: float

        :return: bool
        """
        self.logger.debug(f"BinanceTrailingStopLossManager.set_stop_loss_price() - "
                          f"Setting new stop_loss_price={stop_loss_price}")
        self.stop_loss_price = stop_loss_price
        return True

    def update_stop_loss_quantity(self,
                                  total: float = 0.0,
                                  free: float = 0.0) -> float:
        """
        Calculate and update the stop_loss_quantity!

        :param total: Total asset amount
        :type total: float
        :param free: Free asset amount
        :type free: float

        :return: float
        """
        self.logger.info(f"BinanceTrailingStopLossManager.update_stop_loss_quantity() - Calculating the "
                         f"stop_loss_quantity amount.")
        if "%" in self.keep_threshold:
            keep_threshold_percent = float(self.keep_threshold.rstrip("%"))
            keep_threshold_float = total/100*keep_threshold_percent
        else:
            keep_threshold_float = float(self.keep_threshold)
        if keep_threshold_float > free:
            msg = f"BinanceTrailingStopLossManager.update_stop_loss_quantity() - Nothing to do - `keep_threshold` " \
                  f"is greater then `stop_loss_asset_amount_free`!"
            self.logger.critical(msg)
            self.send_telegram_notification(msg)
            self.send_email_notification(msg)
            self.stop_manager()
            if self.callback_error is not None:
                self.callback_error(msg)
            return False
        stop_loss_quantity = free - keep_threshold_float
        self.stop_loss_quantity = stop_loss_quantity
        return stop_loss_quantity

    def update_stop_loss_asset_amount(self,
                                      total: float = None,
                                      free: float = None) -> tuple:
        """
        Update the owning asset amount (total, free)!

        :param total: Total amount of the stop_loss_asset!
        :type total: float
        :param free: Free amount of the stop_loss_asset!
        :type free: float

        :return: tuple
        """
        if total is None or free is None:
            total, free = self.get_owning_amount(base_asset=self.stop_loss_asset_name)
        self.stop_loss_asset_amount = float(total)
        self.stop_loss_asset_amount_free = float(free)
        return total, free
