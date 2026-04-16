[![Get a UNICORN Binance Suite License](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/logo/LUCIT-UBS-License-Offer.png)](https://shop.lucit.services)

[![Github](https://img.shields.io/badge/source-github-cbc2c8)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss)
[![GitHub Release](https://img.shields.io/github/release/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss.svg?label=github)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/total?color=blue)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/releases)
[![Anaconda Release](https://anaconda.org/lucit/unicorn-binance-trailing-stop-loss/badges/version.svg)](https://anaconda.org/lucit/unicorn-binance-trailing-stop-loss)
[![Anaconda Downloads](https://anaconda.org/lucit/unicorn-binance-trailing-stop-loss/badges/downloads.svg)](https://anaconda.org/lucit/unicorn-binance-trailing-stop-loss)
[![PyPi Release](https://img.shields.io/pypi/v/unicorn-binance-trailing-stop-loss?color=blue)](https://pypi.org/project/unicorn-binance-trailing-stop-loss/)
[![PyPi Downloads](https://pepy.tech/badge/unicorn-binance-trailing-stop-loss)](https://pepy.tech/project/unicorn-binance-trailing-stop-loss)
[![License](https://img.shields.io/badge/license-LSOSL-blue)](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/license.html)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/unicorn_binance_trailing_stop_loss.svg)](https://www.python.org/downloads/)
[![PyPI - Status](https://img.shields.io/pypi/status/unicorn_binance_trailing_stop_loss.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/issues)
[![codecov](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/branch/master/graph/badge.svg?token=5I03AZ3F5S)](https://codecov.io/gh/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss)
[![CodeQL](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/codeql-analysis.yml)
[![Unit Tests](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/unit-tests.yml)
[![Build and Publish GH+PyPi](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/build_wheels.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/build_wheels.yml)
[![Build and Publish Anaconda](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/build_conda.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/actions/workflows/build_conda.yml)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/)
[![Read How To`s](https://img.shields.io/badge/read-%20howto-yellow)](https://medium.lucit.tech)
[![Telegram](https://img.shields.io/badge/chat-telegram-41ab8c)](https://t.me/unicorndevs)
[![Gitter](https://badges.gitter.im/unicorn-binance-suite/unicorn-binance-trailing-stop-loss.svg)](https://gitter.im/unicorn-binance-suite/unicorn-binance-trailing-stop-loss?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![LUCIT-UBTSL-Banner](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/logo/LUCIT-UBTSL-Banner-Readme.png)](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html)

# UNICORN Binance Trailing Stop Loss CLI

[Description](#description) | [Installation](#installation) | [Usage](#usage) | 
[Example commands](#example-commands) | [Smart Entry](#smart-entry) | [Example files](#example-files) | 
[Change Log](#change-log) | [Wiki](#wiki) | [Social](#social) |
[Notifications](#receive-notifications) | [Bugs](#how-to-report-bugs-or-suggest-improvements) | 
[Contributing](#contributing) | [Leave a review](#you-want-to-say-thank-you) | [Disclaimer](#disclaimer) | [Commercial Support](#commercial-support)

After starting the engine, a stop/loss order is placed and trailed until it is completely fulfilled. If desired, a 
notification can be sent via email and Telegram afterwards.

In addition, there is a [smart entry](https://www.lucit.tech/ubtsl-cli.html#smart-entry) option called 
`jump-in-and-trail`. This offers the possibility to buy spot, future and margin assets with a limit or market order and 
then to trail a stop/loss order until sold.

The CLI interface `ubtsl`/`ubtsl.exe` is installed during the 
[installation of `unicorn-binance-trailing-stop-loss`](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html#installation-and-upgrade) 
with `pip` or `conda` and is used to interact with the [`unicorn-binance-trailing-stop-loss`](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html) Python library.

Please read carefully all provided [documentation](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/), our
[disclaimer](#disclaimer) and look in the 
[issues](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/issues) about known 
problems before using this tool - ***you use it at your own risk!***

If you put this engine on a market, you should stop trading manually on this market yourself!

Part of '[UNICORN Binance Suite](https://www.lucit.tech/unicorn-binance-suite.html)'.

## Get a UNICORN Binance Suite License

To run modules of the *UNICORN Binance Suite* you need a [valid license](https://medium.lucit.tech/how-to-obtain-and-use-a-unicorn-binance-suite-license-key-and-run-the-ubs-module-according-to-best-87b0088124a8#4ca4)!

## Description
After startup `ubtsl` tries to load a 
[`ubtsl_config.ini`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini) 
and a 
[`ubtsl_profiles.ini`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini) 
file from the `{home}/.lucit/` and the current working directory. Alternatively, you can specify these files explicitly with the 
`--configfile` and `--profilesfile` parameters.

Once the tool is started, it trails the stop/loss order until it is completely fulfilled, sends the notifications, and
then it stops.

***Supported exchanges:***

| Exchange                                           | Exchange string               | trail                                                                                                                                     | jump-in-and-trail                                                                                                                                        | 
|----------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------| 
| [Binance](https://www.binance.com)                 | `binance.com`                 | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/x-icon.png)                  |
| [Binance Testnet](https://testnet.binance.vision/) | `binance.com-testnet`         | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) | ![no](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/x-icon.png)                  |
| [Binance Futures](https://www.binance.com)         | `binance.com-futures`         | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/x-icon.png)                 |
| [Binance Isolated Margin](https://www.binance.com) | `binance.com-isolated_margin` | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) (experimental) |
| [Binance Margin](https://www.binance.com)          | `binance.com-margin`          | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/ok-icon.png) | ![yes](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/x-icon.png)                 |

## Installation
The CLI interface `ubtsl`/`ubtsl.exe` is installed during the 
[installation of `unicorn-binance-trailing-stop-loss`](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html#installation-and-upgrade) 
with `pip` or `conda` and is used to interact with the [`unicorn-binance-trailing-stop-loss`](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html) Python library.

Every parameter that can be configured via the [`ubtsl_profiles.ini`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini) 
or the [`ubtsl_config.ini`](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini) 
file can also be defined as a command line argument. Therefore, both files are not mandatory, but it increases the 
usability immensely.

### Create `ubtsl_config.ini`
A fresh `ubtsl_config.ini` file can be created with the following command

```
$ ubtsl --createconfigini 
```

### Create `ubtsl_profiles.ini`
The same command is available for the `ubtsl_profiles.ini` file:

```
$ ubtsl --createprofilesini 
```

### Open `ubtsl_config.ini`
Open the used `ubtsl_config.ini` file in a GUI editor: 

```
$ ubtsl --openconfigini 
```

### Open `ubtsl_profiles.ini`
The same command is available for the `ubtsl_profiles.ini` file:

```
$ ubtsl --openprofilesini 
```

### Test the notification settings
If you entered valid email and/or Telegram settings you can test the notification system:

```
$ ubtsl --test notification
```

### Test connectivity to Binance API
If you entered valid API key and secret you can test the connectivity to the Binance API:

```
$ ubtsl --test binance-connectivity
```

### Test data streams
Test the data streams, this test needs a defined exchange and market parameter:

```
$ ubtsl --test streams --exchange binance.com --market BTCUSDT
```

It is possible to use `exchange` and `market` values of a profile. 

```
$ ubtsl --profile "BTCUSDT_SELL" --test streams
```

## Usage

```
$ ubtsl --help
```

Alternatively, it is possible to run `ubtsl` in the Python environment as follows:

Linux/Mac:

```
$ python3 -m ubtsl --help
```

Windows:

```
$ py -m ubtsl --help
```

### Load a profile

If profiles are available, they can be activated with the `--profile` parameter at startup. 

```
$ ubtsl --profile BTCUSDT_SELL
```

### Command line arguments

Instead of loading the values from profiles, they can also be defined explicitly via command line parameters. 

Any CLI parameters will overwrite predefined values from the profile.

All parameters that expect numbers can be configured with fixed numerical values as well as with percentage values.

```
$ ubtsl --help
usage: ubtsl [-h] [-ak APIKEY] [-as APISECRET] [-bt BORROWTHRESHOLD] [-coo] [-cci] [-cpi] [-cf CONFIGFILE] [-cu]
             [-ex EXAMPLE] [-e EXCHANGE] [-n ENGINE] [-k KEEPTHRESHOLD] [-lf LOGFILE] [-ll LOGLEVEL] [-loo]
             [-m MARKET] [-oci] [-opi] [-ot ORDERTYPE] [-pf PROFILE] [-pff PROFILESFILE] [-r RESETSTOPLOSSPRICE]
             [-l STOPLOSSLIMIT] [-sl STOPLOSSSTARTLIMIT] [-p STOPLOSSPRICE] [-t TEST] [-v]

UNICORN Binance Trailing Stop Loss 0.7.1 by LUCIT Systems and Development (MIT License)

options:
  -h, --help            show this help message and exit
  -ak APIKEY, --apikey APIKEY
                        the API key
  -as APISECRET, --apisecret APISECRET
                        The Binance API secret.
  -bt BORROWTHRESHOLD, --borrowthreshold BORROWTHRESHOLD
                        How much of the possible credit line to exhaust. (Only available in Margin)
  -coo, --cancelopenorders
                        Cancel all open orders and then stop. Only valid in combination with parameter `exchange` and
                        `market`.
  -cci, --createconfigini
                        Create the config file and then stop.
  -cpi, --createprofilesini
                        Create the profiles file and then stop.
  -cf CONFIGFILE, --configfile CONFIGFILE
                        Specify path including filename to the config file (ex: `~/my_config.ini`). If not provided
                        ubtsl tries to load a `ubtsl_config.ini` from the `{home}\.lucit\` and the current
                        working directory.
  -cu, --checkupdate    Check if update is available and then stop.
  -ex EXAMPLE, --example EXAMPLE
                        Show an example ini file from GitHub and then stop. Options: `config` or `profiles`.
  -e EXCHANGE, --exchange EXCHANGE
                        Exchange: binance.com, binance.com-testnet, binance.com-futures, binance.com-isolated_margin,
                        binance.com-margin
  -n ENGINE, --engine ENGINE
                        Choose the engine. Default: `trail` Options: `jump-in-and-trail` to place a buy order and
                        trail
  -k KEEPTHRESHOLD, --keepthreshold KEEPTHRESHOLD
                        Set the threshold to be kept. This is the amount that will not get sold.
  -lf LOGFILE, --logfile LOGFILE
                        Specify path including filename to the logfile.
  -ll LOGLEVEL, --loglevel LOGLEVEL
                        Choose a loglevel. Default: INFO Options: DEBUG, INFO, WARNING, ERROR and CRITICAL
  -loo, --listopenorders
                        List all open orders and then stop. Only valid in combination with parameter `exchange` and
                        `market`.
  -m MARKET, --market MARKET
                        The market on which is traded.
  -oci, --openconfigini
                        Open the used config file and then stop.
  -opi, --openprofilesini
                        Open the used profiles file and then stop.
  -ot ORDERTYPE, --ordertype ORDERTYPE
                        Use `limit` or `market`.
  -pf PROFILE, --profile PROFILE
                        Name of the profile to load from ubtsl_profiles.ini!
  -pff PROFILESFILE, --profilesfile PROFILESFILE
                        Specify path including filename to the profiles file (ex: `~/my_profiles.ini`). If not
                        available ubtsl tries to load a ubtsl_profile.ini from the `{home}\.lucit\` and the
                        current working directory.
  -r RESETSTOPLOSSPRICE, --resetstoplossprice RESETSTOPLOSSPRICE
                        Reset the existing stop_loss_price! usage: True anything else is False.
  -l STOPLOSSLIMIT, --stoplosslimit STOPLOSSLIMIT
                        Stop/loss limit in float or percent.
  -sl STOPLOSSSTARTLIMIT, --stoplossstartlimit STOPLOSSSTARTLIMIT
                        Set the start stop/loss limit in float or percent.
  -p STOPLOSSPRICE, --stoplossprice STOPLOSSPRICE
                        Set the start stop/loss price as float value.
  -t TEST, --test TEST  Use this to test specific systems like "notification", "binance-connectivity" and "streams".
                        The streams test needs a valid exchange and market. If test is not None the engine will NOT
                        start! It only tests!
  -v, --version         Show the program version and then stop. the version is `0.7.1` by the way :)
```

## Example commands
### Check if a new update is available
```
$ ubtsl --checkupdate
```

### Show program version
```
$ ubtsl --version
```

### Overwrite values
Arguments defined in the CLI overrule values from the loaded profile!

Start with profile "BTCUSDT_SELL" and overwrite the stoplosslimit:

```
$ ubtsl --profile BTCUSDT_SELL --stoplosslimit 0.5%
```

### Smart entry
***This function is still in an experimental phase and only available for Isolated Margin.***

Do a smart entry by using `engine = jump-in-and-trail` like it is defined within the profile `BTCUSDT_SMART_ENTRY` 
of the [example_ubtsl_profiles.ini](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini).

By activating the `jump-in-and-trail` engine, it first buys the predefined asset amount and then trails them 
automatically. 

```
$ ubtsl --profile BTCUSDT_SMART_ENTRY
```

### List all open orders
Get a list of all open orders.

```
$ ubtsl --exchange "binance.com" --market "BTCUSDT" --listopenorders 
```

It is possible to use `exchange` and `market` values of a profile. 

```
$ ubtsl --profile "BTCUSDT_SELL" --listopenorders
```

### Cancel all open orders

```
$ ubtsl --exchange "binance.com" --market "BTCUSDT" --cancelopenorders 
```

It's possible to use `exchange` and `market` values of a profile.

```
$ ubtsl --profile "BTCUSDT_SELL" --listopenorders
```

## Example files
- [example_ubtsl_config.ini](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini)
- [example_ubtsl_profiles.ini](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini)

## Change Log
[https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/CHANGELOG.html](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/CHANGELOG.html)

## Documentation
- [General](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech)
- [Modules](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/unicorn_binance_trailing_stop_loss.html)
- [CLI](https://unicorn-binance-trailing-stop-loss.docs.lucit.tech/CLI.html)

## Project Homepage
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss)

## Wiki
[https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/wiki](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/wiki)

## Social
- [Discussions](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/discussions)
- [https://t.me/unicorndevs](https://t.me/unicorndevs)
- [https://dev.binance.vision](https://dev.binance.vision)
- [https://community.binance.org](https://community.binance.org)

## Receive Notifications
To receive notifications on available updates you can 
[![watch](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/watch.png)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/watchers) 
the repository on [GitHub](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss).

Follow us on [Twitter](https://twitter.com/LUCIT_SysDev) or on [Facebook](https://www.facebook.com/lucit.systems.and.development) 
for general news about the [unicorn-binance-suite](https://www.lucit.tech/unicorn-binance-suite.html)!

To receive news (like inspection windows/maintenance) about the Binance API`s subscribe to their telegram groups: 

- [https://t.me/binance_api_announcements](https://t.me/binance_api_announcements)
- [https://t.me/binance_api_english](https://t.me/binance_api_english)
- [https://t.me/Binance_JEX_EN](https://t.me/Binance_JEX_EN)
- [https://t.me/Binance_USA](https://t.me/Binance_USA)
- [https://t.me/TRBinanceTR](https://t.me/TRBinanceTR)
- [https://t.me/BinanceDEXchange](https://t.me/BinanceDEXchange)
- [https://t.me/BinanceExchange](https://t.me/BinanceExchange)

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - 
click ![thumbs-up](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/thumbup.png) if you need one of them or suggest a new feature!

Before you report a bug, [try the latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss#installation-and-upgrade). If the issue still exists, provide the error trace, OS 
and Python version and explain how to reproduce the error. A demo script is appreciated.

If you dont find an issue related to your topic, please open a new [issue](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/issues)!

[Report a security bug!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/security/policy)

## Contributing
[UNICORN Binance Trailing Stop Loss](https://www.lucit.tech/unicorn-binance-trailing-stop-loss.html) is an open 
source project which welcomes contributions which can be anything from simple documentation fixes and reporting dead links to new features. To 
contribute follow 
[this guide](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/blob/master/CONTRIBUTING.md).
 
### Contributors
[![Contributors](https://contributors-img.web.app/image?repo=LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-trailing-stop-loss/graphs/contributors)

We ![love](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-trailing-stop-loss/master/images/misc/heart.png) open source!

## You want to say Thank You?
We hope you are enjoying using our libraries and that they are proving to be useful to you. If you have a moment, we would greatly appreciate it if you could leave us a [review on Google](https://g.page/r/CbfHlcs8BfG8EAg/review). Thank you for your support!

## Disclaimer
This project is for informational purposes only. You should not construe this information or any other material as 
legal, tax, investment, financial or other advice. Nothing contained herein constitutes a solicitation, recommendation, 
endorsement or offer by us or any third party provider to buy or sell any securities or other financial instruments in 
this or any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such 
jurisdiction.

***If you intend to use real money, use it at your own risk.***

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities 
of any kind, including but not limited to direct or indirect damages for loss of profits.

## Commercial Support

[![Get professional and fast support](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-binance-suite/master/images/support/LUCIT-get-professional-and-fast-support.png)](https://www.lucit.tech/get-support.html)

***Do you need a developer, operator or consultant?*** [Contact us](https://www.lucit.tech/contact.html) for a non-binding initial consultation!
