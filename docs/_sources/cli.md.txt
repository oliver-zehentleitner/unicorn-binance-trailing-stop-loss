[![GitHub Release](https://img.shields.io/github/release/oliver-zehentleitner/unicorn-binance-trailing-stop-loss.svg?label=github)](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/releases)
[![PyPi Release](https://img.shields.io/pypi/v/unicorn-binance-trailing-stop-loss?color=blue)](https://pypi.org/project/unicorn-binance-trailing-stop-loss/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/LICENSE)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/unicorn_binance_trailing_stop_loss.svg)](https://www.python.org/downloads/)
[![Unit Tests](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/actions/workflows/unit-tests.yml)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/)
[![Telegram](https://img.shields.io/badge/community-telegram-41ab8c)](https://t.me/unicorndevs)

# UNICORN Binance Trailing Stop Loss CLI

[Description](#description) | [Installation](#installation) | [Usage](#usage) |
[Example commands](#example-commands) | [Smart Entry](#smart-entry) | [Example files](#example-files) |
[Documentation](#documentation) | [Disclaimer](#disclaimer)

After starting the engine, a stop/loss order is placed and trailed until it is completely fulfilled. If desired, a
notification can be sent via email afterwards.

In addition, there is a smart entry option called `jump-in-and-trail`. This offers the possibility to buy spot, 
future and margin assets with a limit or market order and then to trail a stop/loss order until sold.

The CLI interface `ubtsl` is installed during the
[installation of `unicorn-binance-trailing-stop-loss`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss#installation-and-upgrade)
with `pip` and is used to interact with the
[`unicorn-binance-trailing-stop-loss`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss) Python library.

Please read carefully all provided [documentation](https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/), our
[disclaimer](#disclaimer) and look in the
[issues](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/issues) about known
problems before using this tool - ***you use it at your own risk!***

If you put this engine on a market, you should stop trading manually on this market yourself!

Part of '[UNICORN Binance Suite](https://github.com/oliver-zehentleitner/unicorn-binance-suite)'.

## Description
After startup `ubtsl` tries to load a
[`ubtsl_config.ini`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini)
and a
[`ubtsl_profiles.ini`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini)
file from the `{home}/.unicorn-binance-suite/config/` and the current working directory. Alternatively, you can specify these files explicitly with the
`--configfile` and `--profilesfile` parameters.

Once the tool is started, it trails the stop/loss order until it is completely fulfilled, sends the notifications, and
then it stops.

***Supported exchanges:***

| Exchange                                           | Exchange string               | trail | jump-in-and-trail |
|----------------------------------------------------|-------------------------------|-------|--------------------|
| [Binance](https://www.binance.com)                 | `binance.com`                 | yes   | no                 |
| [Binance Testnet](https://testnet.binance.vision/) | `binance.com-testnet`         | yes   | no                 |
| [Binance Futures](https://www.binance.com)         | `binance.com-futures`         | yes   | no                 |
| [Binance Isolated Margin](https://www.binance.com) | `binance.com-isolated_margin` | yes   | yes (experimental) |
| [Binance Margin](https://www.binance.com)          | `binance.com-margin`          | yes   | no                 |

## Installation

```
pip install unicorn-binance-trailing-stop-loss
```

Every parameter that can be configured via the [`ubtsl_profiles.ini`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini)
or the [`ubtsl_config.ini`](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini)
file can also be defined as a command line argument. Therefore, both files are not mandatory, but they increase the
usability immensely.

### Create `ubtsl_config.ini`
A fresh `ubtsl_config.ini` file can be created with the following command

```sh
$ ubtsl --createconfigini
```

### Create `ubtsl_profiles.ini`
The same command is available for the `ubtsl_profiles.ini` file:

```sh
$ ubtsl --createprofilesini
```

### Open `ubtsl_config.ini`
Open the used `ubtsl_config.ini` file in a GUI editor:

```sh
$ ubtsl --openconfigini
```

### Open `ubtsl_profiles.ini`
The same command is available for the `ubtsl_profiles.ini` file:

```sh
$ ubtsl --openprofilesini
```

### Test the notification settings
If you entered valid email settings you can test the notification system:

```sh
$ ubtsl --test notification
```

### Test connectivity to Binance API
If you entered valid API key and secret you can test the connectivity to the Binance API:

```sh
$ ubtsl --test binance-connectivity
```

### Test data streams
Test the data streams, this test needs a defined exchange and market parameter:

```sh
$ ubtsl --test streams --exchange binance.com --market BTCUSDT
```

It is possible to use `exchange` and `market` values of a profile.

```sh
$ ubtsl --profile "BTCUSDT_SELL" --test streams
```

## Usage

```sh
$ ubtsl --help
```

Alternatively, it is possible to run `ubtsl` in the Python environment as follows:

Linux/Mac:

```sh
$ python3 -m ubtsl --help
```

Windows:

```sh
$ py -m ubtsl --help
```

### Load a profile

If profiles are available, they can be activated with the `--profile` parameter at startup.

```sh
$ ubtsl --profile BTCUSDT_SELL
```

### Command line arguments

Instead of loading the values from profiles, they can also be defined explicitly via command line parameters.

Any CLI parameters will overwrite predefined values from the profile.

All parameters that expect numbers can be configured with fixed numerical values as well as with percentage values.

## Example commands
### Check if a new update is available
```sh
$ ubtsl --checkupdate
```

### Show program version
```sh
$ ubtsl --version
```

### Overwrite values
Arguments defined in the CLI overrule values from the loaded profile!

Start with profile "BTCUSDT_SELL" and overwrite the stoplosslimit:

```sh
$ ubtsl --profile BTCUSDT_SELL --stoplosslimit 0.5%
```

### Smart entry
***This function is still in an experimental phase and only available for Isolated Margin.***

Do a smart entry by using `engine = jump-in-and-trail` like it is defined within the profile `BTCUSDT_SMART_ENTRY`
of the [example_ubtsl_profiles.ini](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini).

By activating the `jump-in-and-trail` engine, it first buys the predefined asset amount and then trails them
automatically.

```sh
$ ubtsl --profile BTCUSDT_SMART_ENTRY
```

### List all open orders
Get a list of all open orders.

```sh
$ ubtsl --exchange "binance.com" --market "BTCUSDT" --listopenorders
```

It is possible to use `exchange` and `market` values of a profile.

```sh
$ ubtsl --profile "BTCUSDT_SELL" --listopenorders
```

### Cancel all open orders

```sh
$ ubtsl --exchange "binance.com" --market "BTCUSDT" --cancelopenorders
```

It's possible to use `exchange` and `market` values of a profile.

```sh
$ ubtsl --profile "BTCUSDT_SELL" --cancelopenorders
```

## Example files
- [example_ubtsl_config.ini](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_config.ini)
- [example_ubtsl_profiles.ini](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/cli/example_ubtsl_profiles.ini)

## Documentation
- [General](https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss)
- [Modules](https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/modules.html)
- [CLI](https://oliver-zehentleitner.github.io/unicorn-binance-trailing-stop-loss/cli.html)

## Contributing
[UNICORN Binance Trailing Stop Loss](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss) is an open
source project which welcomes contributions which can be anything from simple documentation fixes and reporting dead links to new features. To
contribute follow
[this guide](https://github.com/oliver-zehentleitner/unicorn-binance-trailing-stop-loss/blob/master/CONTRIBUTING.md).

## Disclaimer
This project is for informational purposes only. Nothing contained herein constitutes financial advice or a
solicitation to buy or sell securities.

***If you intend to use real money, use it at your own risk.***

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities
of any kind, including but not limited to direct or indirect damages for loss of profits.
