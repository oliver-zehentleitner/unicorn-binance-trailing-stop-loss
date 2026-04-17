#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: unicorn_binance_trailing_stop_loss/cli.py
#
# Part of ‘UNICORN Binance Trailing Stop Loss’
# Project website: https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html
# Github: https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss
# Documentation: https://unicorn-binance-trailing-stop-loss.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-binance-trailing-stop-loss
#
# License: MIT
# https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/LICENSE
#
# Author: Oliver Zehentleitner
#
# Copyright (c) 2022-2025, Oliver Zehentleitner (https://about.me/oliver-zehentleitner)
# All rights reserved.

try:
    from .manager import BinanceTrailingStopLossManager
except ModuleNotFoundError:
    from unicorn_binance_trailing_stop_loss.manager import BinanceTrailingStopLossManager
from unicorn_binance_rest_api.manager import BinanceRestApiManager, BinanceAPIException
from configparser import ConfigParser, ExtendedInterpolation, MissingSectionHeaderError, ParsingError
from pathlib import Path
from typing import Optional
import asyncio
import argparse
import logging
import platform
import os
import requests
import sys
import textwrap
import webbrowser


async def cli():
    """
        UNICORN Binance Trailing Stop Loss Command Line Interface Documentation

        More info: https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/cli.html
    """
    version = BinanceTrailingStopLossManager.get_version()
    os_type = platform.system()
    home_path = f"{Path.home()}{os.sep}"
    ubs_base = f"{home_path}.unicorn-binance-suite{os.sep}"
    config_path = f"{ubs_base}config{os.sep}"
    log_path = f"{ubs_base}logs{os.sep}"
    log_format = "{asctime} [{levelname:8}] {process} {thread} {module}: {message}"

    parser = argparse.ArgumentParser(
        prog='ubtsl',
        description=f'UNICORN Binance Trailing Stop Loss {version}\n'
                    f'https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
             examples:
                 Check if a new update is available:
                 $ ubtsl --checkupdate

                 Show program version:
                 $ ubtsl --version

                 Test the connectivity to the Binance API:
                 $ ubtsl --test binance-connectivity

                 Test notifications:
                 $ ubtsl --test notification

                 Start with profile "BTCUSDT_SELL" and overwrite the stoplosslimit:
                 $ ubtsl --profile BTCUSDT_SELL --stoplosslimit 0.5%

                 List all open orders:
                 $ ubtsl --exchange "binance.com" --market "BTCUSDT" --listopenorders
                 $ ubtsl --profile BTCUSDT_SELL --listopenorders

             disclaimer:
                 This project is for informational purposes only. You should not construe this
                 information or any other material as legal, tax, investment, financial or other
                 advice. If you intend to use real money, use it at your own risk. Under no
                 circumstances will we be responsible or liable for any claims, damages, losses,
                 expenses, costs or liabilities of any kind, including but not limited to direct
                 or indirect damages for loss of profits.
             '''))

    parser.add_argument('-ak', '--apikey',
                        type=str,
                        help="The API key",
                        required=False)
    parser.add_argument('-as', '--apisecret',
                        type=str,
                        help="The Binance API secret.",
                        required=False)
    parser.add_argument('-bt', '--borrowthreshold',
                        type=str,
                        help="How much of the possible credit line to exhaust. (Only available in Margin)",
                        required=False)
    parser.add_argument('-coo', '--cancelopenorders',
                        help=f'Cancel all open orders and then stop. Only valid in combination with parameter '
                             f'`exchange` and `market`.',
                        required=False,
                        action='store_true')
    parser.add_argument('-cci', '--createconfigini',
                        help=f'Create the config file and then stop.',
                        required=False,
                        action='store_true')
    parser.add_argument('-cpi', '--createprofilesini',
                        help=f'Create the profiles file and then stop.',
                        required=False,
                        action='store_true')
    parser.add_argument('-cf', '--configfile',
                        type=str,
                        help=f"Specify path including filename to the config file (ex: `~/my_config.ini`). If not "
                             f"provided ubtsl tries to load a `ubtsl_config.ini` from the `{config_path}` and the "
                             f"current working directory.",
                        required=False)
    parser.add_argument('-cu', '--checkupdate',
                        help=f'Check if update is available and then stop.',
                        required=False,
                        action='store_true')
    parser.add_argument('-ex', '--example',
                        type=str,
                        help=f'Show an example ini file from GitHub and then stop. Options: `config` or `profiles`.',
                        required=False)
    parser.add_argument('-e', '--exchange',
                        type=str,
                        help="Exchange: binance.com, binance.com-testnet, binance.com-futures, "
                             "binance.com-isolated_margin, binance.com-margin",
                        required=False)
    parser.add_argument('-n', '--engine',
                        type=str,
                        help='Choose the engine. Default: `trail` Options: `jump-in-and-trail` to place a buy order '
                             'and trail.',
                        required=False)
    parser.add_argument('-k', '--keepthreshold',
                        type=str,
                        help="Set the threshold to be kept. This is the amount that will not get sold.",
                        required=False)
    parser.add_argument('-lf', '--logfile',
                        type=str,
                        help='Specify path including filename to the logfile. Default is logfile path is '
                             '`{config_path}`',
                        required=False)
    parser.add_argument('-ll', '--loglevel',
                        type=str,
                        help='Choose a loglevel. Default: INFO; Options: DEBUG, INFO, WARNING, ERROR and CRITICAL',
                        required=False)
    parser.add_argument('-loo', '--listopenorders',
                        help=f'List all open orders and then stop. Only valid in combination with parameter '
                             f'`exchange` and `market`.',
                        required=False,
                        action='store_true')
    parser.add_argument('-m', '--market',
                        type=str,
                        help='The market on which is traded.',
                        required=False)
    parser.add_argument('-oci', '--openconfigini',
                        help=f'Open the used config file and then stop.',
                        required=False,
                        action='store_true')
    parser.add_argument('-opi', '--openprofilesini',
                        help=f'Open the used profiles file and then stop.',
                        required=False,
                        action='store_true')
    parser.add_argument('-ot', '--ordertype',
                        type=str,
                        help="Use `limit` or `market`.",
                        required=False)
    parser.add_argument('-pf', '--profile',
                        type=str,
                        help='Name of the profile to load from ubtsl_profiles.ini!',
                        required=False)
    parser.add_argument('-pff', '--profilesfile',
                        type=str,
                        help=f"Specify path including filename to the profiles file (ex: `~/my_profiles.ini`). If not "
                             f"available ubtsl tries to load a ubtsl_profile.ini from the `{config_path}` and the "
                             f"current working directory.",
                        required=False)
    parser.add_argument('-r', '--resetstoplossprice',
                        type=str,
                        help='Reset the existing stop_loss_price! usage: True anything else is False.',
                        required=False)
    parser.add_argument('-l', '--stoplosslimit',
                        type=str,
                        help='Stop/loss limit in float or percent.',
                        required=False)
    parser.add_argument('-sl', '--stoplossstartlimit',
                        type=str,
                        help='Set the start stop/loss limit in float or percent.',
                        required=False)
    parser.add_argument('-p', '--stoplossprice',
                        type=float,
                        help='Set the start stop/loss price as float value.',
                        required=False)
    parser.add_argument('-t', '--test',
                        type=str,
                        help='Use this to test specific systems like "notification", "binance-connectivity" and '
                             '"streams". The streams test needs a valid exchange and market. If test is not None the '
                             'engine will NOT start! It only tests!',
                        required=False)
    parser.add_argument('-v', '--version',
                        help=f'Show the program version and then stop. The version is `{version}` by the way :)',
                        required=False,
                        action='store_true')
    options = parser.parse_args()

    # Vars
    public_key = None
    private_key = None
    send_to_email_address = None
    send_from_email_address = None
    send_from_email_password = None
    send_from_email_server = None
    send_from_email_port = None
    telegram_bot_token = None
    telegram_send_to = None

    # Log file
    if options.logfile is True:
        logfile = options.logfile
    else:
        logfile = log_path + 'ubtsl.log'

    # Log level
    if options.loglevel == "DEBUG":
        loglevel = logging.DEBUG
    elif options.loglevel == "INFO":
        loglevel = logging.INFO
    elif options.loglevel == "WARN" or options.loglevel == "WARNING":
        loglevel = logging.WARNING
    elif options.loglevel == "ERROR":
        loglevel = logging.ERROR
    elif options.loglevel == "CRITICAL":
        loglevel = logging.CRITICAL
    else:
        loglevel = logging.INFO

    # Config logger
    parent_dir = Path(logfile).parent
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)
    try:
        logging.basicConfig(level=loglevel,
                            filename=logfile,
                            format=log_format,
                            style="{")
    except FileNotFoundError as error_msg:
        print(f"File not found: {error_msg}")
    logger = logging.getLogger("unicorn_binance_trailing_stop_loss")

    # Functions
    def callback_error(message):
        """
        Callback function for error event provided to the unicorn-binance-trailing-stop-loss engine

        :param message: Text message provided by ubtsl lib
        :return: None
        """
        logger.debug(f"callback_error() started, got message: {message}")
        ubtsl.stop_manager()

    def callback_finished(feedback):
        """
        Callback function for finished event provided to the unicorn-binance-trailing-stop-loss engine

        :param feedback: Contains stop loss order detail as well as smart entry buy order details
        :type feedback: dict
        :return: None
        """
        logger.debug(f"callback_finished() started ")
        if engine == "jump-in-and-trail":
            trade_fee = ubra.get_trade_fee(symbol=market)
            print(f"trade_fee: {trade_fee}")
            fee = 0.2
            profit = fee*(float(feedback['sell_order']['order_price'])-float(feedback['buy_order']['order_price']))
            print(f"======================================================\r\n"
                  f"buy_price: {float(feedback['buy_order']['order_price']):g}\r\n"
                  f"sell_price: {float(feedback['sell_order']['order_price']):g}\r\n"
                  f"fee: ~{fee}%\r\n"
                  f"------------------------------------------------------\r\n"
                  f"profit: {profit}")
        ubtsl.stop_manager()

    def load_examples_ini_from_github(example_name: str = None) -> Optional[str]:
        """
        Load example_*.ini files from GitHub

        :param example_name: `config` or `profiles`
        :type example_name:  str
        :return: str or None
        """
        logger.info(f"load_examples_ini_from_github() started ")
        if example_name is None:
            return None
        example_ini = f"https://raw.githubusercontent.com/oliver-zehentleitner/" \
                      f"unicorn-binance-trailing-stop-loss/master/cli/example_ubtsl_{example_name}.ini"
        response = requests.get(example_ini)
        return response.text

    def create_directory(directory: str = None) -> bool:
        """
        Create a directory if not exists.

        Returns True if exists or is successfully created

        :param directory: The full path of the directory to create
        :type directory: str
        :return: bool
        """
        logger.debug(f"create_directory() started ")
        if os.path.isdir(directory):
            return True
        else:
            os.makedirs(directory)
            return True

    # Exit if no args provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    # Create config ini
    if options.createconfigini is True:
        config_file_path = f"{config_path}ubtsl_config.ini"
        print("Creating config ini file ")
        if os.path.isfile(config_file_path):
            decision = input(f"The file `{config_file_path}` already exists. Do you want to overwrite it? [y/N]")
            if decision.upper() != "Y":
                return False
        create_directory(str(config_path))
        content = load_examples_ini_from_github("config")
        with open(config_file_path, "w+") as fh_config_file:
            fh_config_file.write(content)
        print(f"New config file `{config_file_path}` successfully created.")
        print(f"Use `ubtsl --openconfigini` to open it in an editor.")
        sys.exit(0)

    # Create profiles ini
    if options.createprofilesini is True:
        profiles_file_path = f"{config_path}ubtsl_profiles.ini"
        print("Creating profiles ini file ")
        if os.path.isfile(profiles_file_path):
            decision = input(f"The file `{profiles_file_path}` already exists. Do you want to overwrite it? [y/N]")
            if decision.upper() != "Y":
                return False
        create_directory(str(config_path))
        content = load_examples_ini_from_github("profiles")
        with open(profiles_file_path, "w+") as fh_profiles_file:
            fh_profiles_file.write(content)
        print(f"New profiles file `{profiles_file_path}` successfully created.")
        print(f"Use `ubtsl --openprofilesini` to open it in an editor.")
        sys.exit(0)

    # Update available?
    if options.checkupdate is True:
        ubtsl = BinanceTrailingStopLossManager(start_engine=False, warn_on_update=False)
        if ubtsl.is_update_available():
            print("A new update is available: https://github.com/oliver-zehentleitner/"
                  "unicorn-binance-trailing-stop-loss/releases/latest")
        else:
            print("No available updates found!")
        ubtsl.stop_manager()
        sys.exit(0)

    # Print the version
    if options.version is True:
        print(f"UNICORN Binance Trailing Stop Loss {version}")
        sys.exit(0)

    # Print examples ini files:
    if options.example is not None:
        if options.example == "config":
            print(f"{options.example}.ini example:\r\n{load_examples_ini_from_github(example_name=options.example)}")
        if options.example == "profiles":
            print(f"{options.example}.ini example:\r\n{load_examples_ini_from_github(example_name=options.example)}")
        sys.exit(0)

    # Choose config file
    if options.configfile is not None:
        # Load from cli arg if provided
        config_file = str(options.configfile)
    else:
        # Load config from default filenames
        config_file_cwd = "ubtsl_config.ini"
        config_file_home = f"{config_path}ubtsl_config.ini"
        if os.path.isfile(config_file_cwd):
            config_file = config_file_cwd
        elif os.path.isfile(config_file_home):
            config_file = config_file_home
        else:
            config_file = None
            if not options.openconfigini and not options.openprofilesini:
                if options.apikey is None or options.apisecret is None:
                    msg = f"You must provide a valid Binance API key and secret, either as commandline parameter or as " \
                          f"profile parameter.  Please use `ubtsl --help` for further information!"
                    logger.critical(msg)
                    print(msg)
                    sys.exit(1)

    # Choose profiles file
    if options.profilesfile is not None:
        # Load from cli arg if provided
        profiles_file = str(options.profilesfile)
    else:
        profiles_file_cwd = "ubtsl_profiles.ini"
        profiles_file_home = f"{config_path}ubtsl_profiles.ini"
        if os.path.isfile(profiles_file_cwd):
            profiles_file = profiles_file_cwd
        elif os.path.isfile(profiles_file_home):
            profiles_file = profiles_file_home
        else:
            profiles_file = None

    # Open ini files
    if options.openconfigini:
        if config_file is None:
            print(f"No config file found!\r\n"
                  f"Use `ubtsl --createconfigini` to create one.")
        else:
            print(f"Opening `{config_file}`")
            webbrowser.open(config_file)
        sys.exit(0)

    if options.openprofilesini:
        if profiles_file is None:
            print(f"No profiles file found!\r\n"
                  f"Use `ubtsl --createprofilesini` to create one.")
        else:
            print(f"Opening `{profiles_file}`")
            webbrowser.open(profiles_file)
        sys.exit(0)

    # Officially starting :)
    logger.info(f"Started ubtsl_{version}")
    print(f"Started ubtsl_{version}")

    # Loading config ini
    if config_file:
        logger.info(f"Loading configuration file `{config_file}`")
        print(f"Loading configuration file `{config_file}`")
        config = ConfigParser(interpolation=ExtendedInterpolation())
        try:
            config.read(config_file)
        except (MissingSectionHeaderError, ParsingError) as error_msg:
            msg = f"Error: Config file `{config_file}` is invalid: {error_msg}\n" \
                  f"Use `ubtsl --createconfigini` to create a valid config file."
            logger.critical(msg)
            print(msg)
            sys.exit(1)
        try:
            public_key = config['BINANCE']['api_key']
            private_key = config['BINANCE']['api_secret']
            send_to_email_address = config['EMAIL']['send_to_email']
            send_from_email_address = config['EMAIL']['send_from_email']
            send_from_email_password = config['EMAIL']['send_from_password']
            send_from_email_server = config['EMAIL']['send_from_server']
            send_from_email_port = config['EMAIL']['send_from_port']
            telegram_bot_token = config['TELEGRAM']['bot_token']
            telegram_send_to = config['TELEGRAM']['send_to']
        except KeyError as error_msg:
            msg = f"Error: Missing section or key in config file `{config_file}`: {error_msg}\n" \
                  f"Use `ubtsl --createconfigini` to create a valid config file."
            logger.critical(msg)
            print(msg)
            sys.exit(1)

    # Init trailing stop loss vars
    borrow_threshold = ""
    engine = "trail"
    exchange = ""
    keep_threshold = ""
    market = ""
    stop_loss_limit = ""
    stop_loss_start_limit = ""
    stop_loss_order_type = ""
    stop_loss_price: float = 0.0
    reset_stop_loss_price = False
    test = None
    ubra = False

    # Load a profile is provided via argparse
    if options.profile is not None:
        # Loading profiles ini
        logger.info(f"Loading profiles file `{profiles_file}`")
        print(f"Loading profiles file `{profiles_file}`")
        profiles = ConfigParser(interpolation=ExtendedInterpolation())
        profiles.read(profiles_file)

        # Mapping parameters
        try:
            if profiles[options.profile]:
                try:
                    borrow_threshold = profiles[options.profile]['borrow_threshold']
                except KeyError:
                    pass
                try:
                    exchange = profiles[options.profile]['exchange']
                except KeyError:
                    pass
                try:
                    keep_threshold = profiles[options.profile]['keep_threshold']
                except KeyError:
                    pass
                try:
                    reset_stop_loss_price = profiles[options.profile]['reset_stop_loss_price']
                except KeyError:
                    pass
                try:
                    engine = profiles[options.profile]['engine']
                except KeyError:
                    pass
                try:
                    market = profiles[options.profile]['market']
                except KeyError:
                    pass
                try:
                    stop_loss_limit = profiles[options.profile]['stop_loss_limit']
                except KeyError:
                    pass
                try:
                    stop_loss_start_limit = profiles[options.profile]['stop_loss_start_limit']
                except KeyError:
                    pass
                try:
                    stop_loss_order_type = profiles[options.profile]['stop_loss_order_type']
                except KeyError:
                    pass
                try:
                    stop_loss_price = float(profiles[options.profile]['stop_loss_price'])
                except KeyError:
                    pass
        except KeyError as error_msg:
            print(f"ERROR: Profile {error_msg} not found!")
            sys.exit(1)

    # cli args overwrite profile settings
    if options.apikey is not None:
        public_key = options.apikey
    if options.apisecret is not None:
        private_key = options.apisecret
    if options.borrowthreshold is not None:
        borrow_threshold = options.borrowthreshold
    if options.engine is not None:
        engine = options.engine
    if options.exchange is not None:
        exchange = options.exchange
    if options.keepthreshold is not None:
        keep_threshold = options.keepthreshold
    if options.market is not None:
        market = options.market
    if options.stoplosslimit is not None:
        stop_loss_limit = options.stoplosslimit
    if options.stoplossstartlimit is not None:
        stop_loss_start_limit = options.stoplossstartlimit
    if options.ordertype is not None:
        stop_loss_order_type = options.ordertype
    if options.resetstoplossprice is not None:
        reset_stop_loss_price = options.resetstoplossprice
    if options.stoplossprice is not None:
        stop_loss_price = options.stoplossprice
    if options.test is not None:
        test = options.test

    # Normalize `reset_stop_loss_price`
    if str(reset_stop_loss_price).upper() == "TRUE":
        reset_stop_loss_price = True
    else:
        reset_stop_loss_price = False

    # Creating UBRA
    ubra = BinanceRestApiManager(api_key=public_key, api_secret=private_key)

    if options.cancelopenorders is True:
        print(f"Canceling all orders of `{market}` on `{exchange}`")
        try:
            if exchange == "binance.com" or exchange == "binance.com-testnet":
                canceled_orders = ubra.cancel_all_open_orders(symbol=market)
            elif exchange == "binance.com-margin":
                canceled_orders = ubra.cancel_all_open_margin_orders(symbol=market)
            elif exchange == "binance.com-isolated_margin":
                canceled_orders = ubra.cancel_all_open_margin_orders(symbol=market, isIsolated="TRUE")
            elif exchange == "binance.com-futures":
                canceled_orders = ubra.futures_cancel_all_open_orders(symbol=market)
            else:
                print(f"Invalid exchange `{exchange}")
                sys.exit(1)
        except BinanceAPIException as error_msg:
            if "code=-2011" in str(error_msg):
                print(f"No order was found to cancel!")
            else:
                print(f"ERROR: Not able to cancel all open orders. {error_msg}")
            sys.exit(1)
        print(f"Canceled orders: {canceled_orders}")
        sys.exit(0)

    if options.listopenorders is True:
        print(f"Getting open orders of `{market}` on `{exchange}`")
        try:
            if exchange == "binance.com" or exchange == "binance.com-testnet":
                open_orders = ubra.get_open_orders(symbol=market)
            elif exchange == "binance.com-margin":
                open_orders = ubra.get_open_margin_orders(symbol=market)
            elif exchange == "binance.com-isolated_margin":
                open_orders = ubra.get_open_margin_orders(symbol=market, isIsolated="TRUE")
            elif exchange == "binance.com-futures":
                open_orders = ubra.futures_get_open_orders(symbol=market)
            else:
                print(f"Invalid exchange `{exchange}")
                sys.exit(1)
        except BinanceAPIException as error_msg:
            print(f"ERROR: Not able to fetch all open orders. {error_msg}")
            sys.exit(1)
        print(f"Open orders: {open_orders}")
        sys.exit(0)

    # Starting the Trailing Stop/Loss Engine
    with BinanceTrailingStopLossManager(callback_error=callback_error,
                                        callback_finished=callback_finished,
                                        callback_partially_filled=None,
                                        api_key=public_key,
                                        api_secret=private_key,
                                        borrow_threshold=borrow_threshold,
                                        engine=engine,
                                        exchange=exchange,
                                        keep_threshold=keep_threshold,
                                        market=market,
                                        print_notifications=True,
                                        reset_stop_loss_price=reset_stop_loss_price,
                                        send_to_email_address=send_to_email_address,
                                        send_from_email_address=send_from_email_address,
                                        send_from_email_password=send_from_email_password,
                                        send_from_email_server=send_from_email_server,
                                        send_from_email_port=int(send_from_email_port),
                                        stop_loss_limit=stop_loss_limit,
                                        stop_loss_order_type=stop_loss_order_type,
                                        stop_loss_price=stop_loss_price,
                                        stop_loss_start_limit=stop_loss_start_limit,
                                        telegram_bot_token=telegram_bot_token,
                                        telegram_send_to=telegram_send_to,
                                        test=test,
                                        ubra_manager=ubra,
                                        ubwa_manager=None,
                                        warn_on_update=False) as ubtsl:
        if test is None:
            # Catch Keyboard Interrupt only if there is no test running
            while ubtsl.is_manager_stopping() is False:
                # This loop continues until the trailing stop loss engine is terminated
                await asyncio.sleep(1)


def main():
    try:
        asyncio.run(cli())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")


if __name__ == "__main__":
    main()
